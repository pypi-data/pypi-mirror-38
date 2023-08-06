# python-json-doc
Utility functions for JSON Document

[![Build Status](https://travis-ci.org/ddfs/python-json-doc.svg?branch=master)](https://travis-ci.org/ddfs/python-json-doc)
[![Coverage Status](https://coveralls.io/repos/github/ddfs/python-json-doc/badge.svg?branch=master)](https://coveralls.io/github/ddfs/python-json-doc?branch=master)
[![GitHub license](https://img.shields.io/github/license/ddfs/python-json-doc.svg)](https://github.com/ddfs/python-json-doc/blob/master/LICENSE)

It can handle get/set/pop/has operations on nodes

Extended `set` functions for lists:
- append: appends to the list
- extend: extends the list
- replace: `search` and replace in the list  
- replace_re: `search` and replace in the list using regular expression

No external dependencies. Tests requires `unittest2` module

Compatible with Python 2.6+ and 3.3+ 


Examples
---
```python 
doc = {
    'a': {
        'deep': {
            'nested': {
                'list': [1, 2, 3, {'dict': 'OK'}],
                'string': 'string',
                'hex': 0x010101
            }
        },
    },
    'list': [1, 2, 3]
}

# get
print json_doc_get(doc, '/a/deep/nested/list/3/dict')
>> OK

# set
print json_doc_set(doc, '/a/deep/nested/string', 'new string')['a']['deep']['nested']['string']
>> new string

# pop: target exist
print json_doc_pop(doc, '/a/deep/nested/list/2')
>> True

# pop: target doesn't exist
print json_doc_pop(doc, '/a/deep/nested/list/5')
>> False

# has item
print json_doc_has(doc, '/a/deep/nested/list/3/dict')
>> True

# has item with value
print json_doc_has(doc, '/a/deep/nested/list/3/dict', 'OK')
>> True

## List only functions

# append
print json_doc_append(doc, '/list', 4)['list']
[1, 2, 3, 4]

# extend
print json_doc_extend(doc, '/list', [5, 6, 7])['list']
[1, 2, 3, 4, 5, 6, 7]

# replace: value -> new value, search -> old value
print json_doc_replace(doc, '/list', 44, 4)['list']
[1, 2, 3, 44, 5, 6, 7]

# replace_re: -> new value, search -> regex
[111, 2, 3, 44, 5, 6, 7]

```
