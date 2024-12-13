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

    def _split_attrs(self, node):
        node = node.replace("='", '="').replace("' ", '" ')
        attrs = [x for x in node.split(" ") if "=" in x]
        return attrs

    def mk_attrs(self, node):
        """
        mk_attrs parses the current node for attributes
        and stores them in self.stuff[self.active]
        """
        if "!--" in node:
            return False
        attrs = self._split_attrs(node)
        parsed = {
            x.split('="')[0]: unescape(x.split('="')[1].split('"')[0]) for x in attrs
        }
        it = iter_attrs(parsed)
        return it

    def parsed(self, tag, sub_data):
        """
        parsed returns tag, attrs and value
        for an xml element
        """
        value = ""
        attrs = {}
        if tag[0] != "/":
            tag = strip_ns(tag)
        o_data = sub_data
        if ">" in sub_data:
            ridx = sub_data.index(">")
            this_node = sub_data[: ridx + 1]
            attrs = self.mk_attrs(this_node)
            sub_data = sub_data[ridx + 1 :]
            if "<" in sub_data:
                lidx = sub_data.index("<")
                value = sub_data[:lidx].strip()
                sub_data = sub_data[lidx:].replace("\t", "")
            return {
                "tag": tag,
                "attrs": attrs,
                "this": value,
                "xml": o_data,
            }

    def mk_tag(self, data):
        """
        mk_tag parse out the
        next available xml tag from data
        """
        tag = data[1:].split(" ", 1)[0].split(">", 1)[0]
        return tag.strip()

    def mk_element(self, data, tag):
        """
        mk_element slices out the tag element
        inclusive: <tag > stuff</tag> and <tag attr="1"/>
        """
        try:
            return data[: data.index(f"</{tag}>") + len(tag) + 2]
        except:
            return data[: data.index("/>") + 1]

    def mk(self, exemel, target="SpliceInfoSection"):
        """
        parse parses an xml string for a SCTE-35 Cue.
        """
        results = []
        sub_data = None
        data = exemel.replace("\n", "").strip()
        while data:
            sub_data = None
            tag = self.mk_tag(data)
            if target in tag:  # don't even consider namespace
                sub_data = self.mk_element(data, tag)
                results.append(sub_data + ">")
                data = data.replace(sub_data, "")
            else:
                data = data.split(">", 1)[1]
                if "<" in data:
                    data = data[data.index("<") :]
                else:
                    return results

    def gimme(self, tags, exemel):
        """
        gimme get all instances of tag from exemel and return a list of them.
        """
        the_list = []
        for tag in tags:
            element_list = [self.parsed(tag, sd) for sd in self.mk(exemel, tag)]
            if element_list:
                the_list.extend(element_list)
        return the_list

    def gimme_one(self, tag, exemel):
        """
        gimme_one get the first instance of tag from exemel and return it.
        """
        one = self.gimme([tag], exemel)
        if one:
            return one[0]

    def spliceinfosection(self, exemel):
        """
        spliceinfosection parses exemel for info section data
        and returns a loadable dict
        """
        my_name = "SpliceInfoSection"

        out = self.gimme_one(my_name, exemel)
        if out:
            return out["attrs"]
        return {}

    def command(self, exemel):
        """
        command parses exemel for a splice command
        and returns a loadable dict

        """
        ts = self.timesignal(exemel)
        if ts:
            return ts
        si = self.spliceinsert(exemel)
        if si:
            return si
        pc = self.privatecommand(exemel)
        if pc:
            return pc
        return {}

    def timesignal(self, exemel):
        """
        timesignal parses exemel for TimeSignal data
        and creates a loadable dict for the Cue class.
        """
        my_name = "TimeSignal"
        ts = self.gimme_one("TimeSignal", exemel)
        if ts:
            splice_time = self.splicetime(ts["xml"])
            ts["attrs"].update(splice_time)
            setme = {
                "name": "Time Signal",
                "command_type": 6,
            }
            ts["attrs"].update(setme)
            return ts["attrs"]
        return {}

    def privatecommand(self, exemel):
        """
        privatecommand parses exemel for PrivateCommand
        data and creates a loadable dict for the Cue class.
        """
        my_name = "PrivateCommand"
        pc = self.gimme_one("PrivateCommand", exemel)
        if pc:
            setme = {
                "name": "Private Command",
                "command_type": 255,
                "private_bytes": pc["this"],
            }
            pc["attrs"].update(setme)
            return pc["attrs"]
        return {}

    def spliceinsert(self, exemel):
        """
        spliceinsert parses exemel for SpliceInsert data
        and creates a loadable dict for the Cue class.
        """
        my_name = "SpliceInsert"
        si = self.gimme_one(my_name, exemel)
        if si:
            setme = {
                "name": my_name,
                "command_type": 5,
                "event_id_compliance_flag": True,
                "program_splice_flag": False,
                "duration_flag": False,
            }
            splice_time = self.splicetime(exemel)
            if splice_time:
                setme["program_splice_flag"] = True
            si["attrs"].update(setme)
            si["attrs"].update(splice_time)
            break_duration = self.breakduration(exemel)
            si["attrs"].update(break_duration)
            return si["attrs"]
        return {}

    def splicetime(self, exemel):
        """
        splicetime parses xml from a splice command
        to get pts_time, sets time_specified_flag to True
        """
        splicetime = self.gimme_one("SpliceTime", exemel)
        if splicetime:
            return {
                "pts_time": splicetime["attrs"]["pts_time"],
                "time_specified_flag": True,
            }
        return {}

    def breakduration(self, exemel):
        """
        breakduration parses xml for break duration, break_auto_return
        and sets duration_flag to True.
        """
        break_duration = self.gimme_one("BreakDuration", exemel)
        if break_duration:
            return {
                "break_duration": break_duration["attrs"]["duration"],
                "break_auto_return": break_duration["attrs"]["auto_return"],
                "duration_flag": True,
            }
        return {}

    def segmentationdescriptor(self, dscptr):
        """
        segmentationdescriptor creates a dict to be loaded.
        """
        my_name = "SegmentationDescriptor"
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
        if dscptr["attrs"]["segmentation_type_id"] in table22:
            dscptr["attrs"]["segmentation_message"] = table22[
                dscptr["attrs"]["segmentation_type_id"]
            ]
        dscptr["attrs"].update(setme)
        dr = self.deliveryrestrictions(dscptr["xml"])
        dscptr["attrs"].update(dr)
        the_upid = self.upids(dscptr["xml"])
        dscptr["attrs"].update(the_upid)
        return dscptr["attrs"]

    def upids(self, exemel):
        """
        upids parses out upids from a splice descriptors xml
        """
        ulist = self.gimme(["SegmentationUpid"], exemel)
        if len(ulist) == 1:
            try:
                seg_upid = bytes.fromhex(ulist[0]["this"].lower().replace("0x", ""))
            except ValueError:
                seg_upid = ulist[0]["this"]
            seg_upid_type = ulist[0]["attrs"]["segmentation_upid_type"]
            the_upid = {
                "segmentation_upid": ulist[0]["this"],
                "segmentation_upid_type": seg_upid_type,
                "segmentation_upid_type_name": upid_map[seg_upid_type][0],
                "segmentation_upid_length": len(seg_upid),
            }
            return the_upid

    def availdescriptor(self, dscptr):
        my_name = "AvailDescriptor"
        setme = {
            "tag": 0,
            "identifier": "CUEI",
            "name": my_name,
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
        my_name = "TimeDescriptor"
        setme = {
            "tag": 3,
            "identifier": "CUEI",
            "name": my_name,
        }
        dscptr["attrs"].update(setme)
        return dscptr["attrs"]

    def descriptors(self, exemel):
        dmap = {
            "AvailDescriptor": self.availdescriptor,
            # "DTMFDescriptor",
            "SegmentationDescriptor": self.segmentationdescriptor,
            # "TimeDescriptor",
        }
        out = []
        dlist = self.gimme(list(dmap.keys()), exemel)
        for dscptr in dlist:
            out.append(dmap[dscptr["tag"]](dscptr))
        return out

    def deliveryrestrictions(self, exemel):
        dr = self.gimme_one("DeliveryRestrictions", exemel)
        if dr:
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
        bindata = self.gimme_one("Binary", exemel)
        if bindata:
            return bindata["this"]
        splice_info = self.spliceinfosection(exemel)
        cmd = self.command(exemel)
        dscptrs = self.descriptors(exemel)
        return {
            "info_section": splice_info,
            "command": cmd,
            "descriptors": dscptrs,
        }
