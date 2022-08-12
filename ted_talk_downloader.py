# TED TALK video downloader script using python

import requests  # for getting content
from bs4 import BeautifulSoup  # webscraping for urls to download
import re  # pattern matching
import sys  # passing arguments

# if you want to use command line instead of direct url
# if len(sys.argv) > 1:
#     url = sys.argv[1]
# else:
#     sys.exit('Error! Enter the url to TED Talk')

# sample url

# https://www.ted.com/talks/eleni_myrivili_a_3_part_plan_to_take_on_extreme_heat_waves


# get the content of the url
url = "https://www.ted.com/talks/ayana_elizabeth_johnson_how_to_find_joy_in_climate_action"

r = requests.get(url)

print('Download about to start!...')

# scraping details about the video.

soup = BeautifulSoup(r.content, features='lxml')

for val in soup.findAll("script"):
    if (re.search("https", str(val))) is not None:
        result = str(val)

result_mp4 = re.search("(?P<url>https?://[^\s]+)(mp4)", result).group("url")

mp4_url = result_mp4.split('"')[0]

print('Downloading video from ' + mp4_url)

file_name = mp4_url.split("-")[:len(mp4_url.split("/"))-1][1:-2]
file_name = '_'.join(file_name)
file_name += '.mp4'

print(f'file name: {file_name}')
print(mp4_url)

print('Downloading the file')

video = requests.get(mp4_url+'mp4')


with open(file_name, 'wb') as f:
    f.write(video.content)

print('Download Complete..!')
