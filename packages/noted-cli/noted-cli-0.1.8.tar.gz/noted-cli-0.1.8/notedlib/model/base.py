class Base:
    def __str__(self):
        data = str(self.__dict__)

        if len(data) > 60:
            data = data[:60] + '...}'

        return '<%s %s>' % (self.__class__.__name__, data)

    def populate(self, data):
        """Populate data from a dictionary."""
        for key in data:
            if hasattr(self, key):
                setattr(self, key, data[key])

        return self

    def to_raw(self):
        return {}
