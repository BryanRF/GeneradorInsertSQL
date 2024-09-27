class JavaCodeGenerator(CodeGeneratorBase):
    def generate_code(self, data):
        code = "import java.util.*;\n\n"
        code += "public class Main {\n"
        code += "    public static void main(String[] args) {\n"
        code += "        List<List<String>> data = new ArrayList<>();\n"
        for row in data:
            values = ', '.join(f'"{v}"' if isinstance(v, str) else str(v) for v in row.values())
            code += f"        data.add(Arrays.asList({values}));\n"
        code += "        for (List<String> item : data) {\n"
        code += "            System.out.println(item);\n"
        code += "        }\n"
        code += "    }\n"
        code += "}\n"
        return code
