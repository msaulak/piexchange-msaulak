import os
from unittest import TestCase

from src.utils.helper_methods import object_to_str, log_and_call, get_parent_dir
from unittest.mock import MagicMock, Mock


def test_method(*args, **kwargs):
    return ['mocked_return', args, kwargs]

class TestHelperMethods(TestCase):
    def test_log_and_call(self):
        self.assertEqual(1, 1)
        test_log_call = log_and_call(test_method)

        actual_ret_list = test_log_call('arg1', 'arg2', args3='arg3', arg4='arg4')

        expected_ret_list = ['mocked_return', (('arg1', 'arg2'), {'args3': 'arg3', 'arg4': 'arg4'}), {}]

        self.assertEqual(expected_ret_list, actual_ret_list)

    def test_object_to_str(self):
        test_obj = MagicMock()

        setattr(test_obj, 'attr1', 'val1')
        setattr(test_obj, 'attr2', 2)

        expected = 'attr1 : val1 | attr2 : 2'
        actual = object_to_str(test_obj)

        self.assertEqual(expected, actual)

    def test_get_parent_dir(self):
        test_path = os.path.join('pi', 'exchange', 'test', 'path')
        actual = get_parent_dir(test_path, levels_up=2)
        expected = 'pi\exchange'
        self.assertEqual(expected, actual)

    def test_get_parent_recurion_limit(self):
        test_path = os.path.join('pi', 'exchange', 'test', 'path')
        self.assertRaises(RecursionError, get_parent_dir, test_path, levels_up=200000000)
