import os.path
import shutil
import unittest
from pathlib import Path
from tabbyset.utils.folder import Folder


class TestFolder(unittest.TestCase):

    def test_Folder_initializes_with_absolute_path(self):
        folder = Folder(os.path.abspath('./test_folder'))
        self.assertTrue(folder.path.is_absolute())
        shutil.rmtree(folder)

    def test_Folder_creates_nonexistent_directory(self):
        folder = Folder('/tmp/nonexistent_folder')
        self.assertTrue(folder.path.exists())
        self.assertTrue(folder.path.is_dir())
        shutil.rmtree(folder)

    def test_listdir_returns_correct_contents(self):
        folder = Folder('/tmp/test_folder')
        (folder.path / 'file1.txt').touch()
        (folder.path / 'file2.txt').touch()
        contents = folder.listdir()
        self.assertIn('file1.txt', contents)
        self.assertIn('file2.txt', contents)
        shutil.rmtree(folder)

    def test_glob_matches_correct_files(self):
        folder = Folder('/tmp/test_folder')
        (folder.path / 'file1.txt').touch()
        (folder.path / 'file2.log').touch()
        matches = list(folder.glob('*.txt'))
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].name, 'file1.txt')
        shutil.rmtree(folder)

    def test_get_file_path_returns_correct_path(self):
        folder = Folder('/tmp/test_folder')
        file_path = folder.get_file_path('file1.txt')
        self.assertEqual(file_path, folder.path / 'file1.txt')
        shutil.rmtree(folder)

    def test_is_file_exists_returns_true_for_existing_file(self):
        folder = Folder('/tmp/test_folder')
        (folder.path / 'file1.txt').touch()
        self.assertTrue(folder.is_file_exists('file1.txt'))
        shutil.rmtree(folder)

    def test_is_file_exists_returns_false_for_nonexistent_file(self):
        folder = Folder('/tmp/test_folder_empty')
        self.assertFalse(folder.is_file_exists('file1.txt'))
        shutil.rmtree(folder)

    def test_clear_removes_all_contents(self):
        folder = Folder('/tmp/test_folder')
        (folder.path / 'file1.txt').touch()
        self.assertNotEqual(0, len(list(folder.glob('*'))))
        folder.clear()
        self.assertEqual(0, len(list(folder.glob('*'))))
        self.assertTrue(folder.path.exists())
        self.assertTrue(folder.path.is_dir())
        shutil.rmtree(folder)

    def test_mount_subfolder_returns_correct_subfolder(self):
        folder = Folder('/tmp/test_folder')
        subfolder = folder.mount_subfolder('subfolder')
        self.assertEqual(subfolder.path, folder.path / 'subfolder')
        shutil.rmtree(folder)

    def test_mount_from_current_module_returns_correct_folder(self):
        folder = Folder.mount_from_current_module('test_folder')
        current_file_path = Path(__file__).resolve()
        expected_path = (current_file_path.parent / 'test_folder').resolve()
        self.assertEqual(folder.path, expected_path)
        shutil.rmtree(folder)


if __name__ == '__main__':
    unittest.main()
