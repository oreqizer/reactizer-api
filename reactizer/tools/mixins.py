class ModelMixin(object):
    """adds various methods all Base classes should have"""
    def __iter__(self):
        for column in self.__table__.columns:  # NOQA
            yield (column.name, getattr(self, column.name))
