"""
xml.py  The Node class for converting to xml,
        The NameSpace Class.
        The XmlParser class for parsing an xml string for SCTE-35 data.
        and several helper functions
"""

from xml.sax.saxutils import escape, unescape


def t2s(v):
    """
    _t2s converts
    90k ticks to seconds and
    rounds to six decimal places
    """
    return round(v / 90000.0, 6)


def un_camel(k):
    """
    camel changes camel case xml names
    to underscore_format names.
    """
    k = strip_ns(k)
    k = "".join([f"_{i.lower()}" if i.isupper() else i for i in k])
    return (k, k[1:])[k[0] == "_"]


def un_xml(v):
    """
    un_xml converts an xml value
    to ints, floats and booleans.
    """
    mapped = {
        "false": False,
        "true": True,
    }
    if v.isdigit():
        return int(v)
    if v.replace(".", "").isdigit():
        return float(v)
    if v in mapped:
        return mapped[v]
    return v


def strip_ns(this):
    """
    strip_ns strip namespace off this.
    """
    if "xmlns:" in this:
        return "xmlns"
    return this.split(":")[-1]


def iter_attrs(attrs):
    """
    iter_attrs normalizes xml attributes
    and adds them to the gonzo dict.
    """
    conv = {un_camel(k): un_xml(v) for k, v in attrs.items()}
    pts_vars = ["pts_time", "pts_adjustment", "duration", "segmentation_duration"]
    return  {k: (t2s(v) if k in pts_vars else v) for k, v in conv.items()}



def val2xml(val):
    """
    val2xmlconvert val for xml
    """
    if isinstance(val, (bool, int, float)):
        return str(val).lower()
    if isinstance(val, str):
        if val.lower()[:2] == "0x":
            return str(int(val, 16))
    return val


def key2xml(string):
    """
    key2xml convert name to camel case
    """
    new_string = string
    if "_" in string:
        new_string = string.title().replace("_", "")
    return new_string[0].lower() + new_string[1:]


def mk_xml_attrs(attrs):
    """
    mk_xml_attrs converts a dict into
    a dict of xml friendly keys and values
    """
    return "".join([f' {key2xml(k)}="{val2xml(v)}"' for k, v in attrs.items()])


class NameSpace:
    """
    Each Node instance has a NameSpace instance
    to track namespace settings.
    @ns is the name of the namespace
    @uri is the xmlns uri
    @all is a flag to signal that all elements and
    attributes will have the namespace prefixed.
    By default only  the elements are prefixed with the namespace.
    """

    def __init__(self, ns=None, uri=None):
        self.ns = ns
        self.uri = uri
        self.all = False

    def prefix_all(self, abool=True):
        """
        prefix_all takes a boolean
        True turns it on, False turns it off.
        """
        self.all = abool

    def xmlns(self):
        """
        xmlns return xmlns attribute
        """
        if not self.uri:
            return ""
        if not self.ns:
            return f'xmlns="{self.uri}"'
        return f'xmlns:{self.ns}="{self.uri}"'

    def clear(self):
        """
        clear clear namespace info
        """
        self.ns = None
        self.uri = None
        self.all = False


class Node:
    """
    The Node class is to create an xml node.

    An instance of Node has:

        name :      <name> </name>
        value  :    <name>value</name>
        attrs :     <name attrs[k]="attrs[v]">
        children :  <name><children[0]></children[0]</name>
        depth:      tab depth for printing (automatically set)

    Use like this:

        from splicefu.xml import Node

        ts = Node('TimeSignal')
        st = Node('SpliceTime',attrs={'pts_time':3442857000})
        ts.add_child(st)
        print(ts)
    """

    def __init__(self, name, value=None, attrs=None, ns=None):
        self.name = name
        self.value = value
        self.depth = 0
        self.namespace = NameSpace()
        self.namespace.ns = ns
        self.attr = None
        self._handle_attrs(attrs)
        self.children = []

    def __repr__(self):
        return self.mk()

    def _handle_attrs(self, attrs):
        if not attrs:
            attrs = {}
        if "xmlns" in attrs:
            self.namespace.uri = attrs.pop("xmlns")
        self.attrs = attrs

    def attrs2nodes(self):
        """
        attrs2nodes attributes to elements
        """
        for k, v in self.attrs.items():
            self.add_child( Node(name=key2xml(k), value=val2xml(v)),slot=0 )
        self.attrs={}

    def mk_ans(self, attrs):
        """
        mk_ans set namespace on attributes
        """
        new_attrs = {}
        if self.namespace.all:
            for k, v in attrs.items():
                new_attrs[f"{self.namespace.ns}:{k}"] = v
        return new_attrs

    def chk_obj(self, obj):
        """
        chk_obj determines if
        obj is self, or another obj
        for self.set_ns and self.mk
        """
        if obj is None:
            obj = self
        return obj

    def set_ns(self, ns=None):
        """
        set_ns set namespace on the Node
        """
        self.namespace.ns = ns

    def rm_attr(self, attr):
        """
        rm_attr remove an attribute
        """
        self.attrs.pop(attr)

    def add_attr(self, attr, value):
        """
        add_attr add an attribute
        """
        self.attrs[attr] = value

    def set_depth(self):
        """
        set_depth is used to format
        tabs in output
        """
        for child in self.children:
            child.depth = self.depth + 1

    def get_indent(self):
        """
        get_indent returns a string of spaces the required depth for a node
        """
        tab = "   "
        return tab * self.depth

    def _rendrd_children(self, rendrd, ndent, name):
        for child in self.children:
            rendrd += self.mk(child)
        return f"{rendrd}{ndent}</{name}>\n".replace(" >",">")

    def mk_name(self):
        """
        mk_name add namespace to node name
        """
        name = self.name
        if self.namespace.ns:
            name = f"{self.namespace.ns}:{name}"
        return name

    def rendr_attrs(self, ndent, name):
        """
        rendrd_attrs renders xml attributes
        """
        attrs = self.attrs
        if self.namespace.all:
            attrs = self.mk_ans(self.attrs)
        new_attrs = mk_xml_attrs(attrs)
        if self.depth == 0:
            return f"{ndent}<{name} {self.namespace.xmlns()} {new_attrs}>"
        return f"{ndent}<{name}{new_attrs}>"

    def children_namespaces(self):
        """
        children_namespaces give children your namespace
        """
        for child in self.children:
            child.namespace.ns = self.namespace.ns
            child.namespace.all = self.namespace.all
            child.namespace.uri = ""

    def rendr_all(self,ndent,name):
        """
        rendr_all renders the Node instance and it's children in xml.
        """
        rendrd = self.rendr_attrs(ndent, name)
        if self.value:
            return f"{rendrd}{self.value}</{name}>\n"
        rendrd = f"{rendrd}\n"
        rendrd.replace(" >",">")
        if self.children:
            return self._rendrd_children(rendrd, ndent, name)
        return rendrd.replace(">", "/>")

    def mk(self, obj=None):
        """
        mk make the Node as xml.
        """
        obj = self.chk_obj(obj)
        obj.set_depth()
        obj.children_namespaces()
        name = obj.mk_name()
        ndent = obj.get_indent()
        #obj.attrs2nodes()
        if isinstance(obj, Comment):
            return obj.mk(obj)
        return obj.rendr_all(ndent,name)

    def add_child(self, child, slot=None):
        """
        add_child adds a child node
        set slot to insert at index slot.
        """
        if not slot:
            slot = len(self.children)
        self.children = self.children[:slot] + [child] + self.children[slot:]

    def rm_child(self, child):
        """
        rm_child remove a child

        example:
        a_node.rm_child(a_node.children[3])
        """
        self.children.remove(child)

    def add_comment(self, comment, slot=None):
        """
        add_comment add a Comment node
        """
        self.add_child(Comment(comment), slot)


class Comment(Node):
    """
    The Comment class is to create a Node representing a xml comment.

    An instance of Comment has:

        name :      <!-- name -->
        depth:      tab depth for printing (automatically set)

    Since Comment is a Node, it also has attrs, value and children but
    these are ignored. cf etree.Comment
    Use like this:

        from splicefu.xml import Comment, Node

        n = Node('root')
        c = Comment('my first comment')

        n.add_child(c)
        print(n)

    See also Node.add_comment:
    """

    def mk(self, obj=None):
        obj = self.chk_obj(obj)
        obj.set_depth()
        return f"{obj.get_indent()}<!-- {obj.name} -->\n"


class XmlParser:
    """
    XmlParser is for parsing
    a SCTE-35 Cue from  xml.
    """
    
    DESCRIPTORS = [
        "AvailDescriptor",
        "DTMFDescriptor",
        "SegmentationDescriptor",
        "TimeDescriptor",
    ]

    def __init__(self):
        self.active = None
        self.node_list = []
        self.depth=0
        self.parent=None
        self.open=False

    def chk_node_list(self, node):
        """
        chk_node_list is used to track open xml nodes
        """
        if self.active in self.node_list:
            self.node_list.remove(self.active)
            self.open = False
        elif node[-2] != "/":
            self.node_list.append(self.active)
            self.depth +=1
            self.open = True

    def mk_value(self, value, gonzo):
        """
        mk_value, if the xml node has a value, write it to self.spare

        <name>value</name>

        """
        if value:
            gonzo[self.active][un_camel(self.active)] = unescape(value)
        return gonzo

    def mk_active(self, node):
        """
        mk_active sets self.active to the current node name.
        """
        self.active=None
        name = node[1:].split(" ", 1)[0].split(">", 1)[0]
        name = strip_ns(name)
        self.active = name.replace("/", "").replace(">", "")


    def _split_attrs(self, node):
        node = node.replace("='", '="').replace("' ", '" ')
        attrs = [x for x in node.split(" ") if "=" in x]
        return attrs

    def mk_attrs(self, node):
        """
        mk_attrs parses the current node for attributes
        and stores them in self.spare[self.active]
        """
        if "!--" in node:
            return False
        attrs = self._split_attrs(node)
        parsed = {
            x.split('="')[0]: unescape(x.split('="')[1].split('"')[0]) for x in attrs
        }
        it = iter_attrs(parsed)
        return it

    def parse(self, exemel, descriptor_parse=False):
        """
        parse parses an xml string for a SCTE-35 Cue.
        """
        gonzo={}
        if not descriptor_parse:
            gonzo = {"descriptors": []}
        data = exemel.replace("\n", "").strip()
        while ">" in data:
            self.mk_active(data)
            data, gonzo = self._parse_nodes(data, gonzo, descriptor_parse)
        return gonzo

    def _parse_nodes(self, data, gonzo, descriptor_parse=False):
        if self.active in self.DESCRIPTORS and not descriptor_parse:
            data, gonzo = self._parse_descriptor(data, gonzo)
        else:
            data, gonzo = self._parse_most(data, gonzo)
        return data, gonzo

    def _parse_most(self, data, gonzo):
        """
        parse_most parse everything except descriptor nodes
        """
        ridx = data.index(">")
        this_node = data[: ridx + 1]
        self.chk_node_list(this_node)
        attrs = self.mk_attrs(this_node)
        if self.active not in gonzo:
            if  self.active not in ['!--','']:
                gonzo[self.active] = attrs
        data = data[ridx + 1 :]
        if "<" in data:
            lidx = data.index("<")
            value = data[:lidx].strip()
            gonzo = self.mk_value(value, gonzo)
            data = data[lidx:]
        return data, gonzo

    def _parse_descriptor(self, data, gonzo):
        """
        mk_descriptor slices off an entire
        descriptor xml node from data to parse.
        """
        sub_data = ""
        tag = data[1:].split(" ", 1)[0].split('>',1)[0]
        try:
            sub_data = data[: data.index(f"</{tag}>") + len(tag) + 1]
        except:
            sub_data = data[: data.index("/>") + 2]
        data = data.replace(sub_data, "")
        sub_stuff = self.parse(sub_data, descriptor_parse=True)
        if 'SegmentationDescriptor' in sub_stuff and 'SegmentationUpid' in sub_stuff:
            sub_stuff['SegmentationDescriptor']['SegmentationUpid'] = sub_stuff.pop('SegmentationUpid')
        gonzo["descriptors"].append(sub_stuff)
        return data, gonzo
