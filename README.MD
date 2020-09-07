# Task: Download last the biggest size photos from member of social network vk.com (*\<be> in touch*) and upload them to Yandex Disk new folder. 
## Description: the template of file name is \<count_of_likes>.\<ext>. If the same number of likes are found, download date must be added to the file names. Also need to write a json file with file upload information (file name and image size). The new Yandex Disk folder's template is \"img_from_vk_id\<VK_user_id>\_dt\<current datetime in YYYYMMDDHHMISS format>"

## Warning! Task was changed: it is possible situation when photos uploaded at the same date and had the same count of likes. At this case adding upload date will cause an error, so I add upload datetime.

### Class VKUser
#### Description:
Method	  | Parameters | Return type|Description
:-------- |:-----:|:-----:|:-------
\_\_init__ 		 	| user_id:int  | -|Second method during Class creation
\_\_str__     		| -    |_str_|string representation of the Class - link to the homepage of user
print_user_id      	| user_id=None:int    |-| print user id with user = user_id (or current user if user_id is None)
get_user_info		|user_id=None:int|_json_ of VK.users.get|get user description with with user = user_id (or current user if user_id is None)
print_user_info		|user_id=None:int|-|print user information with user = user_id (or current user if user_id is None)  <user_id>: <first_name> <last_name>
get_friends			|user_id=None:int|_set_ of VK id|return set with friends id of  user = user_id (or current user if user_id is None)
\_\_and__			|other_VK_user:VKUser|_list_ of VKUser objects|overriding the "&" method. Method returns a list of class' objects referring to mutual friends current user and other_VK_user
get_last_n_biggest_photos|user_id=None:int, album_id="profile":st, num_photos=0:int|_list_ of photos info|Get last count=num_photos from album_id of user_id

#### Example of using VKUser Class:
```python
    user1 = VKUser(11111111)
    photos = user1.get_last_n_biggest_photos(num_photos=num_last_photos)
```

### Class YaUploader
#### Description:
Method	  | Parameters | Return type|Description
:-------- |:-----:|:-----:|:-------
\_\_init__ 		 	| yandex_token: str  | -|Second method during Class creation
upload_local_file	|local_file_path_name:str, ydisk_file_path_name=None:str|_dict_ with result of execution|upload local_file_path_name (path and file_name) from local computer as ydisk_file_path_name (path and file_name)
upload_url_file		|url_file_web:str, ydisk_file_path_name=None:str|_dict_ with result of execution|upload file from url (url_file_web) as ydisk_file_path_name (path and file_name)
create_folder		|ydisk_path:str|_dict_ with result of execution|create folder as ydisk_path (path from the root of yandex disk)

#### Example of using YaUploader Class:
```python
    uploader = YaUploader("some Yandex Disk token")
    result = uploader.create_folder("/testfolder6")
```


#### log:
```log
      Введите id пользователя Вконтакте: 35163310
      Введите токен Яндекса: ********
      Вконтакте: получены последние 5 фотографий
      Я.Диск: создана папка /img_from_vk_id35163310_dt20200907234019
      Я.Диск: файл /img_from_vk_id35163310_dt20200907234019/9.jpg вскоре будет загружен
      Я.Диск: файл /img_from_vk_id35163310_dt20200907234019/5.jpg вскоре будет загружен
      main: информация о файлах сохранена в img_from_vk_id35163310_dt20200907234019_data.json
```





