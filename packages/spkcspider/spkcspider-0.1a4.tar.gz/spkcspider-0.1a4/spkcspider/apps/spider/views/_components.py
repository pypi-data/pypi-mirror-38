
__all__ = (
    "ComponentIndex", "ComponentPublicIndex", "ComponentCreate",
    "ComponentUpdate", "ComponentDelete"
)

from urllib.parse import urljoin

from datetime import timedelta

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.db import models
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from rdflib import Graph, Literal, URIRef

from ._core import UserTestMixin, UCTestMixin
from ..constants.static import index_names
from ..forms import UserComponentForm
from ..contents import installed_contents
from ..models import UserComponent, TravelProtection, AssignedContent
from ..constants import spkcgraph
from ..serializing import paginated_contents, serialize_stream
from ..helpers import add_property


class ComponentPublicIndex(ListView):
    model = UserComponent
    is_home = False
    allowed_GET_parameters = set(["protection", "raw"])

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs["is_public_view"] = True
        kwargs["hostpart"] = "{}://{}".format(
            self.request.scheme, self.request.get_host()
        )

        GET = self.request.GET.copy()
        # parameters preserved in search
        for key in list(GET.keys()):
            if key not in self.allowed_GET_parameters:
                GET.pop(key, None)
        kwargs["spider_GET"] = GET
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        searchq = models.Q()
        searchq_exc = models.Q()
        infoq = models.Q()
        infoq_exc = models.Q()
        counter = 0
        max_counter = 30  # against ddos
        if "search" in self.request.POST or "info" in self.request.POST:
            searchlist = self.request.POST.getlist("search")
            infolist = self.request.POST.getlist("info")
        else:
            searchlist = self.request.GET.getlist("search")
            infolist = self.request.GET.getlist("info")

        for item in searchlist:
            if counter > max_counter:
                break
            counter += 1
            if len(item) == 0:
                continue
            if item.startswith("!!"):
                _item = item[1:]
            elif item.startswith("!"):
                _item = item[1:]
            else:
                _item = item
            qob = models.Q(
                contents__info__icontains="%s" % _item
            )
            qob |= models.Q(
                description__icontains="%s" % _item
            )
            qob |= models.Q(
                name__icontains="%s" % _item
            )
            if item.startswith("!!"):
                searchq |= qob
            elif item.startswith("!"):
                searchq_exc |= qob
            else:
                searchq |= qob

        for item in infolist:
            if counter > max_counter:
                break
            counter += 1
            if len(item) == 0:
                continue
            if item.startswith("!!"):
                infoq |= models.Q(contents__info__contains="\n%s\n" % item[1:])
            elif item.startswith("!"):
                infoq_exc |= models.Q(
                    contents__info__contains="\n%s\n" % item[1:]
                )
            else:
                infoq |= models.Q(contents__info__contains="\n%s\n" % item)
        if self.request.GET.get("protection", "") == "false":
            searchq &= models.Q(required_passes=0)

        q = models.Q(public=True)
        if self.is_home:
            q &= models.Q(featured=True)
        main_query = self.model.objects.prefetch_related(
            "contents"
        ).filter(
            q & searchq & ~searchq_exc & infoq & ~infoq_exc
        ).order_by(*self.get_ordering()).distinct()
        return main_query

    def get_paginate_by(self, queryset):
        return getattr(settings, "COMPONENTS_PER_PAGE", 25)

    def get_ordering(self):
        if self.is_home:
            return ("modified",)
        else:
            return ("user", "name")

    def render_to_response(self, context):
        # NEVER: allow embedding, things get too big
        if self.request.GET.get("raw", "") != "true":
            return super().render_to_response(context)
        meta_ref = URIRef(context["hostpart"] + self.request.path)
        g = Graph()
        g.namespace_manager.bind("spkc", spkcgraph, replace=True)
        g.add((meta_ref, spkcgraph["scope"], Literal("list")))
        g.add((
            meta_ref, spkcgraph["strength"], Literal(0)
        ))
        for component in context["object_list"]:
            url = urljoin(
                context["hostpart"],
                component.get_absolute_url()
            )
            ref_component = URIRef(url)
            g.add(
                (
                    meta_ref, spkcgraph["components"], ref_component
                )
            )
            g.add((
                ref_component, spkcgraph["type"], Literal("Component")
            ))
            g.add((
                ref_component, spkcgraph["strength"],
                Literal(component.strength)
            ))
            add_property(
                g, "name", ref=ref_component, literal=component.__str__()
            )
            add_property(
                g, "description", ref=ref_component, ob=component
            )

        ret = HttpResponse(
            g.serialize(format="turtle"),
            content_type="text/turtle;charset=utf-8"
        )
        return ret


class ComponentIndex(UCTestMixin, ListView):
    model = UserComponent
    also_authenticated_users = True
    no_nonce_usercomponent = True
    scope = "list"

    user = None

    def dispatch(self, request, *args, **kwargs):
        self.user = self.get_user()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_ordering(self):
        # if self.scope != "export":
        #     return ("modified",)
        return ("id",)

    def get_context_data(self, **kwargs):
        kwargs["component_user"] = self.user
        kwargs["username"] = getattr(self.user, self.user.USERNAME_FIELD)
        kwargs["scope"] = self.scope
        kwargs["is_public_view"] = False
        return super().get_context_data(**kwargs)

    def test_func(self):
        if self.has_special_access(staff=True):
            return True
        return False

    def get_queryset(self):
        searchq = models.Q()
        searchq_exc = models.Q()
        infoq = models.Q()
        infoq_exc = models.Q()
        counter = 0
        # against ddos
        max_counter = getattr(settings, "MAX_SEARCH_PARAMETERS", 30)

        if "search" in self.request.POST or "info" in self.request.POST:
            searchlist = self.request.POST.getlist("search")
            infolist = self.request.POST.getlist("info")
        else:
            searchlist = self.request.GET.getlist("search")
            infolist = self.request.GET.getlist("info")

        for item in searchlist:
            if counter > max_counter:
                break
            counter += 1
            if len(item) == 0:
                continue
            if item.startswith("!!"):
                _item = item[1:]
            elif item.startswith("!"):
                _item = item[1:]
            else:
                _item = item
            qob = models.Q(
                contents__info__icontains="%s" % _item
            )
            qob |= models.Q(
                description__icontains="%s" % _item
            )
            qob |= models.Q(
                name__icontains="%s" % _item
            )
            if item.startswith("!!"):
                searchq |= qob
            elif item.startswith("!"):
                searchq_exc |= qob
            else:
                searchq |= qob

        for item in infolist:
            if counter > max_counter:
                break
            counter += 1
            if len(item) == 0:
                continue
            if item.startswith("!!"):
                infoq |= models.Q(contents__info__contains="\n%s\n" % item[1:])
            elif item.startswith("!"):
                infoq_exc |= models.Q(
                    contents__info__contains="\n%s\n" % item[1:]
                )
            else:
                infoq |= models.Q(contents__info__contains="\n%s\n" % item)
        if self.request.GET.get("protection", "") == "false":
            searchq &= models.Q(required_passes=0)
        searchq &= (
            infoq & ~searchq_exc & ~infoq_exc &
            models.Q(user=self.user)
        )

        # doesn't matter if it is same user, lazy
        travel = TravelProtection.objects.get_active()
        # remove all travel protected if user
        if self.request.user == self.user:
            searchq &= ~models.Q(
                travel_protected__in=travel
            )
            now = timezone.now()
            searchq &= ~(
                # exclude future events
                models.Q(
                    contents__modified__lte=now,
                    contents__info__contains="\ntype=TravelProtection\n"
                )
            )
        if self.request.session.get("is_fake", False):
            searchq &= ~models.Q(name="index")
        else:
            searchq &= ~models.Q(name="fake_index")

        return super().get_queryset().prefetch_related(
            'contents'
        ).filter(searchq).distinct()

    def get_usercomponent(self):
        ucname = "index"
        if self.request.session.get("is_fake", False):
            ucname = "fake_index"
        return get_object_or_404(
            UserComponent, user=self.user, name=ucname
        )

    def get_paginate_by(self, queryset):
        if self.scope == "export":
            return None
        return getattr(settings, "COMPONENTS_PER_PAGE", 25)

    def render_to_response(self, context):
        if self.scope != "export":
            return super().render_to_response(context)
        session_dict = {
            "request": self.request,
            "context": context,
            "scope": self.scope,
            "expires": None,
            "hostpart": context["hostpart"],
            "uc_namespace": spkcgraph["components"],
            "sourceref": URIRef(context["hostpart"] + self.request.path)
        }

        contents = AssignedContent.objects.filter(
            usercomponent__in=context["object_list"]
        )
        g = Graph()
        g.namespace_manager.bind("spkc", spkcgraph, replace=True)
        p = paginated_contents(
            contents,
            getattr(settings, "SERIALIZED_PER_PAGE", 50),
            getattr(settings, "SERIALIZED_MAX_DEPTH", 20)
        )
        page = 1
        try:
            page = int(self.request.GET.get("page", "1"))
        except Exception:
            pass
        if page <= 1:
            g.add((
                session_dict["sourceref"],
                spkcgraph["scope"],
                Literal(context["scope"])
            ))
            g.add((
                session_dict["sourceref"], spkcgraph["strength"],
                Literal(10)
            ))

        serialize_stream(
            g, p, session_dict,
            page=page,
            embed=True
        )

        ret = HttpResponse(
            g.serialize(format="turtle"),
            content_type="text/turtle;charset=utf-8"
        )
        return ret


class ComponentCreate(UserTestMixin, CreateView):
    model = UserComponent
    form_class = UserComponentForm
    also_authenticated_users = True
    no_nonce_usercomponent = True

    def get_success_url(self):
        return reverse(
            "spider_base:ucomponent-update", kwargs={
                "name": self.object.name,
                "nonce": self.object.nonce
            }
        )

    def get_usercomponent(self):
        query = {}
        if self.request.session.get("is_fake", False):
            query["name"] = "fake_index"
        else:
            query["name"] = "index"
        query["user"] = self.get_user()
        return get_object_or_404(UserComponent, **query)

    def get_context_data(self, **kwargs):
        kwargs["available"] = installed_contents.keys()
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        ret = super().get_form_kwargs()
        ret["instance"] = self.model(user=self.get_user())
        ret['request'] = self.request
        return ret


class ComponentUpdate(UserTestMixin, UpdateView):
    model = UserComponent
    form_class = UserComponentForm
    also_authenticated_users = True

    def get_context_data(self, **kwargs):
        # for create_admin_token
        self.usercomponent = self.object
        self.request.auth_token = self.create_admin_token()
        context = super().get_context_data(**kwargs)
        context["content_variants"] = (
            self.object.user_info.allowed_content.all()
        )
        context["remotelink"] = context["spider_GET"].copy()
        context["remotelink"] = "{}{}?{}".format(
            context["hostpart"],
            reverse("spider_base:ucontent-list", kwargs={
                "id": self.usercomponent.id,
                "nonce": self.usercomponent.nonce
            }),
            context["remotelink"].urlencode()
        )
        # this is always available
        context["auth_token"] = self.request.auth_token.token
        return context

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(
            queryset.prefetch_related(
                "protections",
            ),
            user=self.get_user(), name=self.kwargs["name"],
            nonce=self.kwargs["nonce"]
        )

    def get_form_kwargs(self):
        ret = super().get_form_kwargs()
        ret['request'] = self.request
        return ret

    def get_form_success_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        return {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
            'instance': self.object,
            'request': self.request
        }

    def form_valid(self, form):
        self.object = form.save()
        if (
            self.kwargs["nonce"] != self.object.nonce or
            self.kwargs["name"] != self.object.name
        ):
            return redirect(
                "spider_base:ucomponent-update",
                name=self.object.name,
                nonce=self.object.nonce
            )
        return self.render_to_response(
            self.get_context_data(
                form=self.get_form_class()(**self.get_form_success_kwargs())
            )
        )


class ComponentDelete(UserTestMixin, DeleteView):
    model = UserComponent
    fields = []
    object = None
    http_method_names = ['get', 'post', 'delete']

    def dispatch(self, request, *args, **kwargs):
        self.user = self.get_user()
        self.object = self.get_object()
        self.usercomponent = self.object
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        username = getattr(self.user, self.user.USERNAME_FIELD)
        return reverse(
            "spider_base:ucomponent-list", kwargs={
                "user": username
            }
        )

    def get_required_timedelta(self):
        # TODO: needs better design
        _time = getattr(
            settings, "DELETION_PERIODS_COMPONENTS", {}
        ).get(self.object.name, None)
        if _time:
            _time = timedelta(seconds=_time)
        else:
            _time = timedelta(seconds=0)
        return _time

    def get_context_data(self, **kwargs):
        kwargs["uc"] = self.usercomponent
        _time = self.get_required_timedelta()
        if _time and self.object.deletion_requested:
            now = timezone.now()
            if self.object.deletion_requested + _time >= now:
                kwargs["remaining"] = timedelta(seconds=0)
            else:
                kwargs["remaining"] = self.object.deletion_requested+_time-now
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        # hack for compatibility to ContentRemove
        if getattr(self.object, "name", "") in index_names:
            return self.handle_no_permission()
        _time = self.get_required_timedelta()
        if _time:
            now = timezone.now()
            if self.object.deletion_requested:
                if self.object.deletion_requested+_time >= now:
                    return self.get(request, *args, **kwargs)
            else:
                self.object.deletion_requested = now
                self.object.save()
                return self.get(request, *args, **kwargs)
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        # because forms are screwed (delete not possible)
        if request.POST.get("action") == "reset":
            return self.reset(request, *args, **kwargs)
        elif request.POST.get("action") == "delete":
            return self.delete(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def reset(self, request, *args, **kwargs):
        self.object.deletion_requested = None
        self.object.save(update_fields=["deletion_requested"])
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(
            queryset, user=self.user, name=self.kwargs["name"],
            nonce=self.kwargs["nonce"]
        )
