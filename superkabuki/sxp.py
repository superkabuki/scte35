"""
sxp.py
home of the SuperXmlParser class

"""

from xml.sax.saxutils import escape, unescape
from .xml import t2s, un_camel, un_xml, strip_ns, iter_attrs


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
                sub_data = sub_data[lidx:]
            return  {"tag":tag,"attrs":attrs,"value":value,"sub":sub_data,}

    def mk_tag(self, data):
        """
        mk_tag parse out the
        next available xml tag from data
        """
        tag = data[1:].split(" ", 1)[0].split(">", 1)[0]
        return strip_ns(tag)

    def mk_element(self, data, tag):
        """
        mk_element slices out the tag element
        inclusive: <tag > stuff</tag> and <tag attr="1"/>
        """
        try:
            return data[: data.index(f"</{tag}>") + len(tag) + 2]
        except:
            try:
                return data[:data.index("/>") + 1]
            except:
                return data[:data.index(f"{tag}>") + len(tag)]

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
            if tag == target:
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

    def descriptors(self,exemel):    
        tags = [
        "AvailDescriptor",
        "DTMFDescriptor",
        "SegmentationDescriptor",
        "TimeDescriptor",]

        utags =["SegmentationUpid"]
        
        dlist= self.gimme(tags,exemel)
        for dscptr in dlist:
            if dscptr["tag"]=="SegmentationDescriptor":
                dscptr["upids"] =self.gimme(utags, dscptr["sub"])
        return dlist

    def spliceinfosection(self,exemel):
        tags = ["SpliceInfoSection"]

        out =self.gimme(tags,exemel)
        if out:
            return out[0]

    def command(self,exemel):
        tags=["SpliceInsert","TimeSignal"]

        return self.gimme(tags,exemel)[0]

        
        
            
