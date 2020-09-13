# from __future__ import print_function
import pickle
import os.path
import mimetypes
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
from tempfile import gettempdir
import requests

# Взят за основу google.develop


class GDUploader:
    def __init__(self):
        # If modifying these scopes, delete the file token.pickle.
        self.SCOPES = [
            'https://www.googleapis.com/auth/drive.metadata.readonly',
            'https://www.googleapis.com/auth/drive']
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('drive', 'v3', credentials=creds)

    def get_files_list(self):
        # Call the Drive v3 API
        results = self.service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        for item in items:
            print(f"{item['name']} ({item['id']})")

    def create_folder(self, gd_path):
        """ create folder as gd_path (path from the root of google drive disk)
        return folder_id
        """
        result = None  # folder_id
        folder_metadata = {'name': gd_path,
                           'parents': list(''),
                           'mimeType': 'application/vnd.google-apps.folder'}
        create_folder = self.service.files().create(
            body=folder_metadata, fields='id').execute()
        result = create_folder.get('id', [])
        print(result)
        return result

    def upload_local_file(self, local_file_path_name, gdrive_folder_id):
        """upload local_file_path_name (path and file_name) from local computer to gdrive_folder_id
        """
        result = None
        local_file_name = os.path.basename(local_file_path_name)

        some_metadata = {'name': local_file_name,
                         'parents': [gdrive_folder_id]}
        os_file_mimetype = mimetypes.MimeTypes().guess_type(local_file_name)[0]

        media = MediaFileUpload(local_file_path_name,
                                mimetype=os_file_mimetype)

        upload_this = self.service.files().create(body=some_metadata,
                                                  media_body=media,
                                                  fields='id').execute()
        result = upload_this.get('id', [])

        print(result)

    def _load_from_web_to_local_temp(self, url_file_web):
        """ Download frile from web to temp directory of local drive 
        Return full_path with file nime in temp directory of local drive
        """
        local_file_name = os.path.basename(url_file_web)
        local_file_path_name = (os.path.join(gettempdir(), local_file_name))
        downloaded_file = requests.get(url_file_web)
        with open(local_file_path_name, "wb") as temp_file:
            temp_file.write(downloaded_file.content)

        return local_file_path_name

    def upload_url_file(self, url_file_web, gdrive_folder_id):
        """upload url_file_web from web to gdrive_folder_id
        """
        local_file_path_name = self._load_from_web_to_local_temp(url_file_web)
        self.upload_local_file(local_file_path_name, gdrive_folder_id)

        print(f"GDrive: file {url_file_web} uploaded to Google Drive")


if __name__ == '__main__':
    uploader = GDUploader()
    print("Создано GDUploader")
    # uploader.get_files_list()
    # print(os.path.join(gettempdir(), "222.jpg"))
    folder_id = uploader.create_folder("testfolder5")
    # file_id = uploader.upload_local_file("C:\\_work\\_projects\\netology-diploma-A\\files\\aurora_v_svadebnom_platie.jpg", folder_id)
    file_id = uploader.upload_url_file(
        "https://1.bp.blogspot.com/-i6mgSNXptdg/Xjz0oJziruI/AAAAAAAADT4/5LzavjZ6FNoC3qTM0Yf_aisxWN6qHc2hwCK4BGAYYCw/s1600/2824997812.jpg", folder_id)
