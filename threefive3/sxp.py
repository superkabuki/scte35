"""
sxp.py
home of the SuperXmlParser class

"""

from xml.sax.saxutils import escape, unescape
from .xml import t2s, un_camel, un_xml, strip_ns, iter_attrs

class SuperXmlParser:

    CHILD_NODES=[
                    "Program",
                    "SpliceTime",
                    "DeliveryRestrictions",
                    "SegmentationUpid",
                    "BreakDuration",
                ]

    def _split_attrs(self, node):
        node = node.replace("='", '="').replace("' ", '" ')
        attrs = [x for x in node.split(" ") if "=" in x]
        return attrs

    def mk_attrs(self, node):
        """
        mk_attrs parses the current node for attributes
        and stores them in self.stuff[self.active]
        """
        attrs = {}
        try:
            attrs = self._split_attrs(node)
            parsed = {
                x.split('="')[0]: unescape(x.split('="')[1].split('"')[0])
                for x in attrs
            }
            attrs = iter_attrs(parsed)
        finally:
            return attrs

    def mk_tag(self, data):
        """
        mk_tag parse out the
        next available xml tag from data
        """
        tag = data[1:].split(" ", 1)[0].split(">", 1)[0]
        return strip_ns(tag.strip())

    def _vrfy_sp(self, sp):
        if sp and sp[0] not in ["!", "/"]:
            return True
        return False

    def _mk_value(self, sp):
        return sp.split(">")[1].replace("\n", "").strip()

    def _assemble(self, sp):
        return {
            "name": self.mk_tag(sp),
            "attrs": self.mk_attrs(sp),
            "this": self._mk_value(sp),
            "children": [],
        }

    def fu(self, exemel):
        """
        fu slice up exemel into data chunks.
        """
        results = []
        splitted = exemel.split("<")
        exemel = exemel.replace("\n", "").strip()
        for sp in splitted:
            if self._vrfy_sp(sp):
                x = self._assemble(sp)
                if x["name"] in self.CHILD_NODES:
                    results[-1]["children"].append(x)
                else:
                    results.append(x)
        return results
