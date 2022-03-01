#!/usr/bin/python3

from requests import get
from urllib import request
from argparse import ArgumentParser
from sys import argv
from pathlib import Path

log = Logger(__file__, level=INFO)

# CONST
BASE_URL = "https://flipbook.apps.gwo.pl/book/getImage/bookId:"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'}
BOOL_PARAM = dict(nargs='?', type=bool, const=True, default=False)
IMAGE_EXT = 'png'

# ARGUMENTS
arg_engine = ArgumentParser()
arg_engine.add_argument('-b', '--book-id', type=int, dest='book_id', required=True, help='id of book to download')
arg_engine.add_argument('-p', '--pages', type=int, dest='pages', required=True, help='amount of pages to download')
arg_engine.add_argument('-d', '--datadir', type=str, dest='datadir', default='pages', required=False, help='specifies directory where pages will be scrapped')
arg_engine.add_argument('-k', '--prefix', type=str, dest='prefix', default='page_', required=False, help='specifies prefix before every page, concatenated with number and format')
arg_engine.add_argument('-f', '--force', dest='force', help='if given, overrides files in directory', **BOOL_PARAM)
args = arg_engine.parse_args(list(argv[1:]))

# ----------------------------------
bookId = args.book_id # book ID
pages = args.pages # book page ccount
datadir = Path(args.datadir) # path to directory with downloads
override_files = args.force # override existing directory
prefix = args.prefix
# ----------------------------------

def retrive_image(url, path):
	"""save content received from given url to given path"""
	response = get(url, headers=HEADERS)
	with open(path, 'wb') as fhandle:
		fhandle.write(response.content)

def generate_url(page_num) -> str:
	"""generates url for given page number"""
	return f'{BASE_URL}{bookId}/pageNo:{page_num}'

def generate_path(page_num) -> Path:
	"""generates save path for given page number"""
	return datadir / f'{prefix}{page_num}.{IMAGE_EXT}'

def handle_page(page_num):
	path = generate_path(page_num)
	log.info(f'retriving page number {page_num} into: {path}')
	url = generate_url(page_num)
	log.info(f'downloading page number {page_num} from: {url}')
	retrive_image(url, path)


# Path handling
if datadir.exists():
	if not override_files:
		log.warning('directory already exist, change path or remove existing one')
		exit(-1)
else:
	try:
		datadir.mkdir()
	except Exception as e:
		log.error(f'exception occured while creating directory: {e}')

for i in range (1,int(pages) + 1):
	handle_page(i)
