from django.shortcuts import render, redirect

from profiles.forms import ProfileForm
from profiles.models import Profile


def get_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            Profile.objects.update(
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                patronymic=form.cleaned_data["patronymic"],
                phone_number=form.cleaned_data["phone_number"],
                social_network_link=form.cleaned_data["social_network_link"],
                slug=form.cleaned_data["slug"]
            )

        response = redirect("profile")

    else:
        profile = Profile.objects.get(user=request.user)
        data = {"first_name": profile.first_name,
                "last_name": profile.last_name,
                "patronymic": profile.patronymic,
                "phone_number": profile.phone_number,
                "social_network_link": profile.social_network_link,
                "slug": profile.slug,
                }
        form = ProfileForm(data)
        response = render(request, "profile.html", {"form": form})

    return response
