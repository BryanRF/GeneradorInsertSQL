class MySQLInsertGenerator(InsertGeneratorBase):
    def generate_insert(self, table_name, data):
        columns = ', '.join(data.keys())
        values = ', '.join(self.format_value(v) for v in data.values())
        return f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
