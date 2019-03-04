import uuid

from flask_restful.fields import Raw, MarshallingException


class UUID(Raw):
    def format(self, value):
        try:
            if value is None:
                return self.default
            return str(uuid.UUID(value))
        except ValueError as ve:
            raise MarshallingException(ve)


def uuid_param(value, name):
    try:
        return str(uuid.UUID(value))
    except ValueError:
        raise ValueError("The parameter '{}' is not uuid. You gave us the value: {}".format(name, value))
