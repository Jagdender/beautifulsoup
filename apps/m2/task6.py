import sys
from bs4 import BeautifulSoup, SoupReplacer

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <filepath>")
    sys.exit(1)

with open(sys.argv[1]) as file:
    soup = BeautifulSoup(file, replacer=SoupReplacer("b", "blockquote"))

with open("result.html", 'w+') as file:
    file.write(soup.prettify())
