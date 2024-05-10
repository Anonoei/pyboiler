import xml.etree.ElementTree as ET
from xml.dom import minidom
from xml.etree.ElementTree import tostring


def dumps(obj: dict, tag="root", pretty: bool = True):
    root = ET.Element(tag, {"t": "d"})
    _serialize(obj, root)
    xml = minidom.parseString(tostring(root))
    if pretty:
        return xml.toprettyxml()
    return xml.toxml()


def loads(xml_str: str):
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

    raise Exception(f"Unknown object to serialize {type(obj).__name__}")
    tag_name = str(type(obj).__name__)
    elem_tag = ET.Element(tag_name)
    for key_value in vars(obj).items():
        attr_name = key_value[0]
        value = getattr(obj, attr_name)
        if isinstance(value, str):  # For strings inside the object
            elem_text = ET.SubElement(elem_tag, attr_name)
            elem_text.text = str(value)
        elif hasattr(value, "__iter__"):  # For nested lists or dictionaries
            _serialize(value, elem_text)
        else:  # For other values
            elem_attr = ET.SubElement(elem_tag, attr_name)
            elem_attr.text = str(value)
    elem.append(elem_tag)


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

    r_depth = int(root.attrib.get("d"))
    for elem in root.iter():
        # print(f"{elem}: {elem.attrib.get('d')}")
        if not int(elem.attrib.get("d")) == r_depth + 1:
            continue
        e_t, e_d, e_r = parse(elem)
        results[elem.tag] = e_r
    return results
