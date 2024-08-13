import os, json, time, socket, shutil, sys, ftplib
from pathlib import Path

import schedule
from dotenv import load_dotenv

from locations import UploadLocation
from utils import TextColours


class FTPScheduler:
    """
    Main application class.
    """

    def __init__(self):

        # Load config
        with open('./config.json') as configfile:
            parsed_json = json.load(configfile)

        fascia_config = parsed_json['uploadLocations']
        
        # Create fascia objects
        self.locations = []
        for fascia in fascia_config:            
            new_location = UploadLocation(
                name = fascia_config[fascia].get('name'),
                local_folder = fascia_config[fascia].get('local_folder'),
                upload_to = fascia_config[fascia].get('upload_to')
            )
            self.locations.append(new_location)
        
        # Set schedule time from json object
        self.schedule_time = parsed_json['schedule']

        # Set monitor interval from json object 
        self.monitor_interval = parsed_json['interval']
        
        # Set desktop and dropfolder paths
        self.desktop = os.path.join(str(Path.home()), 'desktop/')
        self.drop_folder = os.path.join(self.desktop, 'AutoUploader')


    def make_folders(self):
        """
        Creates the folder structure if it doesnt already exist.
        """

        if not os.path.exists(self.drop_folder):
            os.mkdir(self.drop_folder)

        for location in self.locations:

            # Local fascia folder
            folder_path = os.path.join(self.drop_folder, location.local_folder)
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)

            # Uploaded folder within local fascia folder
            uploaded_path = os.path.join(folder_path, '_uploaded')
            if not os.path.exists(uploaded_path):
                os.mkdir(uploaded_path)


    def check_network_connection(self, host="8.8.8.8", port=53, timeout=3, startup=False):
        """
        Host: 8.8.8.8 (google-public-dns-a.google.com)
        OpenPort: 53/tcp
        Service: domain (DNS/TCP)
        """

        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            if startup:
                print(f'Network connection...{TextColours.GREEN}OK{TextColours.ENDC}')
            return True
        except socket.error as ex:
            print(ex)
            return False


    def upload_folder(self):
        """
        Runs the upload process, attempting to upload assets located in the 
        AutoUploader directories, to FTP.
        """

        print(f'{time.asctime()} // Checking directories...')
            
        # Check each folder and confirm if laden
        for location in self.locations:
            laden_folder, images = location.scan_folder(self.drop_folder)

            # If it is laden, upload to corresponding folder
            if laden_folder:
                print(f'{time.asctime()} // Found {len(images)} images in {TextColours.YELLOW}{location.local_folder}{TextColours.ENDC}')
                try:
                    # Connect / authenticate with the ftp server
                    load_dotenv()
                    FTP_HOST = os.getenv('FTP_HOST')
                    FTP_USER = os.getenv('FTP_USER') 
                    FTP_PSWD = os.getenv('FTP_PSWD')
                    ftp_server = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PSWD)
                    
                    # Set the upload location
                    ftp_server.cwd(location.upload_to)

                    for image in images:
                        print(f'{time.asctime()} // Uploading {TextColours.YELLOW}{image}{TextColours.ENDC}')
                        upload = self.upload_asset(ftp_server, image=image, upload_to=location.upload_to)
                        
                        if upload == True:
                            print(f'{time.asctime()} // {TextColours.GREEN}Upload Complete{TextColours.ENDC}') 
                            shutil.move(image, os.path.join(self.drop_folder, location.local_folder, '_uploaded'))
                        else:
                            print(f'{time.asctime()} // {TextColours.RED}Upload Failed{TextColours.ENDC}')

                except Exception as e:
                    print(f'FTP connection error: {e}')

                finally:
                    # Close FTP connection
                    if ftp_server:
                        ftp_server.quit()


    def upload_asset(self, ftp_server, image, upload_to) -> bool:
        """
        Uploads the asset to Amplience, via FTP.
        """

        # FTP transfer
        file_name = image.split('/')[-1]
        print(f'{time.asctime()} // Transferring {file_name} -> {upload_to}...')

        try:
            with open(image, 'rb') as file:
                ftp_server.storbinary(f'STOR {file_name}', file)
                return True
        
        except ftplib.all_errors as e:
            print(f'Failed to upload {file_name}: {e}')
            return False                                   


    def run(self):
        """
        Triggers the application with corresponding flag.
        """
        
        try:
            flag = sys.argv[1]
        except IndexError:
            flag = '-s'

        self.make_folders()
        self.check_network_connection(startup=True)

        # Run scheduled mode
        if flag == '-s':
            print(f'Autoupload active, {TextColours.GREEN}upload scheduled for {self.schedule_time} each day{TextColours.ENDC}, monitoring {TextColours.YELLOW}{self.drop_folder}/{TextColours.ENDC}')
            schedule.every().day.at('00:00').do(self.upload_folder)
    
            while True:
                schedule.run_pending()
                time.sleep(1)

        # Run interval mode
        elif flag == '-i':
            print(f'Autoupload active {TextColours.GREEN}uploading every {self.monitor_interval} minutes{TextColours.ENDC}, monitoring {TextColours.YELLOW}{self.drop_folder}/{TextColours.ENDC}')
            schedule.every(self.monitor_interval).minutes.do(self.upload_folder)
            
            while True:
                schedule.run_pending()
                time.sleep(1)

        # Run test mode
        elif flag == '-t':
            print(f'Autoupload active, {TextColours.GREEN}upload scheduled for {self.schedule_time} each day{TextColours.ENDC}, monitoring {TextColours.YELLOW}{self.drop_folder}/{TextColours.ENDC}')
            self.upload_folder()