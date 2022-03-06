import urllib.request
import os
opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)
pageText = "pages/page"
fileExtension = ".PNG"

# ----------------------------------
bookId = 2350 # ID książki
pages = 5 # liczba stron książki
# ----------------------------------

os.mkdir("pages")
for i in range (1,int(pages) + 1):
  print("https://flipbook.apps.gwo.pl/book/getImage/bookId:" + str(bookId) + "/pageNo:" + str(i))
  filename = pageText + str(i) + fileExtension
  image_url = "https://flipbook.apps.gwo.pl/book/getImage/bookId:" + str(bookId) + "/pageNo:" + str(i)
  urllib.request.urlretrieve(image_url, filename)
  print("   " + filename)
