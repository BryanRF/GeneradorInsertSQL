import random
import string
import datetime
from typing import List, Dict, Any, Optional
import json
import csv
import xml.etree.ElementTree as ET
import sqlite3

class DataGenerator:
    def __init__(self):
        self.unique_values = {}
        self.custom_generators = {}

    def random_string(self, length: int = 10, charset: str = string.ascii_uppercase + string.digits) -> str:
        return ''.join(random.choices(charset, k=length))

    def random_number(self, min_value: int = 1000, max_value: int = 9999, unique: bool = False, field_name: Optional[str] = None) -> int:
        if unique:
            if field_name not in self.unique_values:
                self.unique_values[field_name] = set()
            
            while True:
                number = random.randint(min_value, max_value)
                if number not in self.unique_values[field_name]:
                    self.unique_values[field_name].add(number)
                    return number
        return random.randint(min_value, max_value)

    def random_date(self, start_year: int = 2000, end_year: int = 2024) -> datetime.date:
        start_date = datetime.date(start_year, 1, 1)
        end_date = datetime.date(end_year, 12, 31)
        return start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))

    def random_datetime(self, start_year: int = 2000, end_year: int = 2024) -> datetime.datetime:
        start_date = datetime.datetime(start_year, 1, 1)
        end_date = datetime.datetime(end_year, 12, 31, 23, 59, 59)
        return start_date + datetime.timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))

    def random_enum(self, options: List[Any]) -> Any:
        return random.choice(options)

    def random_boolean(self) -> bool:
        return random.choice([True, False])

    def random_float(self, min_value: float = 0.0, max_value: float = 1.0, decimals: int = 2) -> float:
        return round(random.uniform(min_value, max_value), decimals)

    def random_email(self, domains: List[str] = ["example.com", "test.org", "demo.net"]) -> str:
        username = self.random_string(8, string.ascii_lowercase)
        domain = random.choice(domains)
        return f"{username}@{domain}"

    def random_phone(self, format: str = "###-###-####") -> str:
        return ''.join(random.choice(string.digits) if char == '#' else char for char in format)

    def random_ipv4(self) -> str:
        return '.'.join(str(random.randint(0, 255)) for _ in range(4))

    def add_custom_generator(self, name: str, generator_func):
        self.custom_generators[name] = generator_func

    def generate_value(self, column: Dict[str, Any]) -> Any:
        col_type = column['type']
        nullable = column.get('nullable', False)
        unique = column.get('unique', False)
        is_pk = column.get('pk', False)

        if nullable and random.random() < 0.1:  # 10% chance of being NULL
            return None

        if col_type in self.custom_generators:
            return self.custom_generators[col_type](column)

        if col_type == 'string':
            length = column.get('length', 10)
            value = self.random_string(length)
            if is_pk or unique:
                while value in self.unique_values.get(column['name'], set()):
                    value = self.random_string(length)
                self.unique_values.setdefault(column['name'], set()).add(value)
            return value
        elif col_type == 'int':
            min_value = column.get('min', 1000)
            max_value = column.get('max', 9999)
            return self.random_number(min_value, max_value, unique or is_pk, column['name'])
        elif col_type == 'date':
            return self.random_date()
        elif col_type == 'datetime':
            return self.random_datetime()
        elif col_type == 'enum':
            return self.random_enum(column['values'])
        elif col_type == 'boolean':
            return self.random_boolean()
        elif col_type == 'float':
            return self.random_float(column.get('min', 0.0), column.get('max', 1.0), column.get('decimals', 2))
        elif col_type == 'email':
            return self.random_email(column.get('domains', ["example.com", "test.org", "demo.net"]))
        elif col_type == 'phone':
            return self.random_phone(column.get('format', "###-###-####"))
        elif col_type == 'ipv4':
            return self.random_ipv4()
        elif col_type == 'static':
            return column['value']
        else:
            raise ValueError(f"Unsupported column type: {col_type}")

    def generate_row(self, columns: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {column['name']: self.generate_value(column) for column in columns}

    def generate_data(self, columns: List[Dict[str, Any]], num_rows: int = 1) -> List[Dict[str, Any]]:
        return [self.generate_row(columns) for _ in range(num_rows)]

    def generate_insert_statement(self, table_name: str, row: Dict[str, Any]) -> str:
        columns = ', '.join(row.keys())
        placeholders = ', '.join(['%s' if isinstance(v, (int, float)) else "'%s'" for v in row.values()])
        values = tuple(row.values())
        return f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});" % values

    def generate_insert_statements(self, table_name: str, columns: List[Dict[str, Any]], num_rows: int = 1) -> str:
        data = self.generate_data(columns, num_rows)
        return '\n'.join(self.generate_insert_statement(table_name, row) for row in data)

    def save_sql_file(self, filename: str, insert_statements: str, use_transaction: bool = True):
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open(filename, 'w') as f:
            f.write(f"-- SQL file generated on {current_datetime}\n\n")
            if use_transaction:
                f.write("BEGIN TRANSACTION;\n")
                f.write("SAVE TRANSACTION DataInsertSavepoint;\n\n")
            f.write(insert_statements)
            if use_transaction:
                f.write("\n-- To undo changes, use:\n")
                f.write("-- ROLLBACK TRANSACTION DataInsertSavepoint;\n")
                f.write("COMMIT;\n")

    def save_json_file(self, filename: str, data: List[Dict[str, Any]]):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    def save_csv_file(self, filename: str, data: List[Dict[str, Any]]):
        if not data:
            return
        
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    def save_xml_file(self, filename: str, root_element: str, data: List[Dict[str, Any]]):
        root = ET.Element(root_element)
        for row in data:
            record = ET.SubElement(root, "record")
            for key, value in row.items():
                ET.SubElement(record, key).text = str(value)
        
        tree = ET.ElementTree(root)
        tree.write(filename, encoding="utf-8", xml_declaration=True)

    def save_sqlite_db(self, filename: str, table_name: str, columns: List[Dict[str, Any]], data: List[Dict[str, Any]]):
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()

        # Create table
        column_defs = [f"{col['name']} {self.get_sqlite_type(col['type'])}" for col in columns]
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(column_defs)});"
        cursor.execute(create_table_sql)

        # Insert data
        placeholders = ', '.join(['?' for _ in columns])
        insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
        cursor.executemany(insert_sql, [tuple(row.values()) for row in data])

        conn.commit()
        conn.close()

    @staticmethod
    def get_sqlite_type(col_type: str) -> str:
        type_mapping = {
            'string': 'TEXT',
            'int': 'INTEGER',
            'date': 'DATE',
            'datetime': 'DATETIME',
            'enum': 'TEXT',
            'boolean': 'BOOLEAN',
            'float': 'REAL',
            'email': 'TEXT',
            'phone': 'TEXT',
            'ipv4': 'TEXT',
            'static': 'TEXT'
        }
        return type_mapping.get(col_type, 'TEXT')

# Example usage:
if __name__ == "__main__":
    generator = DataGenerator()

    # Add a custom generator for a specific column type
    generator.add_custom_generator('custom_id', lambda col: f"ID-{generator.random_string(5)}")

    columns = [
        {'name': 'id', 'type': 'custom_id', 'pk': True},
        {'name': 'name', 'type': 'string', 'length': 50},
        {'name': 'email', 'type': 'email'},
        {'name': 'age', 'type': 'int', 'min': 18, 'max': 100},
        {'name': 'is_active', 'type': 'boolean'},
        {'name': 'created_at', 'type': 'datetime'},
        {'name': 'category', 'type': 'enum', 'values': ['A', 'B', 'C']},
        {'name': 'score', 'type': 'float', 'min': 0.0, 'max': 10.0, 'decimals': 1},
    ]

    # Generate data
    data = generator.generate_data(columns, num_rows=10)

    # Generate and save SQL insert statements
    insert_statements = generator.generate_insert_statements("users", columns, num_rows=10)
    generator.save_sql_file("users_insert.sql", insert_statements, use_transaction=True)

    # Save data in different formats
    generator.save_json_file("users_data.json", data)
    generator.save_csv_file("users_data.csv", data)
    generator.save_xml_file("users_data.xml", "users", data)
    generator.save_sqlite_db("users_data.db", "users", columns, data)

    print("Data generation and export complete.")