from .engine import XPlant, ModelNode


class PYamlNode(ModelNode):
    _single_indent = '  '

    def string_items(self, tree_level):
        representation = "{} - {}".format(self._single_indent * tree_level, self.own_value)
        if self.children:
            representation += ":"
        yield representation + "\n"

        for child in self.children:
            for item in child.string_items(tree_level + 1):
                yield item


class PYamlPlant(XPlant):
    regular_node_type = PYamlNode
    leaf_node_type = PYamlNode
