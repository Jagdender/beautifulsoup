# -*- coding: utf-8 -*-
"""Tests for iterating over BeautifulSoup documents."""

from bs4 import BeautifulSoup
from bs4.element import Comment, Doctype

from . import SoupTest


class TestIterableSoup(SoupTest):
    def test_iteration_over_empty_soup(self):
        soup = self.soup("")

        assert [] == list(soup)

    def test_iteration_over_tags(self):
        soup = self.soup("<p></p><div></div>")

        assert [soup.p, soup.div] == list(soup)

    def test_iteration_over_nested_tags(self):
        soup = self.soup("<div><span><b>text</b></span></div>")

        assert [soup.div, soup.span, soup.b, soup.b.string] == list(soup)

    def test_iteration_over_text_nodes(self):
        soup = self.soup("before<b>inside</b>after")

        assert ["before", soup.b, "inside", "after"] == list(soup)

    def test_iteration_over_special_nodes(self):
        soup = self.soup("<!DOCTYPE html><!-- comment --><p>text</p>")

        nodes = list(soup)
        assert isinstance(nodes[0], Doctype)
        assert isinstance(nodes[1], Comment)
        assert nodes[2] is soup.p
        assert nodes[3] == "text"
