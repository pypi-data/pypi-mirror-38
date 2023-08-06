from django.views.generic.base import RedirectView
from django.core.exceptions import SuspiciousOperation
from pony_indice.models import Link
from pony_indice import settings


class IncrementRankView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        url = self.request.GET.get('url')
        if not url:
            msg = "You must specify an URL."
            raise SuspiciousOperation(msg)
        link = Link.objects.filter(url=url).first()
        if link is not None:
            link.rank += settings.DEFAULT_RANK_INCREMENT
            link.save()
        return url
