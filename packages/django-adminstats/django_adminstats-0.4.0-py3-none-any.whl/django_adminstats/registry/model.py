from . import Registration


class ModelRegistration(Registration):

    def __init__(self, model):
        self.model = model
        self.meta = getattr(self.model, '_meta')

    def get_queryset(self):
        return self.model.objects

    @property
    def key(self):
        return '{}.{}'.format(self.meta.app_label, self.meta.model_name)

    @property
    def label(self):
        return self.meta.verbose_name_plural.title()

    def _filter(self, cls):
        """Given an individual filter token and a model, find the next model"""
        # first check if _meta (model)
        meta = getattr(cls, '_meta', None)
        if meta is not None:
            ff = getattr(meta, '_forward_fields_map', None)
            if ff is not None:
                return ff
            return dict((f.name, f) for f in meta.fields)
        # check if it's a ForeignKey or something
        related = getattr(cls, 'related_model', None)
        if related is not None:
            return self._filter(related)
        raise NotImplementedError

    def filter_options(self, text: str = '') -> set:
        """Given a filter string, return the next options"""
        cls = self.model
        options = self._filter(cls)
        for part in text.split('__'):
            if part in options:
                cls = options[part]
            options = self._filter(cls)
        return set(options.keys())
