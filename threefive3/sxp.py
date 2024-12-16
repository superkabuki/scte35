"""
sxp.py
home of the SuperXmlParser class

"""

from xml.sax.saxutils import escape, unescape
from .xml import t2s, un_camel, un_xml, strip_ns, iter_attrs
from .descriptors import descriptor_map, k_by_v
from .segmentation import table20, table22
from .upids import upid_map


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

    def spliceinfosection(self, sis):
        """
        spliceinfosection parses exemel for info section data
        and returns a loadable dict
        """
        return sis["attrs"]

    def command(self, results):
        """
        command parses exemel for a splice command
        and returns a loadable dict

        """
        cmap = {
            "TimeSignal": self.timesignal,
            "SpliceInsert": self.spliceinsert,
            "PrivateCommand": self.privatecommand,
        }

        for result in results:
            if result["name"] in cmap:
                return cmap[result["name"]](result)
        return {}

    def _timesignal_children(self,ts):
        for child in ts["children"]:
            splice_time = self.splicetime(child)
            ts["attrs"].update(splice_time)
        return ts

    def timesignal(self, ts):
        """
        timesignal parses exemel for TimeSignal data
        and creates a loadable dict for the Cue class.
        """
        setme = {
                "name": "Time Signal",
                "command_type": 6,
        }

        ts["attrs"].update(setme)
        ts = self._timesignal_children(ts)
        return ts["attrs"]

    def privatecommand(self, pc):
        """
        privatecommand parses exemel for PrivateCommand
        data and creates a loadable dict for the Cue class.
        """
        setme = {
            "command_type": 255,
            "private_bytes": pc["this"],
        }

        pc["attrs"].update(setme)
        return pc["attrs"]

    def _spliceinsert_children(self,si):
        for child in si["children"]:
            splice_time = self.splicetime(child)
            si["attrs"].update(splice_time)
            if "pts_time" in si["attrs"]:
                si["attrs"]["program_splice_flag"] = True
            break_duration = self.breakduration(child)
            si["attrs"].update(break_duration)
        return si

    def spliceinsert(self, si):
        """
        spliceinsert parses exemel for SpliceInsert data
        and creates a loadable dict for the Cue class.
        """
        setme = {
            "command_type": 5,
            "event_id_compliance_flag": True,
            "program_splice_flag": False,
            "duration_flag": False,
        }
        si["attrs"].update(setme)
        si = self._spliceinsert_children(si)
        return si["attrs"]

    def splicetime(self, st):
        """
        splicetime parses xml from a splice command
        to get pts_time, sets time_specified_flag to True
        """
        if st["name"] == "SpliceTime":
            return {
                "pts_time": st["attrs"]["pts_time"],
                "time_specified_flag": True,
            }
        return {}

    def breakduration(self, bd):
        """
        breakduration parses xml for break duration, break_auto_return
        and sets duration_flag to True.
        """
        if bd["name"] == "BreakDuration":
            return {
                "break_duration": bd["attrs"]["duration"],
                "break_auto_return": bd["attrs"]["auto_return"],
                "duration_flag": True,
            }
        return {}

    def _segmentationdescriptor_children(self,dscptr):
        for child in dscptr["children"]:
            dr = self.deliveryrestrictions(child)
            dscptr["attrs"].update(dr)
            the_upid = self.upids(child)
            dscptr["attrs"].update(the_upid)
        return dscptr

    def _segmentation_message(self,dscptr):
        if dscptr["attrs"]["segmentation_type_id"] in table22:
            dscptr["attrs"]["segmentation_message"] = table22[
                dscptr["attrs"]["segmentation_type_id"]
            ]
        return dscptr

    def segmentationdescriptor(self, dscptr):
        """
        segmentationdescriptor creates a dict to be loaded.
        """
        setme = {
            "tag": 2,
            "identifier": "CUEI",
            "name": "Segmentation Descriptor",
            "segmentation_event_id_compliance_indicator": True,
            "program_segmentation_flag": True,
            "segmentation_duration_flag": False,
            "delivery_not_restricted_flag": True,
            "segmentation_event_id": hex(dscptr["attrs"]["segmentation_event_id"]),
        }
        dscptr["attrs"].update(setme)
        dscptr = self._segmentation_message(dscptr)
        dscptr = self._segmentationdescriptor_children(dscptr)
        return dscptr["attrs"]

    def upids(self, upid):
        """
        upids parses out upids from a splice descriptors xml
        """
        if upid["name"] == "SegmentationUpid":
            try:
                seg_upid = bytes.fromhex(upid["this"].lower().replace("0x", ""))
            except ValueError:
                seg_upid = upid["this"]
            seg_upid_type = upid["attrs"]["segmentation_upid_type"]
            return {
                "segmentation_upid": upid["this"],
                "segmentation_upid_type": seg_upid_type,
                "segmentation_upid_type_name": upid_map[seg_upid_type][0],
                "segmentation_upid_length": len(seg_upid),
            }
        return {}

    def availdescriptor(self, dscptr):
        setme = {
            "tag": 0,
            "identifier": "CUEI",
        }
        dscptr["attrs"].update(setme)
        return dscptr["attrs"]

    ##    def dtmfdescriptor(self,dscptr)
    ##        """
    ##        Load an DTMFDescriptor from XML
    ##        """
    ##         setme={"tag": 1,
    ##                "identifier": "CUEI",
    ##                "name":my_name,}
    ##        gonzo["DTMFDescriptor"]["dtmf_chars"] = gonzo["DTMFDescriptor"].pop("chars")
    ##        self.load(gonzo["DTMFDescriptor"])
    ##        self.dtmf_count = len(self.dtmf_chars)

    def timedescriptor(self, dscptr):
        setme = {
            "tag": 3,
            "identifier": "CUEI",
            "name": my_name,
        }
        dscptr["attrs"].update(setme)
        return dscptr["attrs"]

    def descriptors(self, results):
        dmap = {
            "AvailDescriptor": self.availdescriptor,
            # "DTMFDescriptor",
            "SegmentationDescriptor": self.segmentationdescriptor,
            "TimeDescriptor": self.timedescriptor,
        }
        out = []
        for result in results:
            if result["name"] in dmap:
                out.append(dmap[result["name"]](result))
        return out

    def deliveryrestrictions(self, dr):
        if dr["name"] == "DeliveryRestrictions":
            setme = {
                "delivery_not_restricted_flag": False,
                "device_restrictions": table20[dr["attrs"]["device_restrictions"]],
            }
            dr["attrs"].update(setme)
            return dr["attrs"]
        return {}

    def xml2cue(self, exemel):
        """
        xml2cue returns a base64 string for xmlbin
        and a dict for xml
        """
        results = self.fu(exemel)
        for result in results:
            if result["name"] == "Binary":
                return result["this"]
            if result["name"] == "SpliceInfoSection":
                splice_info = self.spliceinfosection(result)
        return {
            "info_section": splice_info,
            "command": self.command(results),
            "descriptors": self.descriptors(results),
        }
