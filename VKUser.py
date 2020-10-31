import requests
from datetime import datetime


class VKUser():
    """Class VKUser - access to VK API through user

    Args:
        (int): Vkontakte (VK) user id 
    Returns:
        []: object that represent VK user
    """
    TOKEN = "958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008"
    VKAPI_URL = "https://api.vk.com/method/"
    PICTURE_SIZES = "wzyxrqpoms"

    '''
    s — пропорциональная копия изображения с максимальной стороной 75px;
    m — пропорциональная копия изображения с максимальной стороной 130px;
    x — пропорциональная копия изображения с максимальной стороной 604px;
    o — если соотношение "ширина/высота" исходного изображения меньше или равно 3:2, то пропорциональная копия с максимальной стороной 130px. Если соотношение "ширина/высота" больше 3:2, то копия обрезанного слева изображения с максимальной стороной 130px и соотношением сторон 3:2.
    p — если соотношение "ширина/высота" исходного изображения меньше или равно 3:2, то пропорциональная копия с максимальной стороной 200px. Если соотношение "ширина/высота" больше 3:2, то копия обрезанного слева и справа изображения с максимальной стороной 200px и соотношением сторон 3:2.
    q — если соотношение "ширина/высота" исходного изображения меньше или равно 3:2, то пропорциональная копия с максимальной стороной 320px. Если соотношение "ширина/высота" больше 3:2, то копия обрезанного слева и справа изображения с максимальной стороной 320px и соотношением сторон 3:2.
    r — если соотношение "ширина/высота" исходного изображения меньше или равно 3:2, то пропорциональная копия с максимальной стороной 510px. Если соотношение "ширина/высота" больше 3:2, то копия обрезанного слева и справа изображения с максимальной стороной 510px и соотношением сторон 3:2
    y — пропорциональная копия изображения с максимальной стороной 807px;
    z — пропорциональная копия изображения с максимальным размером 1080x1024;
    w — пропорциональная копия изображения с максимальным размером 2560x2048px.
    '''

    def __init__(self, user_id):
        self.user_id = user_id

    def __str__(self):
        """string representation of the Class

        Returns:
            [str]: link to the homepage of user
        """

        return f"https://vk.com/id{str(self.user_id)}"

    def print_user_id(self, user_id=None):
        '''print user id with user = user_id (or current user if user_id is None)'''
        print(f"User id is {self.user_id if user_id is None else user_id}")

    def get_user_info(self, user_id=None):
        '''get user description with with user = user_id (or current user if user_id is None)'''
        parameters = {"access_token": self.TOKEN,
                      "user_ids": self.user_id if user_id is None else user_id,
                      "v": "5.122"}
        response = requests.get(url=self.VKAPI_URL +
                                "users.get", params=parameters)
        return response.json()

    def print_user_info(self, user_id=None):
        '''print user information with user = user_id (or current user if user_id is None)
        <user_id>: <first_name> <last_name>'''
        user_info = self.get_user_info(
            self.user_id if user_id is None else user_id)
        print(
            f"{user_info['response'][0]['id']}: {user_info['response'][0]['first_name']} {user_info['response'][0]['last_name']}")

    def get_friends(self, user_id=None):
        '''return set with friends id of  user = user_id (or current user if user_id is None)'''
        parameters = {"access_token": self.TOKEN,
                      "user_id": self.user_id if user_id is None else user_id,
                      "v": "5.122"}
        response = requests.get(url=self.VKAPI_URL +
                                "friends.get", params=parameters)
        return set(response.json()["response"]["items"])

    def __and__(self, other_VK_user):
        '''overriding the "&" method. Method returns a list of class' objects referring to mutual friends current user and other_VK_user'''
        common_friends = list()
        friends = self.get_friends() & other_VK_user.get_friends()

        for friend in friends:
            common_friends.append(VKUser(friend))
        return common_friends

    def _get_biggest_photo(self, photos_description):
        ''' return url the biggest photo from photos_description collection'''

        for size in self.PICTURE_SIZES:
            for photo_description in photos_description:
                if photo_description["type"] == size:
                    # ------ EXIT!!! ------
                    return {"size": size,
                            "url": photo_description["url"],
                            "file_type": photo_description["url"].rsplit(".", 1)[-1]
                            }

        return dict()  # ------ EXIT!!! ------

    def get_last_n_biggest_photos(self, user_id: int = None, album_id: str = "profile", num_photos: int = 0):
        """ Get last count=num_photos from album_id of user_id

        Args:
            user_id (int, optional): VK user id. Defaults to None.
            album_id (str, optional): Album in VK, where photos located. Defaults to "profile".
            num_photos (int, optional): number of photos to be downloaded. Defaults to 0.

        Returns:
            [list of dict]: photos:
                ["likes"] - number of likes
                ["date_vk"] - uploading date of photo 
                ["date_num"] - a number representation of uploading date of photo (YYYYMMDD)
                ["date_hum"] - a human representation of uploading date of photo (YYYYMMDDHHMISS)
                ["size"] - a character representation of photo size 
                ["url"] - direct URI of file
                ["file_type"] - extension of photo
                ["file_name"] - name of photo
        """

        print(f"Вконтакте: запрошены последние {num_photos} фотографий")
        parameters = {"access_token": self.TOKEN,
                      "user_id": self.user_id if user_id is None else user_id,
                      "v": "5.122",
                      "album_id": album_id,
                      "extended": 1,
                      "photo_sizes": 1,
                      "rev": 1}
        if num_photos != 0:
            parameters["count"] = num_photos
        response = requests.get(url=self.VKAPI_URL +
                                "photos.get", params=parameters)
        if response.json()["response"]["count"] == 0:
            return list()
        items = response.json()["response"]["items"]
        photos = list()

        for item in items:
            photo = dict()
            photo["likes"] = item["likes"]["count"]
            photo["date_vk"] = item["date"]
            photo["date_hum"] = datetime.fromtimestamp(
                item["date"]).strftime('%Y%m%d')
            photo["datetime_hum"] = datetime.fromtimestamp(
                item["date"]).strftime('%Y%m%d%H%M%S')
            photo.update(self._get_biggest_photo(item["sizes"]))
            photo["file_name"] = str(photo["likes"]) + \
                "." + photo["file_type"]  # likes.ext
            photos.append(photo)

        return photos


if __name__ == '__main__':
    kmu = VKUser(35163310)
    photos = kmu.get_last_n_biggest_photos(num_photos=5)
    print(photos)
