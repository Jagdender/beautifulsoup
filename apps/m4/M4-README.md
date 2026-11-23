# Milestone 4: Iterable BeautifulSoup

`BeautifulSoup` objects are iterable. Iterating over a soup traverses its
parsed tree in document order and yields each descendant node, including tags,
text nodes, comments, and doctypes:

```python
soup = BeautifulSoup(html_doc, "html.parser")
for node in soup:
    print(node)
```

Iteration is lazy: it uses the existing descendant generator and does not
collect the tree into a list before yielding nodes. An empty document therefore
produces no nodes.

The iteration behavior is covered by five tests in
`bs4/tests/test_iterable.py`, including empty, flat, nested, text, and special
node trees.
