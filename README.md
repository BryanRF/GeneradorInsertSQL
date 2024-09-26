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

Este archivo `README.md` proporciona una guía completa sobre cómo configurar y ejecutar el generador de scripts SQL con datos ficticios. ¡Espero que te sea útil!
