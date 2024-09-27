import csv

class CSVExporter(ExporterBase):
    def export(self, data, file_name='output.csv'):
        with open(file_name, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"Archivo CSV generado: {file_name}")
