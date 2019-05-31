import unittest.mock
import mock


from isoimage import mkdir_p, create_destination_directory, extract_zip_file
from isoimage import extract_tar_file, does_file_exists


class TestFactorial(unittest.TestCase):

    @mock.patch('isoimage.os')
    def test_mkdirs_called_once(self, mocked_os):
        mkdir_p('something')
        mocked_os.makedirs.assert_called_once()

    @mock.patch('isoimage.os')
    def test_mkdirs_called_with_certain_variales(self, mocked_os):
        mkdir_p('something')
        mocked_os.makedirs.assert_called_with('something', exist_ok=True)

    @mock.patch('isoimage.os')
    def test_create_destination_directory_called_once(self, mocked_os):
        create_destination_directory(None, 'something')
        mocked_os.makedirs.assert_called_once()

    @mock.patch('isoimage.os')
    def test_create_destination_directory_when_no_parent(self, mocked_os):
        mocked_os.sep = '\\'
        create_destination_directory(None, 'something')
        mocked_os.makedirs.assert_called_with('target\\something', exist_ok=True)

    @mock.patch('isoimage.os')
    def test_create_destination_directory_with_parent(self, mocked_os):
        mocked_os.sep = '\\'
        create_destination_directory('parent', 'something')
        mocked_os.makedirs.assert_called_with('target\\parent\\something', exist_ok=True)

    @mock.patch('isoimage.zipfile')
    def test_extract_zip_file(self, mocked_zipfile):
        extract_zip_file('file_name', 'destination')
        mocked_zipfile.ZipFile.assert_called_with('file_name', 'r')

    @mock.patch('isoimage.tarfile')
    def test_extract_tar_file(self, mocked_tarfile):
        extract_tar_file('file_name', 'destination')
        mocked_tarfile.open.assert_called_with('file_name')

    @mock.patch('isoimage.os')
    def test_does_file_exists_called_once(self, mocked_os):
        result = does_file_exists('file_name')
        mocked_os.path.exists.assert_called_once()
        assert (result == True)

    @mock.patch('isoimage.os')
    def test_does_file_exists_called_with(self, mocked_os):
        result = does_file_exists('file_name')
        mocked_os.path.exists.assert_called_with('file_name')
        assert (result == True)


if __name__ == '__main__':
    unittest.main()
