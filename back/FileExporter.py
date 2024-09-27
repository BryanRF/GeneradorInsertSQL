class FileExporter:
    def __init__(self, format_type):
        if format_type == 'excel':
            self.exporter = ExcelExporter()
        elif format_type == 'csv':
            self.exporter = CSVExporter()
        elif format_type == 'json':
            self.exporter = JSONExporter()
        elif format_type == 'xml':
            self.exporter = XMLExporter()
        else:
            raise ValueError(f"Formato de exportación no soportado: {format_type}")
    def export(self, data, file_name):
        self.exporter.export(data, file_name)
