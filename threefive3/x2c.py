"""
x2c.py  xml to cue conversion
"""
from .descriptors import descriptor_map, k_by_v
from .segmentation import table20, table22
from .sxp import SuperXmlParser
from .upids import upid_map


def _spliceinfosection(sis):
    """
    spliceinfosection parses exemel for info section data
    and returns a loadable dict
    """
    return sis["attrs"]

def _command(results):
    """
    command parses exemel for a splice command
    and returns a loadable dict

    """
    cmap = {
        "TimeSignal": _timesignal,
        "SpliceInsert": _spliceinsert,
        "PrivateCommand": _privatecommand,
    }

    for result in results:
        if result["name"] in cmap:
            return cmap[result["name"]](result)
    return {}

def _timesignal_children(ts):
    for child in ts["children"]:
        splice_time = _splicetime(child)
        ts["attrs"].update(splice_time)
    return ts

def _timesignal( ts):
    """
    timesignal parses exemel for TimeSignal data
    and creates a loadable dict for the Cue class.
    """
    setme = {
            "name": "Time Signal",
            "command_type": 6,
    }

    ts["attrs"].update(setme)
    ts = _timesignal_children(ts)
    return ts["attrs"]

def _privatecommand( pc):
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

def _spliceinsert_children(si):
    for child in si["children"]:
        splice_time = _splicetime(child)
        si["attrs"].update(splice_time)
        if "pts_time" in si["attrs"]:
            si["attrs"]["program_splice_flag"] = True
        break_duration = _breakduration(child)
        si["attrs"].update(break_duration)
    return si

def _spliceinsert( si):
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
    si = _spliceinsert_children(si)
    return si["attrs"]

def _splicetime( st):
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

def _breakduration( bd):
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

def _segmentationdescriptor_children(dscptr):
    for child in dscptr["children"]:
        dr = _deliveryrestrictions(child)
        dscptr["attrs"].update(dr)
        the_upid = _upid(child)
        dscptr["attrs"].update(the_upid)
    return dscptr

def _segmentation_message(dscptr):
    if dscptr["attrs"]["segmentation_type_id"] in table22:
        dscptr["attrs"]["segmentation_message"] = table22[
            dscptr["attrs"]["segmentation_type_id"]
        ]
    return dscptr

def _segmentationdescriptor( dscptr):
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
    dscptr = _segmentation_message(dscptr)
    dscptr = _segmentationdescriptor_children(dscptr)
    return dscptr["attrs"]

def _upid(a_upid):
    """
    upids parses out upids from a splice descriptors xml
    """
    if a_upid["name"] == "SegmentationUpid":
        try:
            seg_upid = bytes.fromhex(a_upid["this"].lower().replace("0x", ""))
        except ValueError:
            seg_upid = a_upid["this"]
        seg_upid_type = a_upid["attrs"]["segmentation_upid_type"]
        return {
            "segmentation_upid": a_upid["this"],
            "segmentation_upid_type": seg_upid_type,
            "segmentation_upid_type_name": upid_map[seg_upid_type][0],
            "segmentation_upid_length": len(seg_upid),
        }
    return {}

def _availdescriptor( dscptr):
    setme = {
        "tag": 0,
        "identifier": "CUEI",
    }
    dscptr["attrs"].update(setme)
    return dscptr["attrs"]

##    def dtmfdescriptor(dscptr)
##        """
##        Load an DTMFDescriptor from XML
##        """
##         setme={"tag": 1,
##                "identifier": "CUEI",
##                "name":my_name,}
##        gonzo["DTMFDescriptor"]["dtmf_chars"] = gonzo["DTMFDescriptor"].pop("chars")
##        self.load(gonzo["DTMFDescriptor"])
##        self.dtmf_count = len(self.dtmf_chars)

def _timedescriptor( dscptr):
    setme = {
        "tag": 3,
        "identifier": "CUEI",
    }
    dscptr["attrs"].update(setme)
    return dscptr["attrs"]

def _descriptors( results):
    dmap = {
        "AvailDescriptor": _availdescriptor,
        # "DTMFDescriptor",
        "SegmentationDescriptor": _segmentationdescriptor,
        "TimeDescriptor": _timedescriptor,
    }
    out = []
    for result in results:
        if result["name"] in dmap:
            out.append(dmap[result["name"]](result))
    return out

def _deliveryrestrictions( dr):
    if dr["name"] == "DeliveryRestrictions":
        setme = {
            "delivery_not_restricted_flag": False,
            "device_restrictions": table20[dr["attrs"]["device_restrictions"]],
        }
        dr["attrs"].update(setme)
        return dr["attrs"]
    return {}

def xml2cue( exemel):
    """
    xml2cue returns a base64 string for xmlbin
    and a dict for xml
    """
    sxp=SuperXmlParser()
    results = sxp.fu(exemel)
    for result in results:
        if result["name"] == "Binary":
            return result["this"]
        if result["name"] == "SpliceInfoSection":
            splice_info = _spliceinfosection(result)
    return {
        "info_section": splice_info,
        "command": _command(results),
        "descriptors": _descriptors(results),
    }

