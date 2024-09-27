import xml.etree.ElementTree as ET

class XMLExporter(ExporterBase):
    def export(self, data, file_name='output.xml'):
        root = ET.Element("data")
        for row in data:
            record = ET.SubElement(root, "record")
            for key, value in row.items():
                ET.SubElement(record, key).text = str(value)
        tree = ET.ElementTree(root)
        tree.write(file_name, encoding="utf-8", xml_declaration=True)
        print(f"Archivo XML generado: {file_name}")
