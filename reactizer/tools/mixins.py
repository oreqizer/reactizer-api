class DictMixin(object):
    """allows serializing as a dict"""
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
