class CppCodeGenerator(CodeGeneratorBase):
    def generate_code(self, data):
        code = "#include <iostream>\n#include <vector>\nusing namespace std;\n\n"
        code += "int main() {\n"
        code += "    vector<vector<string>> data = {\n"
        for row in data:
            values = ', '.join(f'"{v}"' if isinstance(v, str) else str(v) for v in row.values())
            code += f"        {{{values}}},\n"
        code += "    };\n"
        code += "    for (auto& item : data) {\n"
        code += "        for (auto& field : item) cout << field << ' ';\n"
        code += "        cout << endl;\n"
        code += "    }\n"
        code += "    return 0;\n"
        code += "}\n"
        return code
