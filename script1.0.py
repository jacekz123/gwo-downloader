#!/usr/bin/python3

import os
from urllib import request
from argparse import ArgumentParser
from sys import argv
from logging import Logger, INFO

log = Logger(__file__, level=INFO)

# CONST
BOOL_PARAM = dict(nargs='?', type=bool, const=True, default=False)

arg_engine = ArgumentParser()
arg_engine.add_argument('-b', '--book-id', type=int, dest='book_id', required=True, help='id of book to download')
arg_engine.add_argument('-p', '--pages', type=int, dest='pages', required=True, help='amount of pages to download')
arg_engine.add_argument('-d', '--datadir', type=str, dest='datadir', default='pages', required=False, help='specifies directory where pages will be scrapped')
arg_engine.add_argument('-f', '--force', dest='force', help='if given, overrides files in directory', **BOOL_PARAM)
args = arg_engine.parse_args(list(argv[1:]))

# ----------------------------------
bookId = args.book_id # book ID
pages = args.pages # book page ccount
datadir = args.datadir # path to directory with downloads
override_files = args.force # override existing directory
# ----------------------------------

opener = request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
request.install_opener(opener)
pageText = "pages/page"
fileExtension = ".PNG"

if os.path.exists(datadir):
	if not override_files:
		log.warning('directory already exist, change path or remove existing one')
		exit(-1)
else:
	try:
		os.mkdir(datadir)
	except Exception as e:
		log.error(f'exception occured while creating directory: {e}')

for i in range (1,int(pages) + 1):
  print("https://flipbook.apps.gwo.pl/book/getImage/bookId:" + str(bookId) + "/pageNo:" + str(i))
  filename = pageText + str(i) + fileExtension
  image_url = "https://flipbook.apps.gwo.pl/book/getImage/bookId:" + str(bookId) + "/pageNo:" + str(i)
  request.urlretrieve(image_url, filename)
  print("   " + filename)
