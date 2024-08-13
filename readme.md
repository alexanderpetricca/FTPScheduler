# FTP Scheduler

## Description
Upload images to an FTP server on either a schedule or at pre-determined
intervals.

## Installation

### Global Install
1. `$ pip3 install -r requirements.txt`
2. Add a .env file to the project root, with the following variables:
   - FTP_HOST (type: string, the FTP hostname)
   - FTP_USER (type: string, the FTP username)
   - FTP_PSWD (type: string, the FTP password)
3. Configure fascias in the `config.json` file as per below instructions.

## Starting the Application

Launch the application with the following command. Launching without a flag (see below) defaults to scheduled mode.

`$ python3 ftpscheduler/main.py`

## Flags
The application offers three modes:
- **Scheduled** (default). Trigger this with the `-s` flag. Upload will be triggered once per day, at the time specified for the value 'schedule' in the config file. If no flag is specified, the application will default to this.
- **Interval**. Trigger this with the `-i` flag. Upload will occur every x minutes, with x being the value specified for the value 'interval' in the config file.
- **Test**. Trigger this with the `-t` flag. Upload will occur immediately, and only once.

## Setting the Schedule / Interval
You can set the schedule / interval timing by updating the **config.json** file.

### Schedule
This is configured by changing the value for `schedule`. This should be a time, set in 24h format, as a string, i.e. **"01:00"** for 1am. By default, this is set to **midnight**.

### Interval
This is configured by changing the value for `interval`. This is a period of time in whole minutes, as a number. For example, for 5 minute intervals, this should be set to **5**. By default, this is set to **15 mins**.

## Adding Additional Upload Locations
By default, the application creates upload locations for documents, images and video. You can replace these, or add additional locations by updating the `"uploadLocations"` object within **config.json**. The individual objects should be configured as so:

```json
"mul": {
    "name": "My Upload Location",
    "local_folder": "My Upload Location",
    "upload_to": "Images/MyUploadLocation/"
},
```

## Running the Test Suite
`$ python -m unittest tests/test.py`