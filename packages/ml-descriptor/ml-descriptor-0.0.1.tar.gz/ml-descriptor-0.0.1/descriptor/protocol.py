import json
import torch
import os

from typing import Any, Optional, Callable
from collections import OrderedDict, defaultdict

from .core import traverse

ENCODE_TYPES = ['json', 'pth']

def json_encoder(path: str, obj: Any):
    with open(path, "w") as f:
        json.dump(obj, f, indent=4)

def json_decoder(path: str):
    with open(path, "r") as f:
        return json.load(f)

def pytorch_encoder(path: str, obj: Any):
    torch.save(obj, path)

def pytorch_decoder(path: str):
    return torch.load(path)

def decode(obj, root_path=""):
    if type(obj) == str:
        if obj.endswith(".json"):
            return json_decoder(os.path.join(root_path, obj))
        if obj.endswith(".pth"):
            return pytorch_decoder(os.path.join(root_path, obj))
    return obj

def encode(obj, root_path="", force_path=""):
    if type(obj) == dict or type(obj) == OrderedDict or type(obj) == defaultdict:
        # print("encoding: {} - type: {}".format(obj, type(obj)))
        new_obj = type(obj)()
        for key in obj:
            if type(key) == str and "$" in key and type(obj[key]) != str:
                signatures = key.split("$")
                assert len(signatures) == 3, "the signature \"{}\" is ill-formed".format(key)
                _, typ, name = signatures

                assert typ in ['json', 'pth'], "the type \"{}\" is not defined".format(typ)

                if typ == 'json':
                    json_encoder(os.path.join(root_path, name + ".json"), obj[key])
                    new_obj[key] = name + ".json"
                elif typ == "pth":
                    pytorch_encoder(os.path.join(root_path, name + ".pth"), obj[key])
                    new_obj[key] = name + ".pth"
            else:
                new_obj[key] = obj[key]
        obj = new_obj
    return obj

def describe(file_path: str, mutable: bool=True, encapsulate_integral: bool=False):
    basename = os.path.basename(file_path)
    name = ".".join(basename.split(".")[:-1])
    ext = basename.split(".")[-1]
    d = Descriptor({"${}${}".format(ext, name): basename}, os.path.dirname(file_path), mutable, encapsulate_integral)
    d.initialize()
    return d

class Descriptor(object):
    _data: Any
    _decoded_data: Any
    _root_dir: str
    _mutable: bool
    _encapsulate_integral: bool
    _decoded_setter: Optional[Callable]
    _parent: Optional['Descriptor']
    def __init__(self, data: Any, root_dir: str, mutable: bool, encapsulate_integral: bool, 
        parent: Optional['Descriptor']=None, decoded_setter: Optional[Callable]=None):
        self._data = data
        self._decoded_data = None
        self._decoded_setter = decoded_setter
        self._root_dir = root_dir
        self._mutable = mutable
        self._encapsulate_integral = encapsulate_integral
        self._parent = parent

    @property
    def parent(self) -> Optional['Descriptor']:
        return self._parent

    def update(self):
        assert self._decoded_data is not None
        self._data = encode(self._decoded_data, self._root_dir)
        if self._decoded_setter is not None: self._decoded_setter(self._data)
        print("update {} to {} => {}".format(self._decoded_data, self, self._data))

    def flush(self):
        return traverse(self._data, pre_fn=lambda x: decode(x, self._root_dir), in_place=False)

    def override(self, data):
        self._data = data
        self.initialize()

    def initialize(self):
        self._data = traverse(self._data, post_fn=lambda x: encode(x, self._root_dir))

    def _new(self, data, mutable, decoded_setter=None):
        return Descriptor(data, self._root_dir, mutable, self._encapsulate_integral, self, decoded_setter)

    def _find_item(self, obj, item):
        assert "$" not in item, "the key \"{}\" is illegal (cannot contain $)".format(item)
        if item in obj: return item
        global ENCODE_TYPES
        for typ in ENCODE_TYPES:
            new_item = "${}${}".format(typ, item)
            if new_item in obj:
                return new_item
        raise KeyError

    def _get_item_impl(self, item):
        self._decoded_data = decode(self._data, self._root_dir)
        if self._decoded_setter is not None: 
            self._decoded_setter(self._decoded_data)
        print("decode {} => {}".format(self._data, self._decoded_data))
        print("find: {} in {} => ?".format(item, self._decoded_data))
        corrected_item = self._find_item(self._decoded_data, item)
        print("find: {} in {} => {}".format(item, self._decoded_data, corrected_item))
        return_item = self._decoded_data[corrected_item]
        if not self._encapsulate_integral and type(return_item) in [int, bool, None, float] or \
            (type(return_item) == str and "." not in return_item):  
            return return_item
        def setter(x):
            self._decoded_data[corrected_item] = x
        return self._new(return_item, self._mutable, setter)

    def _set_item_impl(self, item, value):
        assert self._mutable, "the descriptor is not mutable"
        self._decoded_data = decode(self._data, self._root_dir)
        self._decoded_data[self._find_item(self._decoded_data, item)] = value
        curr = self
        while curr is not None:  # update all the descriptor along the way to compensate the change
            curr.update()
            curr = curr.parent

    def _is_private(self, attr):
        return True if attr[0] == '_' else False

    def __getitem__(self, item): 
        if self._parent is None: return self._get_item_impl("main")[item]
        return self._get_item_impl(item)
    def __setitem__(self, item, value): self._set_item_impl(item, value)
    def __getattr__(self, item): 
        return self[item]
    def __setattr__(self, item, value):
        if self._is_private(item): super().__setattr__(item, value)
        else: self[item] = value

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return "Descriptor(\n" + "\n  ".join(str(self).split("\n")) + "\n)"
