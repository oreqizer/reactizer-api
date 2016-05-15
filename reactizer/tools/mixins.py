class ModelMixin(object):
    """adds methods all Base classes should have"""
    def __iter__(self):
        for column in self.__table__.columns:  # NOQA
            yield (column.name, getattr(self, column.name))

    def __getitem__(self, item):
        return dict(self)[item]
