class OracleInsertGenerator(InsertGeneratorBase):
    def generate_insert(self, table_name, data):
        columns = ', '.join(data.keys())
        values = ', '.join(self.format_value(v) for v in data.values())
        # Nota: Oracle tiene diferentes tipos de manejo de secuencias, pero esto es un caso básico
        return f"INSERT INTO {table_name} ({columns}) VALUES ({values}) RETURNING id INTO :id;"
