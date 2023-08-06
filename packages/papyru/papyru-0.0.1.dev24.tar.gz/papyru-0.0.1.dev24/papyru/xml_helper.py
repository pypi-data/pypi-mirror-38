import xml.etree.ElementTree as ET
from functools import reduce
from io import StringIO


class XMLHelper:
    def __init__(self, encoded_xml):
        self._namespaces = (
            _collision_free_dict(map(lambda el: el[1],
                                     ET.iterparse(StringIO(encoded_xml),
                                                  events=['start-ns']))))

        self._document = ET.parse(StringIO(encoded_xml))

        for namespace in self._namespaces.items():
            # ns\d+ namespaces are reserved for internal use
            # ns0 conforms to the default namespace (is set i.a. by IE )
            # that's why we replace it with an empty string
            # the other ns\d+ namespaces should not appear
            # ElementTree will throw an error if they do
            ET.register_namespace(
                namespace[0] if namespace[0] != 'ns0' else '', namespace[1])

    @property
    def root(self):
        return self._document.getroot()

    def namespace(self, shortname):
        return self._namespaces.get(shortname, None)

    def deep_copy(self):
        return XMLHelper(self.serialize(self.root).decode('utf-8'))

    @property
    def default_namespace(self):
        return self._namespaces.get('', None)

    def attribute_fullname(self, name, namespace=None):
        return ('{%s}%s' % (self.namespace(namespace), name)
                if namespace is not None
                else name)

    def get_attribute(self, node, name, namespace=None):
        try:
            return node.attrib[self.attribute_fullname(name, namespace)]
        except KeyError:
            return None

    def set_attribute(self, node, name, value, namespace=None):
        node.attrib[self.attribute_fullname(name, namespace)] = value

    def del_attribute(self, node, name, namespace=None):
        del node.attrib[self.attribute_fullname(name, namespace)]

    def has_attribute(self, node, name, namespace=None):
        return self.attribute_fullname(name, namespace) in node.attrib

    def serialize(self, node):
        return ET.tostring(node)


def _collision_free_dict(kv_iter):
    class State:
        def __init__(self):
            self.accumulator = {}
            self.suffix_counter = 0

        def put(self, key, value):
            # Namespaces starting with xml are reserved for extensions by w3c.
            # Writing it with suffixes into the xml is therefore not allowed
            if (key.startswith('xml') and key in self.accumulator):
                return self

            use_key = (key
                       if key not in self.accumulator
                       else self.with_suffix(key))

            self.accumulator[use_key] = value
            return self

        def with_suffix(self, key):
            self.suffix_counter = self.suffix_counter + 1
            return ('%s_%s' % (key, self.suffix_counter)
                    if key != ''
                    else 'userDefinedNamespace%s' % self.suffix_counter)

    def add_to_dict(state, kv):
        key, value = kv
        return state.put(key, value)

    return reduce(add_to_dict, kv_iter, State()).accumulator
