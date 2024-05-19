"""XML object (de)serialization in a similar interface to python.json"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
from xml.etree.ElementTree import tostring


def dumps(obj: dict, tag="root", pretty: bool = True):
    """Serializes a python dict to xml notation"""
    root = ET.Element(tag, {"t": "d"})
    _serialize(obj, root)
    xml = minidom.parseString(tostring(root))
    if pretty:
        return xml.toprettyxml()
    return xml.toxml()


def loads(xml_str: str):
    """Deserializes xml to a python dictionary"""
    xml_str = xml_str.replace("\n", "").replace("\t", "")
    return _deserialize(ET.fromstring(xml_str))


def _serialize(obj, elem=None, tag=None, depth=0):
    if elem is None:
        elem = ET.Element("root")

    elem.attrib["d"] = str(depth)

    if isinstance(obj, str):  # For strings
        elem.text = obj
        return

    if hasattr(obj, "__iter__"):  # For lists, tuples, sets, and dicts
        if isinstance(obj, dict):
            elem.attrib["t"] = "d"
            for k, v in obj.items():
                ele = ET.SubElement(elem, k, {"d": f"{depth+1}"})
                _serialize(v, ele, k, depth=depth + 1)
            return
        elem.attrib["t"] = "l"
        for idx, item in enumerate(obj):
            ele = ET.SubElement(elem, f"i{idx}", {"d": f"{depth+1}"})
            _serialize(item, ele, depth=depth + 1)
        return

    if obj is None:
        elem.attrib["t"] = "n"
        elem.text = "null"
        return
    elem.text = str(obj)
    return


def _deserialize(root: ET.Element):
    results = {}

    def parse(root):
        r_type = root.attrib.get("t", None)
        r_depth = int(root.attrib.get("d"))
        if r_type == "d":
            return r_type, r_depth, parse_dict(root)
        elif r_type == "l":
            return r_type, r_depth, parse_list(root)
        elif r_type == "n":
            return r_type, r_depth, None
        else:
            return r_type, r_depth, root.text

    def parse_dict(root):
        res = {}
        r_depth = int(root.attrib.get("d"))
        for elem in root.iter():
            if not int(elem.attrib.get("d")) == r_depth + 1:
                continue
            e_t, e_d, e_res = parse(elem)
            res[elem.tag] = e_res
        return res

    def parse_list(root):
        res = []
        r_depth = int(root.attrib.get("d"))
        for elem in root.iter():
            if not int(elem.attrib.get("d")) == r_depth + 1:
                continue
            e_t, e_d, e_res = parse(elem)
            res.append(e_res)
        return res

    r_depth = int(root.attrib.get("d"))  # type: ignore
    for elem in root.iter():
        # print(f"{elem}: {elem.attrib.get('d')}")
        if not int(elem.attrib.get("d")) == r_depth + 1:  # type: ignore
            continue
        e_t, e_d, e_r = parse(elem)
        results[elem.tag] = e_r
    return results
