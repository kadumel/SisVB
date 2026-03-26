from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Acesso, Link


def _links_for_user(user):
    groups = user.groups.all()
    if not groups.exists():
        return Link.objects.none()
    return (
        Link.objects.filter(acesso__group__in=groups)
        .distinct()
        .order_by("desc")
    )


@login_required
def indexLinks(request):
    links = _links_for_user(request.user)
    return render(
        request,
        "link/index.html",
        {
            "links": links,
            "grupos": request.user.groups.all(),
        },
    )


@login_required
def painel(request, id):
    link = get_object_or_404(Link, pk=id)
    allowed = Acesso.objects.filter(
        link=link,
        group__in=request.user.groups.all(),
    ).exists()
    if not allowed:
        return render(request, "link/forbidden.html", status=403)
    return render(request, "link/painel.html", {"frame": link})
