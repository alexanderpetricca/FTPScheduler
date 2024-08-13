import unittest

from ftpscheduler.locations import UploadLocation


class TestUploadLocationClass(unittest.TestCase):

    def setUp(self):

        self.test_location = UploadLocation(
            name = 'Test Location',
            local_folder = 'TestLocationLocal',
            upload_to = 'TestLocationRemote',
        )


    def test_location_object_creation(self):
        """
        Tests fascia objects are created correctly.
        """

        self.assertEqual(self.test_location.name, 'Test Location')
        self.assertEqual(self.test_location.local_folder, 'TestLocationLocal')
        self.assertEqual(self.test_location.upload_to, 'TestLocationRemote')


    def test_location_path_method(self):
        """
        Tests the fascias local abs path method returns the correct path.
        """

        test_drop_folder = 'testmachine/testuser/desktop/dropfolder/'

        full_path = self.test_location.local_folder_abs_path(test_drop_folder)
        self.assertEqual(
            full_path,
            'testmachine/testuser/desktop/dropfolder/TestLocationLocal',
        )
