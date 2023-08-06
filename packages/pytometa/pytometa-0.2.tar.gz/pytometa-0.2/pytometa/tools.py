

def getAllFields(cls):
    items = cls.__dict__.items()
    return [k[0] for k in items]

def getAllFieldItems(cls):
    items = cls.__dict__.items()
    return [(k[0], k[1]) for k in items]

_ALLOWED_TYPES=[int, str, bool, float]
def is_primitive_type(value):
    if not isinstance(value, type):
        value = type(value)
    return value in _ALLOWED_TYPES

def create_instance(typ):
    from pytometa.descriptors import TypeDescriptor
    if isinstance(typ, TypeDescriptor):
        return typ.new_instance(typ)

    return typ()