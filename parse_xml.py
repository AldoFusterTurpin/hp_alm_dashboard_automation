from lxml import etree
from copy import deepcopy


def obtain_xml_string():
    with open("out1.xml", "r") as in_file:
        result = in_file.read()
        return result


root = etree.fromstring(obtain_xml_string().encode('utf-8'))
tree = etree.ElementTree(root)

child for child in root
