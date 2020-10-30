from abc import ABC, abstractmethod


class Uploader(ABC):
    """Abstract class for classes which manipulation with Remote Disk (YaUploader, GDUploader etc) """

    @abstractmethod
    def create_folder():
        """Create folder on Remote Disk"""

    @abstractmethod
    def upload_local_file():
        """This function upload file from local computer as file to Remote Disk"""

    @abstractmethod
    def upload_url_file():
        """This function upload file from URI as file to Remote Disk"""
