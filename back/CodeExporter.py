class CodeExporter:
    def __init__(self, language):
        if language == 'python':
            self.generator = PythonCodeGenerator()
        elif language == 'cpp':
            self.generator = CppCodeGenerator()
        elif language == 'javascript':
            self.generator = JavaScriptCodeGenerator()
        elif language == 'java':
            self.generator = JavaCodeGenerator()
        else:
            raise ValueError(f"Lenguaje de programación no soportado: {language}")
    
    def export(self, data):
        return self.generator.generate_code(data)
