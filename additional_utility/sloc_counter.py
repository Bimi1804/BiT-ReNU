# Count SLOC:
import re
import os
script_path = os.path.abspath(__file__)
main_folder = os.path.dirname(script_path).replace("additional_utility","")


def count_sloc(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # Regular expression to match single-line comments and empty lines
    single_line_comment_pattern = re.compile(r'#.*$')
    sloc_count = 0
    in_multi_line_comment = False
    for line in lines:
        # Remove leading and trailing whitespace
        cleaned_line = line.strip()
        # Check if the line is empty
        if not cleaned_line:
            continue
        # Check if the line starts a multi-line comment
        if cleaned_line.startswith("'''") or cleaned_line.startswith('"""'):
            in_multi_line_comment = not in_multi_line_comment
        # If not in a multi-line comment, check for single-line comments
        if not in_multi_line_comment and not single_line_comment_pattern.match(cleaned_line):
            if cleaned_line != '"""':
            	sloc_count += 1
            	#print(cleaned_line)
    return sloc_count



if __name__ == "__main__":
    UI_sloc = count_sloc(f"{main_folder}bitrenu.py")
    print(f"BitReNU-UI: {UI_sloc}")
    DB_module_sloc = count_sloc(f"{main_folder}python_scripts/DB_module.py")
    print(f"DB_module: {DB_module_sloc}")
    NL_module_sloc = count_sloc(f"{main_folder}python_scripts/NL_module.py")
    print(f"NL_module: {NL_module_sloc}")
    UML_module_sloc = count_sloc(f"{main_folder}python_scripts/UML_module.py")
    print(f"UML_module: {UML_module_sloc}")
    print("")
    print(f"Total SLOC: {UI_sloc+DB_module_sloc+NL_module_sloc+UML_module_sloc}")



    

