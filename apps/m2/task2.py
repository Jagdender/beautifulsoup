import sys
from bs4 import BeautifulSoup, SoupStrainer

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <filepath>")
    sys.exit(1)

with open(sys.argv[1]) as file:
    soup = BeautifulSoup(file, 'html.parser')

for i in soup.find_all(SoupStrainer("a")):
    print(i)