import json
import requests
import os
from bs4 import BeautifulSoup as bs
import subprocess


def create_main_folder_path(path):
    path_file = open('path.json', 'w')
    content = json.dumps({'path': path})
    path_file.write(content)
    path_file.close()


def get_path():
    path_file = open('path.json', 'r')
    path = json.loads(path_file.read())['path']
    path_file.close()
    return path


def get_images(google_search, google_search_dir):
    r = requests.get(
        "https://www.google.com/search?q={}&source=lnms&tbm=isch".format(google_search))
    if r.status_code == 200:
        soup = bs(r.text, 'html.parser')
        counter = 0
        for link in soup.find_all('img', attrs={'class': 't0fcAb'}):
            if counter == 10:
                break
            r = requests.get(link.get('src'))
            image_file = open(
                google_search_dir + "\\{}.png".format(counter+1), "wb")
            image_file.write(r.content)
            image_file.close()
            counter += 1


def open_file_explorer(dir_path):
    subprocess.Popen('explorer {}'.format(os.path.normpath(dir_path)))


def main():
    if not os.path.isfile('path.json'):
        create_main_folder_path(
            "Enter path for the main folder which you wish to store the images in: ")
    path = get_path()
    google_search = input("Search for image: ")
    google_images_dir = "{}\\GoogleImages".format(path)
    google_search_dir = google_images_dir + "\\{}".format(google_search)
    if not os.path.isdir(google_images_dir):
        os.mkdir(google_images_dir)
    if not os.path.isdir(google_search_dir):
        os.mkdir(google_search_dir)
    get_images(google_search, google_search_dir)
    open_file_explorer(google_search_dir)


main()
