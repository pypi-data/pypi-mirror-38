"""
JSON-Doc

@author: Fatih Piristine <fatihpiristine () gmail dot com>
@license: Apache License 2
"""

import re

try:
    from collections.abc import Mapping, Sequence
except ImportError:
    from collections import Mapping, Sequence


def validate_pointer(pointer):
    """
    Validate pointer
    :param pointer:
    :return:
    """

    _re_escape = re.compile('(~[^01]|~$)')

    invalid_escape = _re_escape.search(pointer)
    if invalid_escape:
        raise Exception('Invalid escape {}'.format(invalid_escape.group()))

    parts = pointer.split('/')

    if parts.pop(0) != '':
        raise Exception('Pointer must start with /')

    parts = [part.replace('~', '~0').replace('/', '~1') for part in parts]

    if not parts:
        raise Exception('Invalid pointer: %s' % pointer)

    return parts, parts[-1]


def json_doc_get(doc, pointer, default=None):
    """
    Gets value of given pointer. Default: None
    :param doc:
    :param pointer:
    :param default:
    :return:
    """

    ref = doc
    parts, last = validate_pointer(pointer)

    # walk
    _return = default
    for part in parts[:-1]:
        if isinstance(ref, Mapping) and part in ref:
            ref = ref[part]
        elif isinstance(ref, Sequence) and part.isdigit():
            try:
                ref = ref[int(part)]
            except IndexError:
                return _return
        else:
            return _return

    # last
    if isinstance(ref, Mapping) and last in ref:
        _return = ref[last]
    elif isinstance(ref, Sequence) and last.isdigit():
        try:
            _return = ref[int(last)]
        except IndexError:
            pass
    return _return


def json_doc_set(doc, pointer, value=None):
    """
    Sets value of given pointer
    :param doc:
    :param pointer:
    :param value:
    :return: bool
    """

    ref = doc
    parts, last = validate_pointer(pointer)

    # walk
    for part in parts[:-1]:
        if isinstance(ref, Mapping):
            if part not in ref:
                ref[part] = {}
            ref = ref[part]
        elif isinstance(ref, Sequence) and part.isdigit():
            ref = ref[int(part)]
        else:
            raise Exception('Invalid document')

    # last
    if isinstance(ref, Mapping):
        ref[last] = value
    elif isinstance(ref, Sequence) and last.isdigit():
        ref[int(last)] = value
    else:
        raise Exception('Invalid document')

    return doc


def json_doc_has(doc, pointer, value=None):
    """
    Checks given pointer exists.
    If value is defined, checks that values are equal
    :param doc:
    :param pointer:
    :param value:
    :return: bool
    """

    ref = doc
    parts, last = validate_pointer(pointer)

    # walk
    _return = False
    for part in parts[:-1]:
        if isinstance(ref, Mapping) and part in ref:
            ref = ref[part]
        elif isinstance(ref, Sequence) and part.isdigit():
            try:
                ref = ref[int(part)]
            except IndexError:
                return _return
        else:
            return _return

    # last
    if isinstance(ref, Mapping) and last in ref:
        # test if value in list
        if value and isinstance(ref[last], Sequence):
            ref = ref[last]
            _return = value in ref
        elif value and isinstance(ref[last], Mapping):
            _return = value == ref[last]
        else:
            # last one is dict and key is already there
            _return = True
    elif isinstance(ref, Sequence) and last.isdigit():
        try:
            assert ref[int(last)]
            _return = True
        except IndexError:
            _return = False
    else:
        _return = False

    return _return


def json_doc_pop(doc, pointer):
    """
    Unset or pop node at given pointer
    :param doc:
    :param pointer:
    :return: bool
    """

    ref = doc
    parts, last = validate_pointer(pointer)

    # walk
    _return = False
    for part in parts[:-1]:
        if isinstance(ref, Mapping) and part in ref:
            ref = ref[part]
        elif isinstance(ref, Sequence) and part.isdigit():
            try:
                ref = ref[int(part)]
            except IndexError:
                return _return
        else:
            raise Exception("Invalid document")

    # last
    if isinstance(ref, Mapping) and last in ref:
        del ref[last]
        _return = True
    elif isinstance(ref, Sequence) and last.isdigit():
        try:
            del ref[int(last)]
            _return = True
        except IndexError:
            pass

    return _return


def json_doc_append(doc, pointer, value=None):
    """
    Append given value to list at pointer
    :param doc:
    :param pointer:
    :param value:
    :return:
    """

    ref = doc
    parts, last = validate_pointer(pointer)

    # walk
    for part in parts[:-1]:
        if isinstance(ref, Mapping):
            if part not in ref:
                ref[part] = {}
            ref = ref[part]
        elif isinstance(ref, Sequence) and part.isdigit():
            ref = ref[int(part)]
        else:
            raise Exception('Invalid document')

    # last
    if isinstance(ref, Mapping) and last in ref \
            and isinstance(ref[last], Sequence):
        ref[last].append(value)
    elif isinstance(ref, Sequence):
        pass
    else:
        raise Exception('Invalid document')

    return doc


def json_doc_extend(doc, pointer, value=None):
    """
    Extend list at given pointer
    :param doc:
    :param pointer:
    :param value:
    :return:
    """

    ref = doc
    parts, last = validate_pointer(pointer)

    # walk
    for part in parts[:-1]:
        if isinstance(ref, Mapping):
            if part not in ref:
                ref[part] = {}
            ref = ref[part]
        elif isinstance(ref, Sequence) and part.isdigit():
            ref = ref[int(part)]
        else:
            raise Exception('Invalid document')

    # last
    if isinstance(ref, Mapping) and last in ref \
            and isinstance(ref[last], Sequence):
        ref[last].extend(value)
    elif isinstance(ref, Sequence):
        pass
    else:
        raise Exception('Invalid document')

    return doc


def json_doc_replace(doc, pointer, value=None, search=None):
    """
    Search and replace list element while iterating through the list
    and keep its index.
    :param doc:
    :param pointer:
    :param value:
    :param search:
    :return:
    """

    ref = doc
    parts, last = validate_pointer(pointer)

    # walk
    for part in parts[:-1]:
        if isinstance(ref, Mapping):
            if part not in ref:
                ref[part] = {}
            ref = ref[part]
        elif isinstance(ref, Sequence) and part.isdigit():
            ref = ref[int(part)]
        else:
            raise Exception('Invalid document')

    # last
    if isinstance(ref, Mapping) and last in ref \
            and isinstance(ref[last], Sequence):
        # replace any list element that matches
        for search_k, search_v in enumerate(ref[last]):
            if search == search_v:
                ref[last][search_k] = value
    elif isinstance(ref, Sequence):
        pass
    else:
        raise Exception('Invalid document')

    return doc


def json_doc_replace_re(doc, pointer, value=None, search=None):
    """
    Search using regular expression and replace list element while
    iterating through the list and keep its index.
    :param doc:
    :param pointer:
    :param value:
    :param search:
    :return:
    """

    ref = doc
    parts, last = validate_pointer(pointer)

    # walk
    for part in parts[:-1]:
        if isinstance(ref, Mapping):
            if part not in ref:
                ref[part] = {}
            ref = ref[part]
        elif isinstance(ref, Sequence) and part.isdigit():
            ref = ref[int(part)]
        else:
            raise Exception('Invalid document')

    # last
    if isinstance(ref, Mapping) and last in ref \
            and isinstance(ref[last], Sequence):
        # replace any list element matches to regex
        search_re = re.compile(search)
        for search_k, search_v in enumerate(ref[last]):
            if search_re.match(str(search_v)):
                ref[last][search_k] = value
    elif isinstance(ref, Sequence):
        pass
    else:
        raise Exception('Invalid document')

    return doc
