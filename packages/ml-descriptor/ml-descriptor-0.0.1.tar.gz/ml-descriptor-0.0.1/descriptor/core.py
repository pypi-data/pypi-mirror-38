from collections import OrderedDict, defaultdict
from typing import Any, Callable


def traverse(x: Any, pre_fn: Callable=None, post_fn: Callable=None, in_place: bool=False) -> Any:
    if pre_fn is not None: x = pre_fn(x)
    recur_fn = (lambda z: traverse(z, pre_fn, post_fn, in_place))
    if type(x) == dict or type(x) == OrderedDict or type(x) == defaultdict:
        if in_place:
            for key in x: 
                x[key] = recur_fn(x[key])
        else:
            x = {key: recur_fn(x[key]) for key in x}
    
    if type(x) == list:
        if in_place:
            for i in range(len(x)):
                x[i] = recur_fn(x[i])
        else:
            x = [recur_fn(element) for element in x]
    if post_fn is not None: x = post_fn(x)
    return x   
