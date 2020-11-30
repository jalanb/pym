# flake8: noqa

from visitors import default_visitors_map

class Example(object):
    all_examples = []  # class attr

    def __init__(
        self,
        name,
        content,
        visitor_map=default_visitors_map.copy(),
        input_encoding="utf-8",
    ):
        self.name = name
        self.content = content
        self.visitor_map = visitor_map
        self.input_encoding = input_encoding
        Example.all_examples.append(self)

    def show(self):
        print('-'*80)
        print('## Output from example:', self.name)
        print()
        serializer = Serializer(self.visitor_map, self.input_encoding)
        output = serializer.serialize(self.content)
        print(output.encode(get_default_encoding()))


Example(
    "Standard python types, no html",
    [
        1,
        2,
        3,
        4.0,
        "a",
        "b",
        ("c", ("d", "e"), set(["f", "f"])),  # nested
        (i * 2 for i in xrange(10)),
    ],
)
# output = '1234.0abcdef024681012141618'

Example(
    "Standard python types, no html *or* html escaping",
    [1, "<", 2, "<", 3],
    visitor_map=default_visitors_map,
)
# output = '1<2<3'
