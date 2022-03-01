#!/usr/bin/python3

from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from logging import INFO, basicConfig, getLogger
from urllib.request import Request, urlopen
from pathlib import Path
from sys import argv

# Logger configuration
basicConfig(level=INFO, format='[%(levelname)s][%(asctime)s] %(message)s')
log = getLogger(Path(__file__).name)

# CONST
PAGE_OFFSET = 1 # first book page on website is one
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
arg_engine.add_argument('-j', '--jobs', type=int, dest='jobs', default=1, help='specifies amount of jobs that will be used for downloading')
arg_engine.add_argument('-f', '--force', dest='force', help='if given, overrides files in directory', **BOOL_PARAM)
args = arg_engine.parse_args(list(argv[1:]))

# ----------------------------------
bookId = args.book_id # book ID
pages_cnt = args.pages # book page ccount
max_page = pages_cnt + PAGE_OFFSET
datadir = Path(args.datadir) # path to directory with downloads
override_files = args.force # override existing directory
prefix = args.prefix
workers = args.jobs
# ----------------------------------

def retrive_image(url, path):
	"""save content received from given url to given path"""
	response = urlopen(Request(url, headers=HEADERS, method='GET'))
	with open(path, 'wb') as fhandle:
		fhandle.write(response.read())

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

def handle_range(start, stop):
	for page_num in range(start, stop):
		handle_page(page_num)

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

page_stop_range = max_page + 1
pages_per_worker = int(page_stop_range / workers)
with ThreadPoolExecutor(max_workers=workers) as executor:
	futures = []
	for i in range(PAGE_OFFSET, page_stop_range, pages_per_worker):
		futures.append(executor.submit(handle_range, i, min(max_page, i + pages_per_worker)))

	for future in futures:
		exc = future.exception()
		assert exc is None, f'job finished with exception: {exc}'
