class ExporterBase:
    def export(self, data, file_name):
        """Método abstracto para exportar los datos a un archivo. Debe ser sobrescrito."""
        raise NotImplementedError("Este método debe ser implementado por las subclases.")
