import requests
import os


class YaUploader:
    # 1.0 25.08.2020 Изначальный вариант
    # 1.1 06.09.2020

    # Версия 1.1
    def __init__(self,  yandex_token: str):
        self.YANDEX_TOKEN = yandex_token
        self.headers = {'Accept': 'application/json',
                        'Authorization': self.YANDEX_TOKEN}
        self.yad_url = "https://cloud-api.yandex.net/v1/disk/resources"

    def _upload_file(self, url_for_upload, local_file_path_name):
        result = dict()
        with open(file=local_file_path_name, mode="rb") as f:
            response = requests.put(url=url_for_upload, data=f)

        result["status_code"] = response.status_code
        if response.status_code in (200, 201):
            result["message"] = f"Я.Диск: Файл {local_file_path_name} успешно загружен"
        else:
            result["message"] = "Я.Диск: " + response.json()["message"]

        print(result['message'])
        return result

    def _get_upload_url(self, ydisk_file_path_name):
        result = dict()
        url_for_request = f"{self.yad_url}/upload?path={ydisk_file_path_name.replace('/','%2F')}&overwrite=true"
        response = requests.get(
            url_for_request, params={}, headers=self.headers)
        result["status_code"] = response.status_code
        if response.status_code == 200:
            result["href"] = response.json()['href']
            result["message"] = "Я.Диск: Сервер вернул адрес для начала работы с диском"
        else:
            result["message"] = "Я.Диск: " + response.json()['message']
        print(result['message'])
        return result

    def upload_local_file(self, local_file_path_name, ydisk_file_path_name=None):
        ''' upload local_file_path_name (path and file_name) from local computer as ydisk_file_path_name (path and file_name)'''
        result = dict()
        if ydisk_file_path_name is None:
            ydisk_file_path_name = "/" + os.path.basename(local_file_path_name)

        response = self._get_upload_url(ydisk_file_path_name)
        if response["status_code"] in (200, 201):
            result = self._upload_file(response["href"], local_file_path_name)
        else:
            result = response

        # print(result["message"])

        return result

    def create_folder(self, ydisk_path):
        ''' create folder as ydisk_path (path from the root of yandex disk)'''
        result = dict()
        url_for_request = f"{self.yad_url}?path={ydisk_path.replace('/','%2F')}"
        response = requests.put(
            url_for_request, params={}, headers=self.headers)

        result["status_code"] = response.status_code
        if result["status_code"] in (200, 201):
            result["message"] = f"Я.Диск: создана папка {ydisk_path}"
        else:
            result["message"] = "Я.Диск: " + response.json()['message']
        print(result['message'])
        return result

    def upload_url_file(self, url_file_web, ydisk_file_path_name=None):
        ''' upload file from url (url_file_web) as ydisk_file_path_name (path and file_name)'''
        result = dict()
        url_for_request = f"{self.yad_url}/upload?path={ydisk_file_path_name.replace('/','%2F')}&url={url_file_web.replace('/','%2F')}"
        response = requests.post(url=url_for_request,
                                 params={}, headers=self.headers)
        result["status_code"] = response.status_code
        # print(f"{result['status_code']}")
        if result["status_code"] in (200, 201):
            result["message"] = f"Я.Диск: файл {ydisk_file_path_name} успешно загружен"
        elif result["status_code"] == 202:
            result["message"] = f"Я.Диск: файл {ydisk_file_path_name} вскоре будет загружен"
        else:
            print(response.json())
            result["message"] = "Я.Диск: " + response.json()['message']
        print(result['message'])
        return result


if __name__ == '__main__':
    uploader = YaUploader("there is must be a token for Yandex Disk")
    result = uploader.create_folder("/testfolder6")
