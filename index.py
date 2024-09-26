import random
import string
import datetime

# Almacenamiento para valores únicos
unique_values = {}

def random_string(length=10):
    """Genera una cadena aleatoria de longitud fija"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def random_number(min_value=1000, max_value=9999, unique=False, field_name=None):
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

def random_date(start_year=2000, end_year=2024):
    """Genera una fecha aleatoria dentro de un rango de años"""
    start_date = datetime.date(start_year, 1, 1)
    end_date = datetime.date(end_year, 12, 31)
    random_days = random.randint(0, (end_date - start_date).days)
    return start_date + datetime.timedelta(days=random_days)

def random_datetime(start_year=2000, end_year=2024):
    """Genera una fecha y hora aleatoria dentro de un rango de años"""
    start_date = datetime.datetime(start_year, 1, 1)
    end_date = datetime.datetime(end_year, 12, 31, 23, 59, 59)
    random_seconds = random.randint(0, int((end_date - start_date).total_seconds()))
    return start_date + datetime.timedelta(seconds=random_seconds)

def random_enum(options):
    """Devuelve un valor aleatorio de una lista de opciones"""
    return random.choice(options)

def generate_insert_statement(table_name, columns, num_rows=1):
    """Genera una sentencia INSERT INTO con valores ficticios"""
    
    insert_statements = []
    
    for _ in range(num_rows):
        values = []
        for column in columns:
            col_name = column['name']
            col_type = column['type']
            nullable = column.get('nullable', False)
            unique = column.get('unique', False)
            is_pk = column.get('pk', False)
            
            # Si el campo es nullable, existe una probabilidad de que el valor sea NULL
            if nullable and random.random() < 1:  # 20% de probabilidad de que sea NULL
                values.append("NULL")
            else:
                if col_type == 'string':
                    length = column.get('length', 10)
                    if is_pk:  # PK debe ser único
                        value = random_string(length)
                        while value in unique_values.get(col_name, set()):
                            value = random_string(length)
                        unique_values.setdefault(col_name, set()).add(value)
                        values.append(f"N'{value}'")
                    else:
                        values.append(f"N'{random_string(length)}'")
                elif col_type == 'int':
                    min_value = column.get('min', 1000)
                    max_value = column.get('max', 9999)
                    if unique or is_pk:  # Asegurar que IMEI y PK sean únicos
                        value = random_number(min_value, max_value, unique=True, field_name=col_name)
                        values.append(str(value))
                    else:
                        values.append(str(random_number(min_value, max_value)))
                elif col_type == 'date':
                    values.append(f"N'{random_date()}'")
                elif col_type == 'datetime':
                    values.append(f"N'{random_datetime()}'")
                elif col_type == 'enum':
                    enum_values = column['values']
                    values.append(f"N'{random_enum(enum_values)}'")
                elif col_type == 'static':
                    static_value = column['value']
                    values.append(f"N'{static_value}'")
        
        # Construyendo la sentencia INSERT
        col_names = ", ".join([col['name'] for col in columns])
        col_values = ", ".join(values)
        insert_statement = f"INSERT INTO {table_name} ({col_names}) VALUES ({col_values});"
        insert_statements.append(insert_statement)
    
    return "\n".join(insert_statements)


def save_sql_file(filename, insert_statements):
    """Guarda las sentencias SQL en un archivo .sql junto con BEGIN TRANSACTION"""
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open(filename, 'w') as f:
        f.write("-- Archivo SQL generado\n")
        f.write(f"-- Fecha de creación: {current_datetime}\n\n")
        f.write("BEGIN TRANSACTION;\n")
        f.write("SAVE TRANSACTION MiSavepoint;\n\n")
        f.write(insert_statements)
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
    {'name': 'marca', 'type': 'enum', 'values': ['SAMSUNG', 'RENO', 'PRO13', 'MOTO', 'OPPO', 'RENO 7', 'NOKIA', 'S20+', 'GX912']},
    {'name': 'modelo', 'type': 'string', 'length': 3},
    {'name': 'actualizacion', 'type': 'int', 'min': 0, 'max': 0},
    {'name': 'fechaactualizacion', 'type': 'datetime'},  # Ahora es datetime
    {'name': 'idestado', 'type': 'enum', 'values': ['INO', 'AC', 'PER']},
    {'name': 'observacion', 'type': 'string', 'length': 20, 'nullable': True},
    {'name': 'activo', 'type': 'int', 'min': 1, 'max': 1},
    {'name': 'fechacreacion', 'type': 'datetime'},  # Este es datetime
    {'name': 'usuariocreacion', 'type': 'enum', 'values': ['ERUBIO', 'PSANTAMARIA', 'JSUPO']},
    {'name': 'usuarioalteracion', 'type': 'enum', 'values': ['ERUBIO', 'PSANTAMARIA', 'JSUPO']},
    {'name': 'version_apk', 'type': 'int', 'min': 1, 'max': 5},
    {'name': 'chip', 'type': 'int', 'min': 0, 'max': 1},
    {'name': 'acta', 'type': 'int', 'min': 0, 'max': 1},
    {'name': 'acta_url', 'type': 'string', 'length': 50, 'nullable': True},
    {'name': 'idcategoria', 'type': 'enum', 'values': ['CORP', 'LAB', 'CORP', 'SPR']},
    {'name': 'responsable', 'type': 'string', 'length': 30, 'nullable': True},
    {'name': 'usuario', 'type': 'string', 'length': 10, 'nullable': True},
    {'name': 'idsubarea', 'type': 'enum', 'values': ['A0009', 'A0006', 'A0008']},
    {'name': 'fechaultimaentrega', 'type': 'datetime', 'nullable': True},  # Este es datetime
    {'name': 'fechaultimadevolucion', 'type': 'datetime', 'nullable': True},  # Este es datetime
    {'name': 'fechaultimaexportacion', 'type': 'datetime', 'nullable': True}  # Este es datetime
]

# Generar 5 filas ficticias de datos para la tabla "device"
table_name = "device"
num_rows = 5
insert_statements = generate_insert_statement(table_name, columns, num_rows)

# Guardar en archivo .sql
save_sql_file("generated_inserts.sql", insert_statements)

print(f"SQL file 'generated_inserts.sql' se ha creado con {num_rows} INSERT statements.")
