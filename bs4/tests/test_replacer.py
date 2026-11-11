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

    def test_name_xformer_replaces_tag_names_during_parsing(self):
        soup = self.soup(
            "<p><b>bold <i>text</i></b></p>",
            replacer=SoupReplacer(
                name_xformer=lambda tag: "blockquote"
                if tag.name == "b"
                else tag.name
            ),
        )

        assert soup.decode() == "<p><blockquote>bold <i>text</i></blockquote></p>"

    def test_name_xformer_receives_each_tag(self):
        seen = []

        def record_name(tag):
            seen.append(tag.name)
            return tag.name

        self.soup("<p><b>text</b></p>", replacer=SoupReplacer(name_xformer=record_name))

        assert seen == ["p", "b"]

    def test_attrs_xformer_replaces_attributes(self):
        soup = self.soup(
            '<p class="old" id="keep">text</p>',
            replacer=SoupReplacer(
                attrs_xformer=lambda tag: {"class": "new"}
                if tag.name == "p"
                else tag.attrs
            ),
        )

        assert soup.p.attrs == {"class": ["new"]}

    def test_attrs_xformer_can_remove_attributes(self):
        def without_class(tag):
            return {
                name: value for name, value in tag.attrs.items() if name != "class"
            }

        soup = self.soup(
            '<p class="remove" id="keep">text</p>',
            replacer=SoupReplacer(attrs_xformer=without_class),
        )

        assert soup.p.attrs == {"id": "keep"}

    def test_xformer_can_mutate_tag_as_a_side_effect(self):
        def remove_class(tag):
            tag.attrs.pop("class", None)

        soup = self.soup(
            '<p class="remove">text</p>',
            replacer=SoupReplacer(xformer=remove_class),
        )

        assert soup.p.attrs == {}

    def test_transformers_work_together_and_preserve_nesting(self):
        def add_marker(tag):
            tag.attrs["data-seen"] = "yes"

        soup = self.soup(
            '<b class="important"><i>text</i></b>',
            replacer=SoupReplacer(
                name_xformer=lambda tag: "blockquote"
                if tag.name == "b"
                else tag.name,
                attrs_xformer=lambda tag: tag.attrs,
                xformer=add_marker,
            ),
        )

        assert soup.decode() == (
            '<blockquote class="important" data-seen="yes">'
            '<i data-seen="yes">text</i></blockquote>'
        )
