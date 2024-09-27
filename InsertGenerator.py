class InsertGenerator:
    def __init__(self, db_type):
        if db_type == 'mysql':
            self.generator = MySQLInsertGenerator()
        elif db_type == 'postgresql':
            self.generator = PostgreSQLInsertGenerator()
        elif db_type == 'mongodb':
            self.generator = MongoDBInsertGenerator()
        elif db_type == 'sqlserver':
            self.generator = SQLServerInsertGenerator()
        elif db_type == 'sqlite':
            self.generator = SQLiteInsertGenerator()
        elif db_type == 'oracle':
            self.generator = OracleInsertGenerator()
        else:
            raise ValueError(f"Tipo de base de datos no soportado: {db_type}")

    def generate_inserts(self, table_name, schema, num_rows=10):
        data_generator = DataGenerator()
        inserts = []
        for _ in range(num_rows):
            data = data_generator.generate_data(schema)
            insert_statement = self.generator.generate_insert(table_name, data)
            inserts.append(insert_statement)
        return inserts
