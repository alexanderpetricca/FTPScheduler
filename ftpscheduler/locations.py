import os

class UploadLocation:

    def __init__(self, name, local_folder, upload_to):
        self.name = name
        self.local_folder = local_folder
        self.upload_to = upload_to


    def local_folder_abs_path(self, drop_folder):
        """
        Returns the full absolute path of the location local folder.
        """

        return os.path.join(drop_folder, self.local_folder)


    def scan_folder(self, drop_folder):
        """
        Returns an array of the filepaths of all images in the specified folder.
        """

        folder_dir = os.path.join(drop_folder, self.local_folder)

        image_files = [
            os.path.join(drop_folder, self.local_folder, image_file) for 
                image_file in os.listdir(folder_dir) if image_file.endswith('.jpg')
        ]

        if len(image_files) != 0:
            return True, image_files
        else:
            return False, None