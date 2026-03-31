from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_http_methods


def _safe_next_url(request, candidate: str) -> str:
    if (
        candidate
        and url_has_allowed_host_and_scheme(
            candidate,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        )
    ):
        return candidate
    return ""


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect("links:indexLinks")

    raw_next = request.POST.get("next") or request.GET.get("next") or ""
    next_url = _safe_next_url(request, raw_next)

    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next_url:
                return redirect(next_url)
            return redirect("links:indexLinks")
        messages.error(request, "Usuário ou senha inválidos.")

    return render(request, "gestao/login.html", {"next": next_url})


@require_http_methods(["GET", "POST"])
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
@require_http_methods(["GET", "POST"])
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Senha alterada com sucesso.")
            return redirect("links:indexLinks")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, "gestao/change_password.html", {"form": form})

