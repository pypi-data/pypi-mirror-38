from django.db import models


class LinkQuerySet(models.QuerySet):
    def filter_q(self, q):
        return self.filter(
            models.Q(display__icontains=q) |
            models.Q(description__icontains=q)
        )
