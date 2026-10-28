from . import SoupTest
from bs4.replacer import SoupReplacer


class TestSoupReplacer(SoupTest):
    def test_replaces_tags_during_parsing(self):
        soup = self.soup(
            '<p><b class="important">text <b>nested</b></b><i>unchanged</i></p>',
            replacer=SoupReplacer("b", "blockquote"),
        )

        assert (
            '<p><blockquote class="important">text <blockquote>nested</blockquote>'
            '</blockquote><i>unchanged</i></p>'
            == soup.decode()
        )
        assert soup.find_all("b") == []

    def test_replacer_preserves_attributes_and_nonmatching_tags(self):
        soup = self.soup(
            '<b id="first">one</b><strong id="second">two</strong>',
            replacer=SoupReplacer("b", "blockquote"),
        )

        assert soup.blockquote["id"] == "first"
        assert soup.strong["id"] == "second"
        assert soup.strong.string == "two"
