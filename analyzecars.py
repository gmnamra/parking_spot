import argparse
import os
import requests
from fetchandextract import fetch_url_first_frame
from hascar import process
from pathlib import Path
from spot import SpotObserver

BASEURL = 'https://hiring.verkada.com/video'
##time.ctime(int("1284101485"))



class analyzecars:

    def __init__(self, base_url, index_url, first_index, last_index):
        self.base_url = base_url
        self.index_url = index_url
        self.cwd = os.getcwd()
        if Path(index_url).exists():
            fo = open(index_url, "r+")
            self.listing = fo.readlines()

        if len(self.listing) == 0:
            r = requests.get(self.base_url + '.txt')
            decoded_content = r.content.decode('utf-8')
            self.listing = decoded_content.splitlines()

        # Create list of video files we have to process
        self.first = int(first_index)
        self.last = int(last_index)
        self.nlisting = list(map(lambda x: int(x.rstrip()[:-3]), self.listing))
        self.nbatch = [x for x in self.nlisting if x >= self.first and x <= self.last]
        self.batch = list(map(lambda x: str(x) + '.ts', self.nbatch))

        # Instantiate a spot observer
        self.pp = SpotObserver()

        dwp = Path('__down_loads__')
        if not dwp.exists():
            dwp.mkdir()

        car = 'car'
        for idx, file in enumerate(self.batch):
            down_info = fetch_url_first_frame(self.base_url, file, str(dwp))
            found = process(down_info[1], False)
            self.pp.update(found,self.nbatch[idx])
            # print(self.pp.report())

        self.pp.reportAll()



def main():
    parser = argparse.ArgumentParser(description='analyze-cars')
    parser.add_argument('--index', '-i', required=True, help='Index File ')
    parser.add_argument('--start', '-s', required=True, help='Starting time stamp')
    parser.add_argument('--end', '-e', required=True, help='Last time stamp')

    args = parser.parse_args()

    place = analyzecars(BASEURL, args.index, args.start, args.end)


if __name__ == '__main__':
    main()

# def fetch_frames(index_array, start_index, end_index, sampling=None):
