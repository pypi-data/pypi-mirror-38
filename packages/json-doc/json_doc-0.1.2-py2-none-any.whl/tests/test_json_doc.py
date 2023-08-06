"""
JSON-Doc

@author: Fatih Piristine <fatihpiristine () gmail dot com>
@license: Apache License 2
"""

import unittest2

from json_doc import json_doc_get, json_doc_set, json_doc_has, json_doc_pop, \
    json_doc_append, json_doc_extend, json_doc_replace, json_doc_replace_re


class TestJsonDoc(unittest2.TestCase):
    """
    json_doc_* tests
    """

    def setUp(self):
        self.doc_get = {
            '0': {
                '1': {
                    '2': {
                        '3': [4]
                    }
                }
            },
            'a': {
                'deep': {
                    'nested': {
                        'string': 'value'
                    }
                }
            },
            'b': {
                'deep': {
                    'nested': {
                        'list': [1, 2, 3, {'dict': 'OK'}],
                        'string': 'string',
                        'hex': 0x010101
                    }
                },
            },
            'list_num': [1, 2, 3],
            'list_str': ['a', 'b', 'c'],
            'list_mix': [1, 'b', {'c': 0}],
            'list_dict': [{'dict_1': 1}, {'dict_2': [{'dict_3': '3'}]}]
        }

        self.doc_set = {}
        self.doc_pop = self.doc_get

    def test_json_doc_get_exception(self):
        """
        Test exceptions raised with json_doc_get
        :return:
        """
        with self.assertRaises(Exception):
            json_doc_get(self.doc_get, '')

        with self.assertRaises(Exception):
            json_doc_get(self.doc_get, '~')

        with self.assertRaises(Exception):
            json_doc_get(self.doc_get, '/~')

    def test_json_doc_get(self):
        """
        Test json_doc_get
        :return:
        """
        # test: root
        self.assertEqual(json_doc_get(self.doc_get, '/'), None)

        # test: empty doc
        self.assertEqual(json_doc_get({}, '/0/1/2/3/0'), None)

        # test: 0
        self.assertEqual(json_doc_get(self.doc_get, '/0/1/2/3/0'), 4)

        # test: a
        self.assertEqual(json_doc_get(self.doc_get, '/a'),
                         {'deep': {'nested': {'string': 'value'}}})
        self.assertEqual(json_doc_get(self.doc_get, '/a/deep'),
                         {'nested': {'string': 'value'}})
        self.assertEqual(json_doc_get(self.doc_get, '/a/deep/nested'),
                         {'string': 'value'})
        self.assertEqual(json_doc_get(self.doc_get, '/a/deep/nested/string'),
                         'value')
        self.assertEqual(
            json_doc_get(self.doc_get, '/a/deep/nested/string/not-found'), None)

        # test: b
        self.assertEqual(json_doc_get(self.doc_get, '/b'),
                         {'deep': {'nested': {
                             'list': [1, 2, 3, {'dict': 'OK'}],
                             'string': 'string',
                             'hex': 0x010101}}})
        self.assertEqual(json_doc_get(self.doc_get, '/b/deep'),
                         {'nested': {'list': [1, 2, 3, {'dict': 'OK'}],
                                     'string': 'string',
                                     'hex': 0x010101}})

        self.assertEqual(json_doc_get(self.doc_get, '/b/deep/nested'),
                         {'list': [1, 2, 3, {'dict': 'OK'}],
                          'string': 'string',
                          'hex': 0x010101})

        self.assertEqual(json_doc_get(self.doc_get, '/b/deep/nested/list'),
                         [1, 2, 3, {'dict': 'OK'}])
        self.assertEqual(json_doc_get(self.doc_get, '/b/deep/nested/list/0'), 1)
        self.assertEqual(json_doc_get(self.doc_get, '/b/deep/nested/list/1'), 2)
        self.assertEqual(json_doc_get(self.doc_get, '/b/deep/nested/list/2'), 3)
        self.assertEqual(json_doc_get(self.doc_get, '/b/deep/nested/list/3'),
                         {'dict': 'OK'})
        self.assertEqual(
            json_doc_get(self.doc_get, '/b/deep/nested/list/3/dict'), 'OK')
        self.assertEqual(json_doc_get(self.doc_get, '/b/deep/nested/string'),
                         'string')
        self.assertEqual(json_doc_get(self.doc_get, '/b/deep/nested/hex'),
                         0x010101)

        # test: list_num
        self.assertEqual(json_doc_get(self.doc_get, '/list_num'), [1, 2, 3])
        self.assertEqual(json_doc_get(self.doc_get, '/list_num/0'), 1)
        self.assertEqual(json_doc_get(self.doc_get, '/list_num/1'), 2)
        self.assertEqual(json_doc_get(self.doc_get, '/list_num/2'), 3)

        # test: OutOfBounds -> None
        self.assertEqual(json_doc_get(self.doc_get, '/list_num/3'), None)

        # test: list_str
        self.assertEqual(json_doc_get(self.doc_get, '/list_str'),
                         ['a', 'b', 'c'])
        self.assertEqual(json_doc_get(self.doc_get, '/list_str/0'), 'a')
        self.assertEqual(json_doc_get(self.doc_get, '/list_str/1'), 'b')
        self.assertEqual(json_doc_get(self.doc_get, '/list_str/2'), 'c')

        # test: list_mix
        self.assertEqual(json_doc_get(self.doc_get, '/list_mix'),
                         [1, 'b', {'c': 0}])
        self.assertEqual(json_doc_get(self.doc_get, '/list_mix/0'), 1)
        self.assertEqual(json_doc_get(self.doc_get, '/list_mix/1'), 'b')
        self.assertEqual(json_doc_get(self.doc_get, '/list_mix/2'), {'c': 0})

        # test: list_dic
        self.assertEqual(json_doc_get(self.doc_get, '/list_dict'),
                         [{'dict_1': 1}, {'dict_2': [{'dict_3': '3'}]}])
        self.assertEqual(json_doc_get(self.doc_get, '/list_dict/0'),
                         {'dict_1': 1})
        self.assertEqual(json_doc_get(self.doc_get, '/list_dict/0/dict_1'), 1)
        self.assertEqual(json_doc_get(self.doc_get, '/list_dict/1'),
                         {'dict_2': [{'dict_3': '3'}]})
        self.assertEqual(json_doc_get(self.doc_get, '/list_dict/1/dict_2'),
                         [{'dict_3': '3'}])
        self.assertEqual(json_doc_get(self.doc_get, '/list_dict/1/dict_2/0'),
                         {'dict_3': '3'})

    def test_json_doc_set_exception(self):
        """
        Test exceptions raised with json_doc_set
        :return:
        """
        with self.assertRaises(Exception):
            json_doc_set(self.doc_set, '', None)

        with self.assertRaises(Exception):
            json_doc_set(self.doc_set, '/~', None)

    def test_json_doc_set(self):
        """
        Test json_doc_set
        :return:
        """
        self.assertEqual(json_doc_set(self.doc_set, '/set-int', 123)['set-int'],
                         123)
        self.assertEqual(
            json_doc_set(self.doc_set, '/set-hex', 0x010101)['set-hex'],
            0x010101)
        self.assertEqual(
            json_doc_set(self.doc_set, '/set-str', 'str')['set-str'], 'str')
        self.assertEqual(
            json_doc_set(self.doc_set, '/set-list', ['a', 'list'])['set-list'],
            ['a', 'list'])
        self.assertEqual(
            json_doc_set(self.doc_set, '/set-dict', {'a': 'dict'})['set-dict'],
            {'a': 'dict'})

        # test: convert
        self.assertEqual(
            json_doc_set(self.doc_set, '/set-int', [123])['set-int'], [123])
        self.assertEqual(
            json_doc_set(self.doc_set, '/set-hex', [0x010101])['set-hex'],
            [0x010101])
        self.assertEqual(
            json_doc_set(self.doc_set, '/set-str', ['str'])['set-str'], ['str'])
        self.assertEqual(
            json_doc_set(self.doc_set, '/set-list', 'a list')['set-list'],
            'a list')
        self.assertEqual(
            json_doc_set(self.doc_set, '/set-dict', 'a dict')['set-dict'],
            'a dict')

        # test: create list elements with sub lists
        self.assertEqual(json_doc_set(self.doc_set, '/set-1', [123])['set-1'],
                         [123])
        self.assertEqual(
            json_doc_set(self.doc_set, '/set-1/0', 'list-1')['set-1'],
            ['list-1'])
        self.assertEqual(json_doc_set(self.doc_set, '/set-2', [123])['set-2'],
                         [123])
        self.assertEqual(json_doc_set(self.doc_set, '/set-2/0', [123])['set-2'],
                         [[123]])
        self.assertEqual(
            json_doc_set(self.doc_set, '/set-2/0/0', [123])['set-2'], [[[123]]])
        self.assertEqual(
            json_doc_set(self.doc_set, '/set-2/0/0/0', [123])['set-2'],
            [[[[123]]]])

        # test: create list elements with sub dicts
        self.assertEqual(json_doc_set(self.doc_set, '/set-3', [])['set-3'], [])
        self.assertEqual(json_doc_set(self.doc_set, '/set-3', [{}])['set-3'],
                         [{}, ])
        self.assertEqual(
            json_doc_set(self.doc_set, '/set-3/0/list', [{}])['set-3'][0],
            {'list': [{}]})
        self.assertEqual(json_doc_set(self.doc_set, '/set-3/0/list/0/dict/list',
                                      ['A', 'B', 'C'])['set-3'][0]['list'][0],
                         {'dict': {'list': ['A', 'B', 'C']}})
        self.assertEqual(
            json_doc_set(self.doc_set, '/set-3/0/list/0/dict/list/1',
                         'BB')['set-3'][0]['list'][0]['dict']['list'][1], 'BB')

    def test_json_doc_pop(self):
        """
        Test json_doc_pop
        :return:
        """
        self.assertFalse(json_doc_pop(self.doc_pop, '/set-int'))
        self.assertFalse(json_doc_pop(self.doc_pop, '/set'))

        # test: character keys
        self.assertTrue(json_doc_pop(self.doc_pop, '/a/deep/nested/string'))
        self.assertTrue(json_doc_pop(self.doc_pop, '/a/deep/nested'))
        self.assertTrue(json_doc_pop(self.doc_pop, '/a/deep'))

        # test: numerical dict keys
        self.assertFalse(json_doc_pop(self.doc_pop, '/0/1/2/3/4'))
        self.assertTrue(json_doc_pop(self.doc_pop, '/0/1/2/3'))
        self.assertTrue(json_doc_pop(self.doc_pop, '/0/1/2'))
        self.assertTrue(json_doc_pop(self.doc_pop, '/0/1'))
        self.assertTrue(json_doc_pop(self.doc_pop, '/0'))

        # test: mixed tree
        self.assertTrue(
            json_doc_pop(self.doc_pop, '/b/deep/nested/list/3/dict'))
        self.assertTrue(json_doc_pop(self.doc_pop, '/b/deep/nested/list/3'))

    def test_json_doc_has(self):
        """
        Test json_doc_has
        :return:
        """
        self.assertTrue(json_doc_has(self.doc_get, '/b/deep/nested/list/0'))
        self.assertTrue(json_doc_has(self.doc_get, '/b/deep/nested/list/0', 1))
        self.assertTrue(
            json_doc_has(self.doc_get, '/b/deep/nested/list/3/dict'))
        self.assertTrue(
            json_doc_has(self.doc_get, '/b/deep/nested/list/3/dict', 'OK'))
        self.assertTrue(json_doc_has(self.doc_get, '/0/1/2/3/0'))

        # test: has value in list
        self.assertTrue(json_doc_has(self.doc_get, '/0/1/2/3', 4))

    def test_json_doc_append(self):
        """
        Test json_doc_append
        :return:
        """
        self.assertListEqual(
            json_doc_append(self.doc_get, '/0/1/2/3', 5)['0']['1']['2']['3'],
            [4, 5])

    def test_json_doc_extend(self):
        """
        Test json_doc_extend
        :return:
        """
        self.assertDictEqual(
            json_doc_extend(self.doc_get, '/0/1/2/3', [5, 6])['0']['1']['2'],
            {'3': [4, 5, 6]})

    def test_json_doc_replace(self):
        """
        Test json_doc_replace
        :return:
        """
        self.assertDictEqual(
            json_doc_replace(self.doc_get, '/0/1/2/3', 22, 4)['0'],
            {'1': {'2': {'3': [22]}}})

    def test_json_doc_replace_re(self):
        """
        Test json_doc_replace_re
        :return:
        """
        self.assertEqual(
            json_doc_replace_re(self.doc_get, '/list_str', 'aa', 'a')[
                'list_str'][0], 'aa')
        self.assertEqual(
            json_doc_replace_re(self.doc_get, '/list_str', 'aaa', '^a')[
                'list_str'][0], 'aaa')
        self.assertListEqual(
            json_doc_replace_re(self.doc_get, '/list_str', 'aaa', '[ab]')[
                'list_str'],
            ['aaa', 'aaa', 'c'])

        self.assertEqual(
            json_doc_replace_re(self.doc_get, '/list_num', 111, '^1$')[
                'list_num'][0], 111)

    def tearDown(self):
        """
        Teardown test
        :return:
        """
        self.doc_get = None
        self.doc_set = None
        self.doc_pop = None


if __name__ == '__main__':
    unittest2.main()
