import YaUploader
import GDUploader
import VKUser
import json
from datetime import datetime  # , timedelta
# import time

# YATOKEN = "there is must be a token for Yandex Disk"


def prepare_list_files(photos):
    photos_count = len(photos)
    for photo_num in range(photos_count):
        photo = photos[photo_num]
        # print(photo)
        # counter = 0
        photo["file_name"] = str(photo["likes"])
        for photo_num_same_like in range(photo_num+1, photos_count):
            if photo["likes"] == photos[photo_num_same_like]["likes"]:
                # print(photos[photo_num_same_like])
                # counter += 1
                photos[photo_num_same_like]["file_name"] = str(
                    photos[photo_num_same_like]["likes"]) + f"_{photos[photo_num_same_like]['datetime_hum']}." + photos[photo_num_same_like]["file_type"]
                photo["file_name"] = str(
                    photo["likes"]) + f"_{photo['datetime_hum']}." + photos[photo_num_same_like]["file_type"]
                # print("-----V")
                # print(photos[photo_num_same_like])
    return photos


def get_photos_from_vk_user(vk_user, num_last_photos=5):
    photos = vk_user.get_last_n_biggest_photos(num_photos=num_last_photos)
    photos = prepare_list_files(photos)
    return photos


def save_photos_information(file_name, files_information):
    with open(file_name, "w") as write_file:
        json.dump(files_information, write_file, indent=4)
    print(f"main: информация о файлах сохранена в {file_name}")


def save_photos_to_yadisk(ya_disk, folder_name, photos):
    ya_disk.create_folder("/" + folder_name)
    files_information = list()
    for photo in photos:
        ya_disk.upload_url_file(
            photo["url"], f"/{folder_name}/{photo['file_name']}")
        files_information.append(
            {"file_name": photo['file_name'], "size": photo['size']})
    save_photos_information(folder_name + "_data.json", files_information)


def save_photos_to_gdrive(gdisk, folder_name, photos):
    folder_id = gdisk.create_folder(folder_name)
    files_information = list()
    for photo in photos:
        gdisk.upload_url_file(photo["url"], folder_id)
        files_information.append(
            {"file_name": photo['file_name'], "size": photo['size']})
    save_photos_information(folder_name + "_data.json", files_information)


def main():
    user_id = int(input("Введите id пользователя Вконтакте: "))
    yandex_token = input("Введите токен Яндекса: ")

    vk_user = VKUser.VKUser(user_id)
    photos = get_photos_from_vk_user(vk_user, 5)

    ya_disk = YaUploader.YaUploader(yandex_token)
    new_folder = (
        f"img_from_vk_id{user_id}_dt{datetime.now().strftime('%Y%m%d%H%M%S')}")
    save_photos_to_yadisk(ya_disk, new_folder, photos)


def main_vk_gdisk():
    user_id = int(input("Введите id пользователя Вконтакте: "))

    social_user = VKUser.VKUser(user_id)
    photos = get_photos_from_vk_user(social_user, 5)

    gdrive = GDUploader.GDUploader()
    new_folder = (
        f"img_from_vk_id{user_id}_dt{datetime.now().strftime('%Y%m%d%H%M%S')}")
    save_photos_to_gdrive(gdrive, new_folder, photos)


main_vk_gdisk()
# 35163310
