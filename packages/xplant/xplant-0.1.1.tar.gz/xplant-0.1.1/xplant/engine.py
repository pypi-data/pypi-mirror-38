from contextlib import contextmanager


class ModelNode(object):
    """
        Sequential node can describe itself in the document, yields markup items of itself and its children.
    """
    _empty_iterator = iter(())
    __slots__ = ("own_value", "children")

    def __init__(self, value):
        self.own_value = value
        self.children = []

    def __str__(self):
        return "".join(k for k in self.string_items(0) if k)

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self.own_value)

    def append_child_node(self, new_node_obj, plant):
        if not isinstance(new_node_obj, ModelNode):
            raise TypeError("Can append only instances of ModelNode, got {}.".format(type(new_node_obj).__name__))

        self.children.append(new_node_obj)

    @property
    def degree(self):
        """ For a given node, its number of children. A leaf is necessarily degree zero. """
        return len(self.children)

    @property
    def height(self):
        """ The height of a node is the number of edges on the longest path between that node and a leaf. """
        if not self.children:
            return 0
        else:
            return 1 + max(child.height for child in self.children)

    def string_items(self, tree_level):
        msg = "\n".join([
            "ModelNode.string_items is an abstract method.", "",
            "It's supposed to:",
            " - be a generator yielding string items,",
            " - compose document representation of that node with ''.join(node.string_items(0)),",
            " - care for document's line breaks, markup and indentation.",
            "It needs to be implemented in derived class {name!r}.",
            ""
        ])
        raise NotImplementedError(msg.format(name=self.__class__.__name__))


class RootNodeType(ModelNode):
    """
        Root node in current implementation has no owb value, no head nor tail markup.
        It's just a children's container.
    """

    def __init__(self):
        super(RootNodeType, self).__init__(None)

    def string_items(self, _):
        for child in self.children:
            for item in child.string_items(tree_level=0):
                yield item
        if self.children:
            yield "\n"


class LeafNodeType(ModelNode):
    """ Leaf - a node that is not allowed to have children. """

    def append_child_node(self, new_node_obj, plant):
        raise AttributeError("{} is not allowed to append any children".format(self.__class__.__name__))


class XPlant(object):
    _root_node_type = RootNodeType
    regular_node_type = ModelNode
    leaf_node_type = LeafNodeType

    def __init__(self):
        self.__tag_stack = [self._root_node_type()]

    def __str__(self):
        return str(self.__tag_stack[0])

    def __getattr__(self, attr_name):
        """ It exposes interface of current _top_node object. """
        if not attr_name.startswith("_") and hasattr(self._top_node, attr_name):
            return getattr(self._top_node, attr_name)
        return super(XPlant, self).__getattribute__(attr_name)

    @property
    def _top_node(self):
        """ The node whose context we are currently in. """
        return self.__tag_stack[-1]

    @contextmanager
    def node(self, *args, **kwargs):
        new_node = self.regular_node_type(*args, **kwargs)
        self._top_node.append_child_node(new_node, self)
        self.__tag_stack.append(new_node)
        try:
            yield
        finally:
            self.__tag_stack.pop()

    def leaf(self, *args, **kwargs):
        new_node = self.leaf_node_type(*args, **kwargs)
        self._top_node.append_child_node(new_node, self)

    @contextmanager
    def descent(self, new_node_obj):
        """ Register a new child node to the current self._top_node and enter its scope/context. """
        self._top_node.append_child_node(new_node_obj)

        self.__tag_stack.append(new_node_obj)
        try:
            yield
        finally:
            self.__tag_stack.pop()
