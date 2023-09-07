# BiT-ReNU

#--------------------------- Import BiT-ReNU Modules --------------------------#
from python_scripts.DB_module import *
from python_scripts.NL_module import *
from python_scripts.UML_module import *

#--------------------------------- BiT-ReNU UI --------------------------------#
class BiTReNU_UI():
    """
    BiTReNU_UI provides an interface for the bidirectional Transformation 
    between NL and a UML class model.

    Parameters
    ----------
    project_name : str
        The name of the project for which UML and NL transformations will be
        performed. Used to name the database-file.

    Attributes
    ----------
    project_name : str
        The name of the current project.
    DB_Handler : DB_Handler
        An instance of the database handler for managing the database file.
    NL_Filter : NL_Filter
        An instance of the NL filtering module for processing NL requirements.
    NL_SQL_Transformer : NL_SQL_Transformer
        An instance of the NL to SQL transformation module.
    SQL_NL_Transformer : SQL_NL_Transformer
        An instance of the SQL to NL transformation module.
    SQL_UML_Transformer : SQL_UML_Transformer
        An instance of the SQL to UML transformation module.
    UML_SQL_Transformer : UML_SQL_Transformer
        An instance of the UML to SQL transformation module.

    Methods
    -------
    uml_to_nl(uml_input)
        Transform a UML class model into a set of requirements in NL.

    nl_to_uml(nl_input)
        Transform a set of requirements in NL into a UML class model.
    """

    def __init__(self, project_name):
        self.project_name = project_name
        # Initiate BiT-ReNU modules:
        # DB Module:--------------------------------------------
        self.DB_Handler = DB_Handler()
        # Set up new project:
        self.DB_Handler.create_new_project(self.project_name)
        self.DB_Handler.set_curr_project(self.project_name)
        # NL Modules:-------------------------------------------
        self.NL_Filter = NL_Filter()
        self.NL_SQL_Transformer = NL_SQL_Transformer()
        self.SQL_NL_Transformer = SQL_NL_Transformer()
        # UML-Module:-------------------------------------------
        self.SQL_UML_Transformer = SQL_UML_Transformer()
        self.UML_SQL_Transformer = UML_SQL_Transformer()
                
    def uml_to_nl(self,uml_input):
        """
        Transform a UML class model into a set of requirements in NL.

        Parameters
        ----------
        uml_input : str
            The UML class model as a plantuml string.

        Returns
        -------
        final_NL : list[str]
            A list of sentences, transformed from the input UML. 
        """
        # UML -> SQL:
        sql_statements = self.UML_SQL_Transformer.plantuml_to_sql(uml_input)
        self.DB_Handler.write_to_db(sql_statements)
        # SQL -> NL:
        df = self.DB_Handler.read_all_db()
        final_NL = self.SQL_NL_Transformer.transform_sql_nl(df)
        return final_NL

    def nl_to_uml(self,nl_input):
        """
        Transform a set of requirements in NL into a UML class model.

        Parameters
        ----------
        nl_input : list[str]
            A list of sentences as requirements.

        Returns
        -------
        final_NL : str
            The UML class model as a plantuml string, transformed from the NL input.
        """
        # NL -> SQL:
        filtered_nl = self.NL_Filter.filter_nl(nl_input)
        sql_queues = self.NL_SQL_Transformer.transform_nl_sql(filtered_nl)
        self.DB_Handler.write_to_db(sql_queues)
        # SQL -> UML:
        df = self.DB_Handler.read_all_db()
        final_UML = self.SQL_UML_Transformer.sql_to_plantuml(df)
        return final_UML




