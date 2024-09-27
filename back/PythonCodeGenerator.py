class PythonCodeGenerator(CodeGeneratorBase):
    def generate_code(self, data):
        code = "data = [\n"
        for row in data:
            code += f"    {row},\n"
        code += "]\n"
        code += "for item in data:\n"
        code += "    print(item)\n"
        return code
