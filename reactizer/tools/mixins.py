class ModelMixin():
    """adds methods all Base classes should have"""
    def __iter__(self):
        for column in self.__table__.columns:
            yield (column.name, getattr(self, column.name))

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        return setattr(self, key, value)
