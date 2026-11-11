# Milestone-3

## Context

The m2 API is a focused pair substitution:

```python
SoupReplacer("b", "blockquote")
```

It is easy to discover and use, and it is a good fit for a single,
unconditional tag-name replacement. However, it cannot express conditional
changes, attribute changes, or transformations that depend on the complete
`Tag` object. Users who need those capabilities must parse first and walk the
tree afterward, which adds a second pass and can make transformations interact
poorly with parser-created structure.

The m3 API adds parser-time callbacks:

```python
SoupReplacer(
    name_xformer=lambda tag: "blockquote" if tag.name == "b" else tag.name,
    attrs_xformer=lambda tag: {**tag.attrs, "class": "test"},
    xformer=lambda tag: tag.attrs.pop("class", None),
)
```

`name_xformer` returns the replacement name, `attrs_xformer` returns the
replacement attributes, and `xformer` performs side effects directly on the
newly created tag. These callbacks receive the tag while it is being parsed,
so nested content is still handled by BeautifulSoup's normal parser flow.

## Comparison

| Concern | m2 pair API | m3 transformer API |
| --- | --- | --- |
| Simplicity | Excellent for one fixed rename | More concepts to learn |
| Tag-name changes | One unconditional mapping | Conditional or computed |
| Attribute changes | Not supported | Replacement or removal |
| Side effects | Not supported | Supported through `xformer` |
| Compatibility | Existing positional calls | Can preserve m2 calls |
| Risk | Small, predictable behavior | User callback errors and mutation semantics |

## Recommendation

I recommend keeping both interfaces, with the m2 positional form as a
backward-compatible convenience and the m3 callback form as the extensibility
API. This gives simple replacements a short path while avoiding a growing
constructor full of narrowly scoped replacement options.

For a production extension, I would make the callback arguments explicitly
keyword-only, document their execution order, and validate callback results
early. In particular:

1. Apply the name callback, then the attributes callback, then the side-effect
   callback.
2. Require `name_xformer` to return a valid tag name.
3. Require `attrs_xformer` to return a mapping and normalize multi-valued
   attributes using the active builder.
4. State clearly that callbacks run once per parsed start tag and that
   exceptions abort parsing rather than being silently ignored.
5. Keep end-tag matching based on the original parser name internally, so a
   renamed tag cannot corrupt the open-tag stack.

The callback API is the better long-term foundation because it separates the
stable parser integration from the policy supplied by users. It should not,
however, replace the m2 shorthand: the shorthand remains valuable for
readability, compatibility, and the common case where a declarative
name-to-name mapping is all that is needed.
