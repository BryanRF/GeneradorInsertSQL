import random
import string
import datetime
import uuid
import names  # Import para generación de nombres

class DataGenerator:
    def __init__(self):
        self.unique_values = {}

    def random_string(self, length=10):
        """Genera una cadena aleatoria de longitud fija."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def random_int(self, min_value=0, max_value=1000):
        """Genera un número entero aleatorio dentro de un rango."""
        return random.randint(min_value, max_value)

    def random_float(self, min_value=0.0, max_value=1000.0, decimals=2):
        """Genera un número flotante aleatorio dentro de un rango."""
        return round(random.uniform(min_value, max_value), decimals)

    def random_boolean(self):
        """Genera un valor booleano aleatorio."""
        return random.choice([True, False])

    def random_date(self, start_year=2000, end_year=2024):
        """Genera una fecha aleatoria dentro de un rango de años."""
        start_date = datetime.date(start_year, 1, 1)
        end_date = datetime.date(end_year, 12, 31)
        return start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))

    def random_datetime(self, start_year=2000, end_year=2024):
        """Genera una fecha y hora aleatoria."""
        start_date = datetime.datetime(start_year, 1, 1)
        end_date = datetime.datetime(end_year, 12, 31, 23, 59, 59)
        return start_date + datetime.timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))

    def random_hour(self):
        """Genera una hora aleatoria."""
        return datetime.time(random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))

    def random_uuid(self):
        """Genera un UUID único."""
        return str(uuid.uuid4())

    def random_enum(self, options):
        """Genera un valor aleatorio de una lista de opciones (enum)."""
        return random.choice(options)

    def random_email(self, domain_list=None):
        """Genera un correo electrónico aleatorio."""
        domain_list = domain_list or ["example.com", "test.org", "demo.net"]
        return f"{self.random_string(8)}@{random.choice(domain_list)}"

    def random_phone(self, digits=8, unique=False, field_name=None):
        """Genera un número de teléfono aleatorio con una cantidad definida de dígitos, opcionalmente único."""
        if unique:
            if field_name not in self.unique_values:
                self.unique_values[field_name] = set()
            
            while True:
                number = ''.join(random.choices(string.digits, k=digits))
                if number not in self.unique_values[field_name]:
                    self.unique_values[field_name].add(number)
                    return number
        return ''.join(random.choices(string.digits, k=digits))

    def random_name(self):
        """Genera un nombre aleatorio utilizando la librería `names`."""
        return names.get_full_name()

    def value_or_null(self, generator_func, nullable=False, null_chance=0.1):
        """Devuelve un valor generado o `None` si nullable es True y se cumple la probabilidad."""
        if nullable and random.random() < null_chance:
            return None
        return generator_func()

    def generate_data(self, schema):
        """Genera datos aleatorios basados en un esquema proporcionado."""
        data = {}
        for field, specs in schema.items():
            field_type = specs.get('type')
            nullable = specs.get('nullable', False)
            
            if field_type == 'string':
                length = specs.get('length', 10)
                data[field] = self.value_or_null(lambda: self.random_string(length), nullable)
            elif field_type == 'int':
                min_value = specs.get('min', 0)
                max_value = specs.get('max', 1000)
                data[field] = self.value_or_null(lambda: self.random_int(min_value, max_value), nullable)
            elif field_type == 'float':
                min_value = specs.get('min', 0.0)
                max_value = specs.get('max', 1000.0)
                decimals = specs.get('decimals', 2)
                data[field] = self.value_or_null(lambda: self.random_float(min_value, max_value, decimals), nullable)
            elif field_type == 'boolean':
                data[field] = self.value_or_null(self.random_boolean, nullable)
            elif field_type == 'date':
                start_year = specs.get('start_year', 2000)
                end_year = specs.get('end_year', 2024)
                data[field] = self.value_or_null(lambda: self.random_date(start_year, end_year), nullable)
            elif field_type == 'datetime':
                start_year = specs.get('start_year', 2000)
                end_year = specs.get('end_year', 2024)
                data[field] = self.value_or_null(lambda: self.random_datetime(start_year, end_year), nullable)
            elif field_type == 'hour':
                data[field] = self.value_or_null(self.random_hour, nullable)
            elif field_type == 'enum':
                options = specs.get('options', [])
                data[field] = self.value_or_null(lambda: self.random_enum(options), nullable)
            elif field_type == 'email':
                domain_list = specs.get('domain_list', None)
                data[field] = self.value_or_null(lambda: self.random_email(domain_list), nullable)
            elif field_type == 'phone':
                digits = specs.get('digits', 8)
                unique = specs.get('unique', False)
                data[field] = self.value_or_null(lambda: self.random_phone(digits, unique, field_name=field), nullable)
            elif field_type == 'uuid':
                data[field] = self.value_or_null(self.random_uuid, nullable)
            elif field_type == 'name':
                data[field] = self.value_or_null(self.random_name, nullable)
            else:
                raise ValueError(f"Tipo de dato desconocido: {field_type}")
        return data
