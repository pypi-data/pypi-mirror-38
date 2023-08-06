from django.conf import settings


def get_setting(name, default=None):
    key = 'INDICE_%s' % name
    value = getattr(settings, key, default)
    return value

DEFAULT_RANK = get_setting('DEFAULT_RANK', 10)
DEFAULT_RANK_INCREMENT = 1
DEFAULT_ORDER_BY = get_setting('DEFAULT_RANK',
                               ('-rank', 'display'))
AUTO_UPDATE_TAGS = get_setting('AUTO_UPDATE_TAGS', True)
FILTER_FUNC_PATH = get_setting('FILTER_FUNC_PATH',
                               'pony_indice.querysets.default_filter_q')
