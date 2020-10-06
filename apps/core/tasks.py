import cv2
import numpy as np
import os

from celery import shared_task

from .models import Video


@shared_task
def generate_thumbnail(video_id, threshold=15, limit=40):
    try:
        video = Video.objects.get(id=video_id)
        video.status = Video.IN_PROGRESS
        video.threshold = threshold
        video.limit = limit
        video.save()
    except Video.DoesNotExist:
        return

    cap = cv2.VideoCapture(video.video.path)
    filename, file_extension = os.path.splitext(video.video.name)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    try:
        p = total_frames // 10
        batch = [x for x in range(total_frames)[-p:]]
    except ZeroDivisionError:
        video.status = Video.FAILED
        video.save()
        return

    export_frame = None
    last_mean = 0
    indexes = []
    above_limit = []
    c = 0
    t = False

    cap.set(cv2.CAP_PROP_POS_FRAMES, batch[0])

    for index, batch_item in enumerate(batch):
        if not cap.isOpened():
            break

        ret, frame = cap.read()
        if not ret:
            break

        frame_mean = frame.mean()
        diff = frame_mean - last_mean

        if diff < 0 and np.abs(diff) >= threshold:
            indexes.append(batch_item)

        if frame_mean > limit:
            above_limit.append(batch_item)

        last_mean = frame_mean
        c += 1

    if indexes:
        cap.set(cv2.CAP_PROP_POS_FRAMES, indexes[0])
        t, export_frame = cap.read()

    if not t and above_limit:
        cap.set(cv2.CAP_PROP_POS_FRAMES, above_limit[-1])
        t, export_frame = cap.read()

    file_out_path = f"{video.video.path}".replace(file_extension, "_output.jpg")
    out_path = f"{video.video.name}".replace(file_extension, "_output.jpg")

    try:
        cv2.imwrite(file_out_path, export_frame)
        video.status = Video.FINISHED
        video.thumbnail = out_path
    except Exception:
        video.status = Video.FAILED

    video.save()
    return
