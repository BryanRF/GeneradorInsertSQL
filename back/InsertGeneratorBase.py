class InsertGeneratorBase:
    def generate_insert(self, table_name, data):
        """Método que genera una sentencia INSERT para la base de datos. Se sobrescribe en las subclases."""
        raise NotImplementedError("Este método debe ser implementado por las subclases.")

    def format_value(self, value):
        """Formatea el valor para ser usado en una sentencia INSERT según el tipo de base de datos."""
        if value is None:
            return 'NULL'
        elif isinstance(value, str):
            return f"'{value}'"
        elif isinstance(value, bool):
            return 'TRUE' if value else 'FALSE'
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, datetime.datetime):
            return f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif isinstance(value, datetime.date):
            return f"'{value.strftime('%Y-%m-%d')}'"
        else:
            return f"'{str(value)}'"
