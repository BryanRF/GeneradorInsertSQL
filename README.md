# GeneradorInsertSQL

Aquí tienes un ejemplo de un archivo `README.md` para tu proyecto de generación de scripts SQL:

---

# Generador de Scripts SQL con Datos Ficticios

Este proyecto es una herramienta en Python que genera sentencias `INSERT INTO` para tablas de bases de datos con valores ficticios. Incluye soporte para diferentes tipos de columnas, como `string`, `int`, `enum`, `date` y `datetime`, y permite garantizar unicidad en columnas clave como una llave primaria (`PK`) o campos únicos, como el IMEI. Además, permite generar un archivo `.sql` que contiene las sentencias `INSERT` junto con comandos de transacción (`BEGIN`, `SAVEPOINT`, `ROLLBACK`, `COMMIT`).

## Características

- Generación de valores ficticios para diferentes tipos de columnas (`string`, `int`, `enum`, `date`, `datetime`).
- Control de unicidad para campos como llaves primarias (`PK`) y otros campos únicos (como IMEI).
- Posibilidad de generar valores `NULL` en columnas configuradas como `nullable`.
- Soporte para diferentes tipos de datos como fechas (`date` y `datetime`).
- Generación de un archivo `.sql` con las sentencias `INSERT INTO` y manejo de transacciones (`BEGIN TRANSACTION`, `SAVEPOINT`, `ROLLBACK`, `COMMIT`).
- Personalización de la cantidad de filas generadas.

## Requisitos

- Python 3.x
- No es necesario instalar librerías externas, ya que usa solo módulos estándar de Python (`random`, `string`, `datetime`).

## Uso

### Configuración de las Columnas

Define la estructura de tu tabla en la variable `columns`, que es una lista de diccionarios. Cada diccionario representa una columna y contiene los siguientes campos:

- `name`: Nombre de la columna.
- `type`: Tipo de dato (`string`, `int`, `enum`, `date`, `datetime`).
- `length`: (Opcional) Longitud de la cadena para columnas de tipo `string`.
- `min`, `max`: (Opcional) Valores mínimos y máximos para columnas de tipo `int`.
- `values`: (Opcional) Lista de valores posibles para columnas de tipo `enum`.
- `nullable`: (Opcional) Si la columna permite valores `NULL` (por defecto es `False`).
- `unique`: (Opcional) Si la columna debe contener valores únicos.
- `pk`: (Opcional) Define si la columna es la llave primaria (`PK`).

Ejemplo de configuración:

```python
columns = [
    {'name': 'iddevice', 'type': 'string', 'length': 10, 'pk': True},  # PK y único
    {'name': 'imei', 'type': 'int', 'min': 100000000000, 'max': 999999999999, 'unique': True},  # IMEI único
    {'name': 'fechaactualizacion', 'type': 'datetime'},  # Fecha y hora
    {'name': 'idestado', 'type': 'enum', 'values': ['INO', 'AC', 'PER']},
    {'name': 'observacion', 'type': 'string', 'length': 20, 'nullable': True},
]
```

### Generar Sentencias SQL

Para generar las sentencias SQL de `INSERT INTO`, puedes llamar a la función `generate_insert_statement()` pasando el nombre de la tabla y la configuración de las columnas. Por ejemplo, para generar 5 filas ficticias:

```python
table_name = "device"
num_rows = 5
insert_statements = generate_insert_statement(table_name, columns, num_rows)
print(insert_statements)
```

### Guardar las Sentencias en un Archivo `.sql`

Para guardar las sentencias generadas en un archivo `.sql`, puedes utilizar la función `save_sql_file()`:

```python
save_sql_file("generated_inserts.sql", insert_statements)
```

Esto guardará el archivo `generated_inserts.sql` que contendrá:

- La fecha actual de creación.
- Sentencias `BEGIN TRANSACTION`, `SAVEPOINT`, `ROLLBACK`, y `COMMIT`.
- Las sentencias `INSERT INTO` generadas.

### Ejemplo de Archivo Generado

```sql
-- Archivo SQL generado
-- Fecha de creación: 2024-09-26 12:34:56

BEGIN TRANSACTION;
SAVE TRANSACTION MiSavepoint;

INSERT INTO device (iddatabase, idempresa, iddevice, imei, numero, idtipodevice, marca, modelo, actualizacion, fechaactualizacion, idestado, observacion, activo, fechacreacion, usuariocreacion, usuarioalteracion, version_apk, chip, acta, acta_url, idcategoria, responsable, usuario, idsubarea, fechaultimaentrega, fechaultimadevolucion, fechaultimaexportacion) VALUES (N'AGROVISIONCORP', N'001', N'G5TPHDAF7C', 128765091543, 8174234, N'MOBILE', N'S20+', N'R53', 0, N'2020-01-28', N'PER', NULL, 1, N'2020-05-01', N'ERUBIO', N'PSANTAMARIA', 1, 0, 1, N'URL_DUMMY', N'CORP', N'ERUBIO', NULL, N'A0009', NULL, NULL, NULL);

-- Si quieres deshacer los cambios usa:
ROLLBACK TRANSACTION MiSavepoint;
COMMIT;
```

### Ejecutar el Script

1. Configura las columnas en el script de Python.
2. Ejecuta el script en tu entorno Python para generar las sentencias SQL.
3. El archivo `generated_inserts.sql` será generado y listo para su uso en tu base de datos.

## Personalización

Puedes modificar fácilmente las configuraciones del script para adaptarlo a tu base de datos:

- Cambia los tipos de datos o agrega nuevas columnas.
- Ajusta la lógica para campos específicos.
- Configura cuántas filas quieres generar modificando el valor de `num_rows`.

## Contribución

Si deseas contribuir a este proyecto, puedes clonar el repositorio, hacer modificaciones y enviar pull requests. Sugerencias y mejoras son bienvenidas.

---

Para conectar todo esto (la generación de datos, exportación a archivos y la generación de código en diferentes lenguajes) con una **API REST en Django**, necesitas implementar un **backend en Django** utilizando **Django REST Framework (DRF)**. Vamos a dividir esto en pasos para hacer una API que exponga todas las funcionalidades que has desarrollado.

### **Pasos para integrar con una API REST en Django**

#### **1. Crear el proyecto de Django**

Primero, asegúrate de tener **Django** y **Django REST Framework** instalados:

```bash
pip install django djangorestframework
```

Luego, crea un proyecto Django y una aplicación donde vamos a trabajar:

```bash
django-admin startproject myproject
cd myproject
python manage.py startapp api
```

#### **2. Configuración inicial de Django**

Agrega la aplicación `api` y `rest_framework` a tu archivo `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'api',  # La aplicación donde manejaremos la API
]
```

#### **3. Crear los endpoints en la API**

##### **Definir las rutas en `api/urls.py`**

Define las rutas de la API para que los usuarios puedan interactuar con la generación de datos, la exportación a archivos y la generación de código.

```python
from django.urls import path
from . import views

urlpatterns = [
    path('generate-data/', views.GenerateDataView.as_view(), name='generate-data'),
    path('export-file/', views.ExportFileView.as_view(), name='export-file'),
    path('generate-code/', views.GenerateCodeView.as_view(), name='generate-code'),
]
```

##### **Definir los views en `api/views.py`**

Aquí es donde implementaremos la lógica para generar los datos y exportarlos en diferentes formatos o generar código en distintos lenguajes.

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .data_generator import DataGenerator  # Clase que ya implementamos
from .file_exporters import FileExporter   # Exportadores de archivos
from .code_exporters import CodeExporter   # Exportadores de código

class GenerateDataView(APIView):
    """Genera datos aleatorios basados en un esquema y los retorna como JSON."""
    def post(self, request):
        schema = request.data.get('schema', {})
        num_rows = request.data.get('num_rows', 10)
        
        data_generator = DataGenerator()
        generated_data = [data_generator.generate_data(schema) for _ in range(num_rows)]
        
        return Response(generated_data, status=status.HTTP_200_OK)


class ExportFileView(APIView):
    """Genera datos y los exporta en un archivo del formato especificado."""
    def post(self, request):
        schema = request.data.get('schema', {})
        num_rows = request.data.get('num_rows', 10)
        file_format = request.data.get('format', 'csv')  # csv, json, xml, excel
        file_name = request.data.get('file_name', 'output_file')

        # Generar los datos
        data_generator = DataGenerator()
        generated_data = [data_generator.generate_data(schema) for _ in range(num_rows)]

        # Exportar a archivo
        exporter = FileExporter(file_format)
        exporter.export(generated_data, f'{file_name}.{file_format}')

        return Response({"message": f"Archivo generado: {file_name}.{file_format}"}, status=status.HTTP_200_OK)


class GenerateCodeView(APIView):
    """Genera datos y devuelve el código en el lenguaje especificado (Python, C++, JS, Java)."""
    def post(self, request):
        schema = request.data.get('schema', {})
        num_rows = request.data.get('num_rows', 10)
        language = request.data.get('language', 'python')

        # Generar los datos
        data_generator = DataGenerator()
        generated_data = [data_generator.generate_data(schema) for _ in range(num_rows)]

        # Generar código
        code_exporter = CodeExporter(language)
        code = code_exporter.export(generated_data)

        return Response({"code": code}, status=status.HTTP_200_OK)
```

#### **4. Crear los Serializadores (opcional)**
Si quieres estructurar mejor los datos que recibe o envía la API, puedes utilizar **serializadores** en Django REST Framework. Para simplificar, el ejemplo anterior no los incluye, pero puedes definirlos en `serializers.py`.

#### **5. Definir la lógica de exportación y generación de código en `file_exporters.py` y `code_exporters.py`**
Los módulos `file_exporters.py` y `code_exporters.py` contendrán la lógica que ya creamos para exportar los datos a diferentes formatos y generar código en distintos lenguajes.

- **file_exporters.py** contendrá las clases `FileExporter`, `ExcelExporter`, `CSVExporter`, `JSONExporter`, `XMLExporter`.
- **code_exporters.py** contendrá las clases `CodeExporter`, `PythonCodeGenerator`, `CppCodeGenerator`, `JavaScriptCodeGenerator`, `JavaCodeGenerator`.

Ya que estos archivos ya los hemos creado en pasos anteriores, los puedes mover a estos archivos.

#### **6. Ejecutar el servidor**

Una vez que tengas todo configurado, ejecuta el servidor Django para comenzar a probar la API.

```bash
python manage.py runserver
```

#### **7. Ejemplo de cómo usar la API**

1. **Generar datos en JSON**:

   - Método: `POST`
   - URL: `/generate-data/`
   - Cuerpo del request:
     ```json
     {
       "schema": {
         "name": {"type": "name"},
         "age": {"type": "int", "min": 18, "max": 99},
         "email": {"type": "email"},
         "phone": {"type": "phone", "digits": 9},
         "created_at": {"type": "datetime"}
       },
       "num_rows": 10
     }
     ```

2. **Generar un archivo CSV**:

   - Método: `POST`
   - URL: `/export-file/`
   - Cuerpo del request:
     ```json
     {
       "schema": {
         "name": {"type": "name"},
         "age": {"type": "int", "min": 18, "max": 99},
         "email": {"type": "email"},
         "phone": {"type": "phone", "digits": 9},
         "created_at": {"type": "datetime"}
       },
       "num_rows": 10,
       "format": "csv",
       "file_name": "generated_data"
     }
     ```

3. **Generar código Python**:

   - Método: `POST`
   - URL: `/generate-code/`
   - Cuerpo del request:
     ```json
     {
       "schema": {
         "name": {"type": "name"},
         "age": {"type": "int", "min": 18, "max": 99},
         "email": {"type": "email"},
         "phone": {"type": "phone", "digits": 9},
         "created_at": {"type": "datetime"}
       },
       "num_rows": 10,
       "language": "python"
     }
     ```

### **Conclusión**

Con esta estructura, hemos conectado todo el sistema de generación de datos, exportación a diferentes formatos, y generación de código en diferentes lenguajes a una **API RESTful en Django**. Esto permite a los usuarios generar datos, exportarlos o generar código a través de solicitudes HTTP.

¿Te gustaría que profundicemos en algún otro aspecto, como la autenticación o la implementación de pruebas automatizadas para la API?