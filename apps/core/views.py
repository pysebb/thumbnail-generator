from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from .forms import FileForm, GeneratorForm
from .models import Video
from .tasks import generate_thumbnail
# from .tasks import


class IndexView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FileForm()
        context["videos"] = Video.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        form = FileForm(request.POST, request.FILES)

        if form.is_valid():
            video = form.save()

            return redirect(
                reverse("video-view", args=[video.id])
            )

        return super(TemplateView, self).render_to_response(context)


class VideoView(TemplateView):
    template_name = "core/video_detail.html"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {
                "object": get_object_or_404(Video, pk=kwargs.get("pk")),
                "form": GeneratorForm(initial={"threshold": 15, "limit": 50})
            }
        )

    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Video, pk=kwargs.get("pk"))

        form = GeneratorForm(request.POST)
        if form.is_valid():
            generate_thumbnail(obj.id, form.cleaned_data["threshold"], form.cleaned_data["limit"])
            return redirect(obj.get_absolute_url())
        return render(
            request,
            self.template_name,
            {
                "object": obj,
                "form": form
            }
        )
