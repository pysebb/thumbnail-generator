from django.db import models
from django.urls import reverse


class Video(models.Model):
    NEW = "new"
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"
    POSTPONED = "postponed"
    CANCELED = "canceled"
    FAILED = "failed"

    CHOICES = (
        (NEW, "NEW"),
        (PENDING, "PENDING"),
        (IN_PROGRESS, "IN PROGRESS"),
        (FINISHED, "FINISHED"),
        (POSTPONED, "POSTPONED"),
        (CANCELED, "CANCELED"),
        (FAILED, "FAILED")
    )

    video = models.FileField(upload_to="files", max_length=255)
    finished = models.BooleanField("Processing finished", help_text="Only for task purposes", default=False)
    thumbnail = models.ImageField("Thumbnail", upload_to="files", blank=True, null=True)
    status = models.CharField("Status", choices=CHOICES, max_length=50, default=NEW)
    threshold = models.PositiveIntegerField(default=15)
    limit = models.PositiveIntegerField(default=50)

    def __str__(self):
        return f"{self.video.name}"

    def get_absolute_url(self):
        return reverse("video-view", args=[self.id])

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"
