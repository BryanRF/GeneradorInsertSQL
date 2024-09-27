import json

class JSONExporter(ExporterBase):
    def export(self, data, file_name='output.json'):
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Archivo JSON generado: {file_name}")
