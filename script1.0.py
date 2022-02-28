#!/usr/bin/python3

import os
from urllib import request
from argparse import ArgumentParser
from sys import argv

arg_engine = ArgumentParser()
arg_engine.add_argument('-b','--book-id', type=int, target='book_id', required=True, help='id of book to download')
arg_engine.add_argument('-p','--pages', type=int, target='pages', required=True, help='amount of pages to download')
args = arg_engine.parse_args(list(argv[1:]))

# ----------------------------------
bookId = args.book_id # ID książki
pages = args.pages # liczba stron książki
# ----------------------------------

opener = request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
request.install_opener(opener)
pageText = "pages/page"
fileExtension = ".PNG"

os.mkdir("pages")
for i in range (1,int(pages) + 1):
  print("https://flipbook.apps.gwo.pl/book/getImage/bookId:" + str(bookId) + "/pageNo:" + str(i))
  filename = pageText + str(i) + fileExtension
  image_url = "https://flipbook.apps.gwo.pl/book/getImage/bookId:" + str(bookId) + "/pageNo:" + str(i)
  request.urlretrieve(image_url, filename)
  print("   " + filename)
