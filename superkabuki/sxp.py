"""
sxp.py
home of the SuperXmlParser class

"""

from xml.sax.saxutils import escape, unescape
from .xml import t2s, un_camel, un_xml, strip_ns, iter_attrs
from .descriptors import descriptor_map,k_by_v

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
        attrs={}
        if ">" in sub_data:
            ridx = sub_data.index(">")
            this_node = sub_data[: ridx + 1]
            attrs = self.mk_attrs(this_node)
            sub_data = sub_data[ridx + 1 :]
            if "<" in sub_data:
                lidx = sub_data.index("<")
                value = sub_data[:lidx].strip()
                sub_data = sub_data[lidx:].replace("\t","")
            return  {"tag":tag,"attrs":attrs,"value":value,"sub":sub_data,}

    def mk_tag(self, data):
        """
        mk_tag parse out the
        next available xml tag from data
        """
        tag = data[1:].split(" ", 1)[0].split(">", 1)[0]
        return tag

    def mk_element(self, data, tag):
        """
        mk_element slices out the tag element
        inclusive: <tag > stuff</tag> and <tag attr="1"/>
        """
        try:
            return data[: data.index(f"</{tag}>") + len(tag) + 2]
        except:
            try:
                return data[:data.index(f"{tag}>") + len(tag)]
            except:
                return data[:data.index("/>") +1 ]

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
            if target in tag:
                sub_data = self.mk_element(data, tag)
               # print(sub_data)
                results.append(sub_data + ">")
                data = data.replace(sub_data, "")
            else:
                data= data.split(">", 1)[1]
                if "<" in data:
                    data = data[data.index("<") :]
                else:
                    return results

    def gimme(self,tags,exemel):
        the_list =[]
        for tag in tags:
            results = self.mk(exemel, tag)
            if results:
                element_list = [self.parsed(tag, sd) for sd in results]
                if element_list:
                    the_list.extend(element_list)
        return the_list

    def spliceinfosection(self,exemel):
        tags = ["SpliceInfoSection"]

        out =self.gimme(tags,exemel)
        if out:
            return out[0]

    def command(self,exemel):
        tags=["SpliceInsert","TimeSignal"]
        cmd =  self.gimme(tags,exemel)[0]
        if cmd:
            splice_time = self.splicetime(cmd['sub'])
            if splice_time:
                cmd['attrs'].update(splice_time)
            break_duration=self.breakduration(cmd['sub'])
            if break_duration:
                cmd["attrs"].update(break_duration)
                #cmd['attrs']['break_duration']=break_duration[0]
                #cmd['attrs']['auto_return']=break_duration[1]
            return cmd
        return False

    def splicetime(self,exemel):
        splicetime =self.gimme(['SpliceTime'], exemel)
        if splicetime:
            return {"pts_time":splicetime[0]['attrs']['pts_time']}
        return False

    def breakduration(self,exemel):
        break_duration= self.gimme(['BreakDuration'],exemel)
        if break_duration:
            return {"break_duration":break_duration[0]['attrs']['duration'],
                    "auto_return": break_duration[0]['attrs']['auto_return']}
        return False

    def segmentationdescriptor(self,dscptr):
        if dscptr["tag"]=="SegmentationDescriptor":
            dr = self.deliveryrestrictions(dscptr['sub'])
            if dr:
                dscptr['attrs'].update(dr)
                dscptr["upids"] =self.gimme(['SegmentationUpid'], dscptr["sub"])
        return dscptr

    def descriptors(self,exemel):
        tags = [
        "AvailDescriptor",
        "DTMFDescriptor",
        "SegmentationDescriptor",
        "TimeDescriptor",]

        dlist= self.gimme(tags,exemel)
        for dscptr in dlist:
            dscptr = self.segmentationdescriptor(dscptr)
        return dlist

    def deliveryrestrictions(self,exemel):
        dr = self.gimme(['DeliveryRestrictions'], exemel)
        if dr:
            return dr[0]['attrs']
        return False
