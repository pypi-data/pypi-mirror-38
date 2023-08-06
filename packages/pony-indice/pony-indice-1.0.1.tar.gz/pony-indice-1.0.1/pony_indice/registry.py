from pony_indice import signals


class Registry(dict):
    def get_model_key(self, model_class):
        key = '%s.%s' % (model_class._meta.app_label,
                         model_class._meta.model_name)
        return key

    def register_model(self, model_class, get_absolute_url=None,
                       get_display=None, get_description=None,
                       get_tags=None, get_rank=None, skip=None):
        key = self.get_model_key(model_class)
        self[key] = {
            'class': model_class,
            'url': get_absolute_url,
            'display': get_display,
            'description': get_description,
            'tags': get_tags,
            'rank': get_rank,
            'skip': skip,
        }
        for signal, receiver, uid in signals.DJANGO_DB_SIGNALS:
            dispatch_uid = '%s_%s' % (key.replace('.', '_'), uid)
            signal.connect(receiver, sender=model_class,
                           dispatch_uid=dispatch_uid)

    @property
    def models(self):
        return [i['class'] for i in self.values()]

    def get_model_options(self, model_class):
        key = self.get_model_key(model_class)
        return self[key]

    def clear_model(self, model_class):
        """
        Remove model from registery.
        """
        key = '%s.%s' % (model_class._meta.app_label,
                         model_class._meta.model_name)
        for signal, receiver, uid in signals.DJANGO_DB_SIGNALS:
            dispatch_uid = '%s_%s' % (key.replace('.', '_'), uid)
            signal.disconnect(receiver, sender=model_class,
                              dispatch_uid=dispatch_uid)

    def clear(self):
        """
        Remove all stuff from registery.
        """
        for model_class in self.models:
            self.clear_model(model_class)
        super().clear()


registry = Registry()


def register_model(get_absolute_url=None, get_display=None, get_description=None,
                   get_tags=None, get_rank=None, skip=None):
    """
    Decorator to register a `Model` class.

    :param get_absolute_url: Callable or string representing method on model.
    """
    def _model_wrapper(model_class):
        registry.register_model(
            model_class=model_class,
            get_absolute_url=get_absolute_url,
            get_display=get_display,
            get_description=get_description,
            get_tags=get_tags,
            get_rank=get_rank,
            skip=skip)
        return model_class
    return _model_wrapper
