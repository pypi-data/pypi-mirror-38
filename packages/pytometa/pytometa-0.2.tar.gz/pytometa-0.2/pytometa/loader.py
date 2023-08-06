import typing

from pytometa import tools
from pytometa.descriptors import FieldDescriptor

_T = typing.TypeVar('T')

def allowed_field_name(name:str):
    return not name.startswith('_')

def load_field(obj, dic, meta: FieldDescriptor):
    setattr(obj, meta.name, meta.load_function(dic))

def load_from_dict(dic, obj: _T) -> _T:
    assert obj, "object is empty"
    fields = tools.getAllFieldItems(obj.__class__)
    for k in fields:
        name = k[0]
        metaInfo = k[1]
        if isinstance(metaInfo, FieldDescriptor):
            if not metaInfo.name:
                metaInfo.name = name
            load_field(obj, dic, metaInfo)
        elif allowed_field_name(name) and isinstance(metaInfo, type):
            # set primitive
            val = metaInfo(dic[name])
            setattr(obj, name, val)

    return obj
