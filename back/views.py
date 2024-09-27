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
