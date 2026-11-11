from typing import Any, Callable, Mapping, Optional

from .element import Tag


NameTransformer = Callable[[Tag], str]
AttrsTransformer = Callable[[Tag], Mapping[str, Any]]
Transformer = Callable[[Tag], None]


class SoupReplacer:
    def __init__(
        self,
        og_tag: Optional[str] = None,
        alt_tag: Optional[str] = None,
        *,
        name_xformer: Optional[NameTransformer] = None,
        attrs_xformer: Optional[AttrsTransformer] = None,
        xformer: Optional[Transformer] = None,
    ):
        if (og_tag is None) != (alt_tag is None):
            raise TypeError("og_tag and alt_tag must be provided together")

        self.og_tag = og_tag
        self.alt_tag = alt_tag
        self.name_xformer = name_xformer
        self.attrs_xformer = attrs_xformer
        self.xformer = xformer

    def transform(self, tag: Tag, original_name: str) -> None:
        """Apply the configured transformations to a newly parsed tag."""
        tag._soup_replacer_original_name = original_name

        if self.name_xformer is not None:
            tag.name = self.name_xformer(tag)
        elif self.og_tag == original_name:
            tag.name = self.alt_tag

        if self.attrs_xformer is not None:
            attrs = self.attrs_xformer(tag)
            if attrs is None:
                raise TypeError("attrs_xformer must return tag attributes")
            tag.attrs = self._attribute_dict(tag, attrs)

        if self.xformer is not None:
            self.xformer(tag)

    @staticmethod
    def _attribute_dict(tag: Tag, attrs: Mapping[str, Any]) -> Any:
        result = tag.attrs.__class__()
        universal = tag.cdata_list_attributes.get("*", set())
        tag_specific = tag.cdata_list_attributes.get(tag.name.lower(), set())
        for name, value in attrs.items():
            if (
                isinstance(value, str)
                and (name in universal or name in tag_specific)
            ):
                value = tag.attribute_value_list_class(value.split())
            result[name] = value
        return result