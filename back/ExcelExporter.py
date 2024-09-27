import openpyxl

class ExcelExporter(ExporterBase):
    def export(self, data, file_name='output.xlsx'):
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # Asume que data es una lista de diccionarios
        headers = data[0].keys()
        sheet.append(list(headers))

        for row in data:
            sheet.append(list(row.values()))

        workbook.save(file_name)
        print(f"Archivo Excel generado: {file_name}")
