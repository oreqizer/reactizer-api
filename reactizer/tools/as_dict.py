def as_dict(cls):
    """allows serializing as a dict"""
    def fn(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    setattr(cls, 'as_dict', fn)
    return cls
