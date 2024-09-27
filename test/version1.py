import random
import string
import datetime
import names  # Puedes usar la librería "names" para generar nombres aleatorios

# Almacenamiento para valores únicos
unique_values = {}

class DataGenerator:
    """Clase para generar datos aleatorios y SQL INSERT statements adaptables a diferentes escenarios"""

    def __init__(self, table_name, columns, num_rows=1, use_transaction=True):
        self.table_name = table_name
        self.columns = columns
        self.num_rows = num_rows
        self.use_transaction = use_transaction

    def random_string(self, length=10):
        """Genera una cadena aleatoria de longitud fija"""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def random_number(self, min_value=1000, max_value=9999, unique=False, field_name=None):
        """Genera un número aleatorio dentro de un rango, asegura unicidad si es necesario"""
        if unique:
            if field_name not in unique_values:
                unique_values[field_name] = set()
            
            while True:
                number = random.randint(min_value, max_value)
                if number not in unique_values[field_name]:
                    unique_values[field_name].add(number)
                    return number
        return random.randint(min_value, max_value)

    def random_date(self, start_year=2000, end_year=2024):
        """Genera una fecha aleatoria dentro de un rango de años"""
        start_date = datetime.date(start_year, 1, 1)
        end_date = datetime.date(end_year, 12, 31)
        random_days = random.randint(0, (end_date - start_date).days)
        return start_date + datetime.timedelta(days=random_days)

    def random_datetime(self, start_year=2000, end_year=2024):
        """Genera una fecha y hora aleatoria dentro de un rango de años"""
        start_date = datetime.datetime(start_year, 1, 1)
        end_date = datetime.datetime(end_year, 12, 31, 23, 59, 59)
        random_seconds = random.randint(0, int((end_date - start_date).total_seconds()))
        return start_date + datetime.timedelta(seconds=random_seconds)

    def random_enum(self, options):
        """Devuelve un valor aleatorio de una lista de opciones"""
        return random.choice(options)

    def random_name(self):
        """Genera un nombre aleatorio"""
        return names.get_full_name()

    def random_address(self):
        """Genera una dirección aleatoria"""
        streets = ["Main St", "Highland Ave", "Elm St", "Park Ave", "Oak St", "Maple St"]
        house_number = random.randint(1, 9999)
        street = random.choice(streets)
        return f"{house_number} {street}"

    def nullable_or_value(self, nullable, generator_fn, force_null=False):
        """Decide si un campo es nulo o genera un valor utilizando la función generadora dada"""
        if force_null:
            return "NULL"
        if nullable and random.random() < 0.2:  # 20% de probabilidad de ser NULL
            return "NULL"
        else:
            return generator_fn()

    def generate_insert_statements(self):
        """Genera sentencias SQL INSERT INTO con datos ficticios"""
        insert_statements = []
        for _ in range(self.num_rows):
            values = []
            for column in self.columns:
                col_name = column['name']
                col_type = column['type']
                nullable = column.get('nullable', False)
                unique = column.get('unique', False)
                is_pk = column.get('pk', False)
                force_null = column.get('force_null', False)

                if col_type == 'string':
                    length = column.get('length', 10)
                    values.append(self.nullable_or_value(nullable, lambda: f"N'{self.random_string(length)}'", force_null))
                elif col_type == 'int':
                    min_value = column.get('min', 1000)
                    max_value = column.get('max', 9999)
                    values.append(self.nullable_or_value(nullable, lambda: str(self.random_number(min_value, max_value, unique=unique or is_pk, field_name=col_name)), force_null))
                elif col_type == 'date':
                    values.append(self.nullable_or_value(nullable, lambda: f"N'{self.random_date()}'", force_null))
                elif col_type == 'datetime':
                    values.append(self.nullable_or_value(nullable, lambda: f"N'{self.random_datetime()}'", force_null))
                elif col_type == 'enum':
                    enum_values = column['values']
                    values.append(self.nullable_or_value(nullable, lambda: f"N'{self.random_enum(enum_values)}'", force_null))
                elif col_type == 'name':
                    values.append(self.nullable_or_value(nullable, lambda: f"N'{self.random_name()}'", force_null))
                elif col_type == 'address':
                    values.append(self.nullable_or_value(nullable, lambda: f"N'{self.random_address()}'", force_null))
                elif col_type == 'static':
                    static_value = column['value']
                    values.append(f"N'{static_value}'")
            
            # Construcción de la sentencia INSERT
            col_names = ", ".join([col['name'] for col in self.columns])
            col_values = ", ".join(values)
            insert_statement = f"INSERT INTO {self.table_name} ({col_names}) VALUES ({col_values});"
            insert_statements.append(insert_statement)
        
        return "\n".join(insert_statements)

    def save_sql_file(self, filename, insert_statements):
        """Guarda las sentencias SQL en un archivo .sql, con o sin transacción"""
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open(filename, 'w') as f:
            f.write("-- Archivo SQL generado\n")
            f.write(f"-- Fecha de creación: {current_datetime}\n\n")
            if self.use_transaction:
                f.write("BEGIN TRANSACTION;\n")
                f.write("SAVE TRANSACTION MiSavepoint;\n\n")
            f.write(insert_statements)
            if self.use_transaction:
                f.write("\n-- Si quieres deshacer los cambios usa:\n")
                f.write("ROLLBACK TRANSACTION MiSavepoint;\n")
                f.write("COMMIT;\n")


# Ejemplo de uso:

columns = [
    {'name': 'iddatabase', 'type': 'enum', 'values': ['AGROVISIONCORP']},  # No es único
    {'name': 'idempresa', 'type': 'enum', 'values': ['001', '002']},  # No es único
    {'name': 'iddevice', 'type': 'string', 'length': 10, 'pk': True},  # PK y único
    {'name': 'imei', 'type': 'int', 'min': 100000000000, 'max': 999999999999, 'unique': True},  # IMEI único
    {'name': 'numero', 'type': 'int', 'min': 1000000, 'max': 9999999},
    {'name': 'idtipodevice', 'type': 'enum', 'values': ['MOBILE']},
    {'name': 'marca', 'type': 'enum', 'values': ['SAMSUNG', 'RENO', 'PRO13', 'MOTO', 'OPPO', 'NOKIA']},
    {'name': 'modelo', 'type': 'string', 'length': 3},
    {'name': 'fechaactualizacion', 'type': 'datetime'},  # datetime
    {'name': 'observacion', 'type': 'string', 'length': 20, 'nullable': True},
    {'name': 'activo', 'type': 'int', 'min': 1, 'max': 1},
    {'name': 'nombre', 'type': 'name', 'nullable': True},  # Nombre aleatorio
    {'name': 'direccion', 'type': 'address', 'nullable': True},  # Dirección aleatoria
    {'name': 'usuariocreacion', 'type': 'enum', 'values': ['ERUBIO', 'PSANTAMARIA', 'JSUPO']}
]

# Generar 5 filas ficticias de datos para la tabla "device"
table_name = "device"
num_rows = 5
use_transaction = True

data_generator = DataGenerator(table_name, columns, num_rows, use_transaction)
insert_statements = data_generator.generate_insert_statements()

# Guardar en archivo .sql
data_generator.save_sql_file("generated_inserts.sql", insert_statements)

print(f"SQL file 'generated_inserts.sql' se ha creado con {num_rows} INSERT statements.")

# Ejemplo con otra tabla

columns_2 = [
    {'name': 'idpersona', 'type': 'string', 'length': 8, 'pk': True},  # PK y único
    {'name': 'nombre', 'type': 'name', 'nullable': False},  # Nombre siempre generado
    {'name': 'apellido', 'type': 'name', 'nullable': False},  # Apellido siempre generado
    {'name': 'edad', 'type': 'int', 'min': 18, 'max': 80},
    {'name': 'direccion', 'type': 'address', 'nullable': False},  # Dirección siempre generada
    {'name': 'telefono', 'type': 'int', 'min': 1000000000, 'max': 9999999999, 'unique': True},  # Teléfono único
    {'name': 'fecharegistro', 'type': 'datetime'},  # Fecha de registro
    {'name': 'estado', 'type': 'enum', 'values': ['Activo', 'Inactivo']}
]

table_name_2 = "personas"
num_rows_2 = 3

data_generator_2 = DataGenerator(table_name_2, columns_2, num_rows_2, use_transaction=False)
insert_statements_2 = data_generator_2.generate_insert_statements()

# Guardar en archivo .sql
data_generator_2.save_sql_file("generated_personas.sql", insert_statements_2)

print(f"SQL file 'generated_personas.sql' se ha creado con {num_rows_2} INSERT statements.")
