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
    :return: mixed
    """

    ref = doc
    parts, last = validate_pointer(pointer)
    result = default

    # walk
    for part in parts[:-1]:
        if isinstance(ref, Mapping) and part in ref:
            ref = ref[part]
        elif isinstance(ref, Sequence) and part.isdigit():
            try:
                ref = ref[int(part)]
            except IndexError:
                return result
        else:
            # empty or invalid doc falls here
            return default

    # last
    if isinstance(ref, Mapping) and last in ref:
        result = ref[last]
    elif isinstance(ref, Sequence) and last.isdigit():
        try:
            result = ref[int(last)]
        except IndexError:
            pass
    return result


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
    changed = False

    # walk
    for part in parts[:-1]:
        if isinstance(ref, Mapping):
            if part not in ref:
                ref[part] = {}
                changed = True
            ref = ref[part]
        elif isinstance(ref, Sequence) and part.isdigit():
            ref = ref[int(part)]
        else:
            raise Exception('Invalid document')

    # last
    if isinstance(ref, Mapping):
        ref[last] = value
        changed = True
    elif isinstance(ref, Sequence) and last.isdigit():
        ref[int(last)] = value
        changed = True

    return changed


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
    result = False

    # walk
    for part in parts[:-1]:
        if isinstance(ref, Mapping) and part in ref:
            ref = ref[part]
        elif isinstance(ref, Sequence) and part.isdigit():
            try:
                ref = ref[int(part)]
            except IndexError:
                return False
        else:
            return False

    # last
    if isinstance(ref, Mapping) and last in ref:
        # test if value in list
        if value and isinstance(ref[last], Sequence):
            ref = ref[last]
            result = value in ref
        elif value and isinstance(ref[last], Mapping):
            result = value == ref[last]
        else:
            # last one is dict and key is already there
            result = True
    elif isinstance(ref, Sequence) and last.isdigit():
        try:
            assert ref[int(last)]
            # check index exists and compare with value if given
            result = value == ref[int(last)] if value else True
        except IndexError:
            result = False

    return result


def json_doc_pop(doc, pointer):
    """
    Unset or pop node at given pointer
    :param doc:
    :param pointer:
    :return: bool
    """

    ref = doc
    parts, last = validate_pointer(pointer)
    changed = False

    # walk
    for part in parts[:-1]:
        if isinstance(ref, Mapping) and part in ref:
            ref = ref[part]
        elif isinstance(ref, Sequence) and part.isdigit():
            try:
                ref = ref[int(part)]
            except IndexError:
                return False
        else:
            return False

    # last
    if isinstance(ref, Mapping) and last in ref:
        del ref[last]
        changed = True
    elif isinstance(ref, Sequence) and last.isdigit():
        try:
            del ref[int(last)]
            changed = True
        except IndexError:
            pass

    return changed


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
    changed = False

    # walk
    for part in parts[:-1]:
        if isinstance(ref, Mapping) and part in ref:
            ref = ref[part]
        elif isinstance(ref, Sequence) and part.isdigit():
            ref = ref[int(part)]
        else:
            return False

    # last
    if isinstance(ref, Mapping) and last in ref \
            and isinstance(ref[last], Sequence):
        ref[last].append(value)
        changed = True

    return changed


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
    changed = False

    # walk
    for part in parts[:-1]:
        if isinstance(ref, Mapping) and part in ref:
            ref = ref[part]
        elif isinstance(ref, Sequence) and part.isdigit():
            ref = ref[int(part)]
        else:
            return False

    # last
    if isinstance(ref, Mapping) and last in ref \
            and isinstance(ref[last], Sequence):
        ref[last].extend(value)
        changed = True

    return changed


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
    changed = False

    # walk
    for part in parts[:-1]:
        if isinstance(ref, Mapping) and part in ref:
            ref = ref[part]
        elif isinstance(ref, Sequence) and part.isdigit():
            ref = ref[int(part)]
        else:
            return False

    # last
    if isinstance(ref, Mapping) and last in ref \
            and isinstance(ref[last], Sequence):
        # replace any list element that matches
        for search_k, search_v in enumerate(ref[last]):
            if search == search_v:
                ref[last][search_k] = value
                changed = True

    return changed


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
    changed = False

    # walk
    for part in parts[:-1]:
        if isinstance(ref, Mapping) and part in ref:
            ref = ref[part]
        elif isinstance(ref, Sequence) and part.isdigit():
            ref = ref[int(part)]
        else:
            return False

    # last
    if isinstance(ref, Mapping) and last in ref \
            and isinstance(ref[last], Sequence):
        # replace any list element matches to regex
        search_re = re.compile(search)
        for search_k, search_v in enumerate(ref[last]):
            if search_re.match(str(search_v)):
                ref[last][search_k] = value
                changed = True

    return changed
