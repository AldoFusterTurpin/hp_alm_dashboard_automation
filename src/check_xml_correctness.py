from lxml import etree


def main():
    '''If the file contains a non correct XML, it will throw an exception, otherwise will print it'''
    file_path = "result.xml"
    doc = etree.parse(file_path)
    raw_bytes = etree.tostring(doc, encoding='utf-8', method='xml', pretty_print=True, xml_declaration=False)
    xml_string = raw_bytes.decode("utf-8")
    print(xml_string)


main()
