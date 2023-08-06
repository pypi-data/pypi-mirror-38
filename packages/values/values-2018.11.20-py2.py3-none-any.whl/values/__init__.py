#!/usr/bin/env python
import public
import this_is


@public.add
def get(input):
    """return list with input values or [] if input is None"""
    if input is None:
        return []
    if not this_is.iterable(input) or this_is.string(input):
        return [input]
    return list(input)
