import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from bs4 import BeautifulSoup, SoupReplacer


if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <filepath>")
    sys.exit(1)


def set_test_class(tag):
    attrs = dict(tag.attrs)
    attrs["class"] = "test"
    return attrs


with open(sys.argv[1]) as file:
    soup = BeautifulSoup(
        file,
        "html.parser",
        replacer=SoupReplacer(
            attrs_xformer=lambda tag: set_test_class(tag)
            if tag.name == "p"
            else tag.attrs
        ),
    )

with open("result.html", "w+") as file:
    file.write(soup.prettify())
