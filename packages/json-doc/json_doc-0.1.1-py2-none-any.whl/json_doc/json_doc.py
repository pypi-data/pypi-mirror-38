# -*- coding: utf-8 -*-

#
# @author: Fatih Piristine <fatihpiristine () gmail dot com>
# @license: Apache License 2
#


import re

try:
    from collections.abc import Mapping, Sequence
except ImportError:
    from collections import Mapping, Sequence


def json_doc_get(doc, pointer, default=None):
    return json_doc(doc, pointer, do='get', default=default)


def json_doc_set(doc, pointer, value=None):
    return json_doc(doc, pointer, do='set', value=value)


def json_doc_has(doc, pointer, value=None):
    return json_doc(doc, pointer, do='has', value=value)


def json_doc_pop(doc, pointer):
    return json_doc(doc, pointer, do='pop')


"""
extended `set` functions for lists only
"""


def json_doc_append(doc, pointer, value=None):
    return json_doc(doc, pointer, do='append', value=value)


def json_doc_extend(doc, pointer, value=None):
    return json_doc(doc, pointer, do='extend', value=value)


def json_doc_replace(doc, pointer, value=None, search=None):
    return json_doc(doc, pointer, do='replace', value=value, search=search)


def json_doc_replace_re(doc, pointer, value=None, search=None):
    return json_doc(doc, pointer, do='replace_re', value=value, search=search)


def json_doc(doc, pointer, do=None, value=None, search=None, default=None):
    _re_escape = re.compile('(~[^01]|~$)')

    invalid_escape = _re_escape.search(pointer)
    if invalid_escape:
        raise Exception('Invalid escape {}'.format(invalid_escape.group()))

    parts = pointer.split('/')

    if parts.pop(0) != '':
        raise Exception('Pointer must start with /')

    parts = [part.replace('~', '~0').replace('/', '~1') for part in parts]

    if len(parts) == 0:
        raise Exception('Invalid pointer: %s' % pointer)

    ref, last = doc, parts[-1]

    # set: lists
    if do in ['append', 'extend', 'replace', 'replace_re']:
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
        if isinstance(ref, Mapping) and last in ref and isinstance(ref[last], Sequence):
            if do == 'append':
                ref[last].append(value)

            elif do == 'extend':
                ref[last].extend(value)
            elif do == 'replace':
                # replace any list element that matches
                for search_k, search_v in enumerate(ref[last]):
                    if search == search_v:
                        ref[last][search_k] = value
            elif do == 'replace_re':
                # replace any list element matches to regex
                search_re = re.compile(search)
                for search_k, search_v in enumerate(ref[last]):
                    if search_re.match(str(search_v)):
                        ref[last][search_k] = value
        elif isinstance(ref, Sequence):
            # nothing to do here
            pass
        else:
            raise Exception('Invalid document')
    # set: dict
    elif do == 'set':
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
    # pop
    elif do == 'pop':
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
            return True
        elif isinstance(ref, Sequence) and last.isdigit():
            _return = False
            try:
                ref.pop(int(last))
                _return = True
            finally:
                return _return
        else:
            return False
    # get
    elif do == 'get':
        # walk
        for part in parts[:-1]:
            if isinstance(ref, Mapping) and part in ref:
                ref = ref[part]
            elif isinstance(ref, Sequence) and part.isdigit():
                try:
                    ref = ref[int(part)]
                except IndexError:
                    return default
            else:
                return default

        # last
        if isinstance(ref, Mapping) and last in ref:
            return ref[last]
        elif isinstance(ref, Sequence) and last.isdigit():
            _return = default
            try:
                _return = ref[int(last)]
            finally:
                return _return
        else:
            return default
    # has
    elif do == 'has':
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
                return value in ref
            elif value and isinstance(ref[last], Mapping):
                return value == ref[last]
            else:
                return True
        elif isinstance(ref, Sequence) and last.isdigit():
            try:
                ref = ref[int(last)]
                return True
            except IndexError:
                return False
        else:
            return False

    return doc
