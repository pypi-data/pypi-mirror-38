""" Unit test for Reuse. """
import os
import sys
import unittest

test_dir = os.path.dirname(__file__)
src_dir = os.path.join(test_dir, '..')
sys.path.insert(0, src_dir)

import reuse as rs


class TestReuse(unittest.TestCase):

    def test_check_exists(self):
        self.assertTrue(rs.check_exists('/etc/apt'))
        self.assertFalse(rs.check_exists('/etc/apt/not_exist'))

    def test_concat_path(self):
        self.assertEqual(rs.concat_path(['home', 'user', 'project']),
                         'home/user/project')
        self.assertEqual(rs.concat_path(['/home', 'user', 'project']),
                         '/home/user/project')

    def test_flat_list(self):
        self.assertEqual(rs.flat_list([[1, 2], [3]]), [1, 2, 3])
        self.assertEqual(rs.flat_list([1, 2]), [1, 2])
        self.assertEqual(rs.flat_list([]), [])

    def test_parent_dir(self):
        self.assertEqual(rs.parent_dir('/etc/apt/sources.list'), '/etc/apt')
        self.assertEqual(rs.parent_dir('/etc/apt'), '/etc')

    def test_full_name(self):
        self.assertEqual(rs.full_name('/etc/apt/sources.list'), 'sources.list')
        self.assertEqual(rs.full_name('/etc/apt'), 'apt')

    def test_pure_name(self):
        self.assertEqual(rs.pure_name('/etc/apt/sources.list'), 'sources')
        self.assertEqual(rs.full_name('/etc/apt'), 'apt')


if __name__ == '__main__':
    unittest.main()

