from .engine import XPlant, ModelNode
from ._xml_attributes import XmlAttributes


class Text(ModelNode):
    def string_items(self, tree_level):
        yield self.own_value


class Comment(ModelNode):
    def string_items(self, tree_level):
        yield "<!-- %s -->" % self.own_value


class CdataTag(ModelNode):
    def string_items(self, tree_level):
        return "<![CDATA[%s]]>" % self.own_value


class _XmlElementBaseNode(ModelNode):
    attribute_processor = XmlAttributes
    _force_inline = False
    __slots__ = ("attributes",)

    def __init__(self, tag_name, *args, **kwargs):
        super(_XmlElementBaseNode, self).__init__(tag_name)
        self.attributes = self.attribute_processor(*args, **kwargs)


class EmptyXmlElement(_XmlElementBaseNode):
    """ E.g.: <br />, <hr /> or <img src="#" alt="" /> """

    def append_child_node(self, new_node_obj, plant):
        raise AttributeError("Cannot append to {} node.".format(self.__class__.__name__))

    def string_items(self, tree_level):
        yield "<{}{} />".format(self.own_value, self.attributes)


class XmlElement(_XmlElementBaseNode):
    _single_indent_val = "  "

    def string_items(self, tree_level):
        yield "<{}{}>".format(self.own_value, self.attributes)

        for item in self._childrens_markup(tree_level):
            yield item

        yield "</{}>".format(self.own_value)

    def _childrens_markup(self, tree_level):
        break_lines = self.degree > 1 and not self._force_inline
        child_indent = self._make_indent(tree_level + 1)

        for child in self.children:
            if break_lines:
                yield child_indent

            for child_string in child.string_items(tree_level + 1):
                yield child_string

        if break_lines:
            yield self._make_indent(tree_level)

    @classmethod
    def _make_indent(cls, tree_level):
        return "\n" + cls._single_indent_val * tree_level


class XmlPlant(XPlant):
    regular_node_type = XmlElement
    leaf_node_type = EmptyXmlElement

    def text(self, *text):
        for t in text:
            self.append_child_node(Text(t), self)

    def line(self, tag_name, content, *args, **kwargs):
        """ Element containing just a text. """
        with self.node(tag_name, *args, **kwargs):
            self.append_child_node(Text(content), self)

    def cdata(self, content):
        self.append_child_node(CdataTag(content), self)

    def comment(self, content):
        self.append_child_node(Comment(content), self)
