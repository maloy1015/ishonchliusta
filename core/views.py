from django.shortcuts import render, redirect


def splash_view(request):
    if request.session.get("splash_shown"):
        if request.user.is_authenticated:
            return redirect("accounts:dashboard")
        return redirect("accounts:login")

    request.session["splash_shown"] = True
    next_url = "accounts:dashboard" if request.user.is_authenticated else "accounts:login"
    return render(request, "core/splash.html", {"next_url_name": next_url})
