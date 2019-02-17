
import cv2 as cv
import argparse
import os
import requests
from pathlib import Path
import threading
import sys


def arg_parse():
    """
    Parse arguements to the detect module

    """

    parser = argparse.ArgumentParser(description='fetch-and-extract')

    parser.add_argument("--video", dest='videofile', help="Video to run detection upon", type=str)
    parser.add_argument("--fetch", dest='frame_index', help="0 based frame", default=0)
    parser.add_argument("--show", dest='show', help="Display frame", type=bool, default=False)
    parser.add_argument("--info", dest='info', help="Run Information", type=bool, default=False)

    return parser.parse_args()


def get_filename(filename):
    # determine the file extension of the current file
    slash = filename.rfind("/")

    return filename[slash + 1:]


def fetch_url_first_frame(base_url, filename, download_path, overwrite=False):
    url = base_url + os.sep + filename
    ff_name = filename[:-2] + 'jpg'
    download_fqfn = download_path + os.sep + ff_name
    donot_overwrite = not overwrite
    exists = Path(download_fqfn).exists() and donot_overwrite
    if not exists:
        msg = 'downloading ' + url + '...'
        print(msg)
        response = requests.get(url)
        content_type = response.headers['Content-Type'].split('/')[-1]
        with open(download_fqfn, 'wb') as f:
            f.write(response.content)

        cap = cv.VideoCapture(download_fqfn)
        while cap.isOpened():

            ret, frame = cap.read()
            if ret:
                orig_im = frame
                cv.imwrite(ff_name, orig_im)
                print('extracting...' + ff_name)
            break
    return (download_fqfn, ff_name)


class fetcherThread (threading.Thread):
   def __init__(self, threadID, base_url, filename, download_path, overwrite=False):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.base_url = base_url
      self.name = filename
      self.downlood_path = download_path
      self.overwrite = overwrite


   def run(self):
      print ("Starting " + self.name)
      fetch_url_first_frame(self.base_url, self.name, self.downlood_path, self.overwrite)
      print ("Exiting " + self.name)


if __name__ == '__main__':
    url = sys.argv[1]
    filename = sys.argv[2]
    file = fetch_url_first_frame(url, filename, './__down_loads__')
