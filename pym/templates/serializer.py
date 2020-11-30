class Serializer(object):
    """A tree walker that uses the visitor pattern to serialize what
    it walks into properly escaped unicode.
    """

    def __init__(self, visitor_map=None, input_encoding=None):
        if visitor_map is None:
            visitor_map = default_visitors_map.copy()
        self.visitor_map = visitor_map
        self.input_encoding = input_encoding or get_default_encoding()
        self._safe_unicode_buffer = []

    def serialize(self, obj):
        """Serialize an object, and its children, into sanitized unicode."""
        self._safe_unicode_buffer = []
        self.walk(obj)
        return safe_unicode(u"".join(self._safe_unicode_buffer))

    def walk(self, obj):
        """This method is called by visitors for anything they
        encounter which they don't explicitly handle.
        """
        visitor = self.visitor_map.get_visitor(obj)
        if visitor:
            visitor(obj, self)  # ignore return value
        else:
            raise TypeError("No visitor found for %s" % repr(obj))

    def emit(self, escaped_unicode_output):
        """This is called by visitors when they have escaped unicode
        to output.
        """
        self._safe_unicode_buffer.append(escaped_unicode_output)

    def emit_many(self, output_seq):
        self._safe_unicode_buffer.extend(output_seq)
