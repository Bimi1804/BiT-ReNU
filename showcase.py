# Showcase of BiT-ReNU

#-------------------------------- Imports --------------------------------#
from bitrenu import *
import os
script_path = os.path.abspath(__file__)
main_folder = os.path.dirname(script_path)

#----------------------------- Use BiT-ReNU ------------------------------------#
def execute_showcase():
    # Import a NL file:
    with open(main_folder+"\\Test_files\\PT\\input_NL.txt") as file:
        lines = file.readlines()
        nl_input = []
        for l in lines:
            l = l.replace("\n","")
            nl_input.append(l)

    # Import a UML file:
    with open(main_folder+"\\Test_files\\PT\\input_UML.txt") as file:
        uml_input = file.read()


    # Create new BiTReNU object and use it for T2M transformation:-----------------
    BiTReNU1 = BiTReNU_UI("Showcase1")
    # Transform NL to UML:
    transformed_UML = BiTReNU1.nl_to_uml(nl_input)
    print(transformed_UML)
    df = BiTReNU1.DB_Handler.read_all_db()

    # Transform back to NL:
    transformed_NL = BiTReNU1.uml_to_nl(transformed_UML)
    print(transformed_NL)

    # Delete database file:
    BiTReNU1.DB_Handler.delete_db_file(BiTReNU1.project_name)


    # Create new BiTReNU object and use it for M2T transformation:-----------------
    BiTReNU2 = BiTReNU_UI("Showcase2")
    # Transform UML to NL:
    transformed_NL = BiTReNU2.uml_to_nl(uml_input)
    print(transformed_NL)

    # Transform back to UML:
    transformed_UML = BiTReNU2.nl_to_uml(transformed_NL)
    print(transformed_UML)

    # Delete database file:
    BiTReNU2.DB_Handler.delete_db_file(BiTReNU2.project_name)

#execute_showcase()




# Create new BiTReNU object and use it for T2M transformation:-----------------


input("Press any key to create a new BiTReNU Object:---------------")
BiTReNU_ex = BiTReNU_UI("Example")
print("")
print(f"Type of BiTReNU object = {type(BiTReNU_ex)}")
print("")


input("Import requirements in NL:-----------------")
# Import a NL file:
with open(main_folder+"\\Test_files\\PT\\input_NL.txt") as file:
    lines = file.readlines()
    original_NL = []
    for l in lines:
        l = l.replace("\n","")
        original_NL.append(l)
counter = 0
for i in original_NL:
    print(i)
    counter = counter +1
print("")
print(f"{counter} requirements imported")
print("")


input("Transform NL into UML:---------------------")
# Transform NL to UML:
transformed_UML = BiTReNU_ex.nl_to_uml(original_NL)

print(transformed_UML)


input("Show DB-content:--------------------------------------------")
db_content = BiTReNU_ex.DB_Handler.read_all_db()
for i in db_content:
    print(i)
    print("")


input("Transform the UML back into NL:------------------------------")
final_NL = BiTReNU_ex.uml_to_nl(transformed_UML)
counter_final = 0
for i in final_NL:
    print(i)
    counter_final = counter_final +1
print("")
print(f"{counter} requirements transformed")
print("")


input("Compare difference between original NL and final NL:------------------------------")
original_set = set(original_NL)
final_set = set(final_NL)
only_original = list(original_set - final_set)
only_final = list(final_set - original_set)
print("")
print(f"Sentences only in original NL: {len(only_original)}")
print(f"Sentences only in final NL: {len(only_final)}")

# Delete database file:
BiTReNU_ex.DB_Handler.delete_db_file(BiTReNU_ex.project_name)








