from pony_indice import signals


class Registry(dict):
    def register(self, model_class, name=None):
        key = name or '%s.%s' % (model_class._meta.app_label,
                                 model_class._meta.model_name)
        self[key] = model_class
        for signal, receiver, uid in signals.DJANGO_DB_SIGNALS:
            dispatch_uid = '%s_%s' % (key.replace('.', '_'), uid)
            signal.connect(receiver, sender=model_class,
                           dispatch_uid=dispatch_uid)

    @property
    def models(self):
        return list(self.values())

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


def register():
    """
    Decorator to register a `Model` class.
    """
    def _model_wrapper(model_class, name=None):
        registry.register(model_class, name)
        return model_class
    return _model_wrapper
