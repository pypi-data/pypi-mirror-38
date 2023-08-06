__metaclass__ = type


class EqualityComparableMixin:
    def __eq__(self, other):
        return (
            type(self) is type(other)
            and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self == other
