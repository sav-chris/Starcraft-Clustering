
import urllib.request
import glob
from typing import List
import zipfile
import os


data_dest_dir: str = "../data/unziped" 


def scrape_spawning_tool(page_count: int)->None:

    url: str = "https://lotv.spawningtool.com/zip/?order_by=&query=&before_time=&patch=150&adv=1&after_time=&coop=n&before_played_on=&tag=7&after_played_on=&pro_only=on&p={0}"
    fileName: str = "../data/replay{0}.zip"

    for i in range(1, page_count + 1):
        urllib.request.urlretrieve(url.format(i), fileName.format(i))
        print(i)

def unzip_file(filename: str, dest_directory: str)->None:
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(dest_directory)


def unzip_replays(directory: str)->None:

    data_files: List[str] = glob.glob(directory)
    for file in data_files:
        unzip_file(file, data_dest_dir)
        print(data_files)

def cleanup(directory: str)->None:
    data_files: List[str] = glob.glob(directory)
    for file in data_files:
        os.remove(file)

if __name__ == "__main__":
    scrape_spawning_tool(10)
    unzip_replays("../data/replay*.zip")
    cleanup("../data/replay*.zip")



    
