from lxml import etree
from copy import deepcopy


def merge(original_xml, second_xml) -> str:
    '''Copy all the 'Entity' nodes of 'second_xml' to 'original_xml'(as children of 'Entities' node)'''

    # the root of original_xml is the 'Entities node'
    root_accumulated = etree.fromstring(original_xml.encode('utf-8'))
    root_second_xml = etree.fromstring(second_xml.encode('utf-8'))

    # print("root: " + root_original.tag)
    # print(type(root_original))

    # the nodes I will insert
    entity_nodes = root_second_xml.xpath("Entity")

    [root_accumulated.append(deepcopy(element)) for element in entity_nodes]

    ret = etree.tostring(root_accumulated, encoding='UTF-8', method='xml', pretty_print=True, xml_declaration=False).decode("utf-8")
    ret = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' + "\n" + ret
    return ret


def get_entities_total_results(xml) -> str:
    root = etree.fromstring(xml.encode('utf-8'))
    return root.xpath("/Entities")[0].get("TotalResults")
