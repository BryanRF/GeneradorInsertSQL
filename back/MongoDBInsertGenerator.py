class MongoDBInsertGenerator(InsertGeneratorBase):
    def generate_insert(self, table_name, data):
        return f"db.{table_name}.insert({data});"
