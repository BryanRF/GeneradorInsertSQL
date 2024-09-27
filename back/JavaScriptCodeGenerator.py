class JavaScriptCodeGenerator(CodeGeneratorBase):
    def generate_code(self, data):
        code = "const data = [\n"
        for row in data:
            values = ', '.join(f'"{v}"' if isinstance(v, str) else str(v) for v in row.values())
            code += f"    {{{values}}},\n"
        code += "];\n"
        code += "data.forEach(item => console.log(item));\n"
        return code
