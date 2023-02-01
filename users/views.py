from django.shortcuts import redirect


def test(request):
    return redirect("https://github.com/login/oauth/authorize")
