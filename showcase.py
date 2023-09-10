# Showcase of BiT-ReNU

#-------------------------------- Imports --------------------------------#
from bitrenu import *
import os
script_path = os.path.abspath(__file__)
main_folder = os.path.dirname(script_path)

#----------------------------- Use BiT-ReNU ------------------------------------#
def execute_showcase():
    # Import a NL file:
    with open(main_folder+"\\Test_files\\PT\\PT04\\input_NL_PT04.txt") as file:
        lines = file.readlines()
        nl_input = []
        for l in lines:
            l = l.replace("\n","")
            nl_input.append(l)

    # Import a UML file:
    with open(main_folder+"\\Test_files\\PT\\PT01\\input_UML_PT01.txt") as file:
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

execute_showcase()