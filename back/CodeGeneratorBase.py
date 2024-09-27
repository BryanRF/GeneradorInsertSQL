class CodeGeneratorBase:
    def generate_code(self, data):
        """Método abstracto para generar el código en el lenguaje específico. Debe ser sobrescrito."""
        raise NotImplementedError("Este método debe ser implementado por las subclases.")
