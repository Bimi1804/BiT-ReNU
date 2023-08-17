BiT-ReNU - BIdirectional Transformation of Requirements in Natural Language and UML class models
----------------------------------------------------------------------------------------------------
DOI: [![DOI](https://zenodo.org/badge/606422705.svg)](https://zenodo.org/badge/latestdoi/606422705)


A tool for transforming requirements in UML/NL into NL/UML with the use of a SQL database as an intermediate model.


- by Markus Bimassl
- as part of the master thesis "Bidirectional transformation of natural-language requirements to and from UML class models for Model-Driven Development"
- at Vienna University of Economics and Business




Tool description:
--------------------------------------------------------------------------------------
This tool can import requirements in natural language (NL) or as a UML class model in the plantuml notation. The tool is then able to transform the imported requirements into a db-schema that functinos as an intermediate model. The tool can also transform the intermediate model into NL/UML, enabling the transformation from NL/UML into UML/NL.

NOTE: The tool has limitations that are described in the master thesis "Bidirectional transformation of natural-language requirements to and from UML class models for Model-Driven Development" by Markus Bimassl-




File descriptions:
--------------------------------------------------------------------------------------

CODE:
----
The tool for the tool is located in "python_scripts"

DB_module.py:
Holds all functions that are needed to connect to the database, as well as read and write to it.

NL_module.py:
Holds all functions that are needed to transform requirements from NL into the intermediate model representation, as well as the reverse transformations from the intermediate model into NL.

UML_module.py:
Holds all functions that are needed to transform requirements from a UML class model into the intermediate model representation, as well as the reverse transformations from the intermediate model into a UML class model.


Additional files/folder:
-----------------------

Manually_transformed_Tests:
Holds the files that were manually created for the Validation tests that were conducted as part of the master thesis.

SLR:
Holds the documentation of the systematic literature search that was conducted as part of the master thesis.

Validation_Tests:
Holds all files that were created during the validation tests that were conducted as part of the master thesis.

eval_tests.py:
The python script that was used to conduct the validation tests.




How to install and run the tool:
--------------------------------------------------------------------------------------

Dependencies can be found in the requirements.txt file.

Additional steps might be needed to install the used ML-model for spacy:
(code taken from https://spacy.io/usage)

pip install -U pip setuptools wheel

pip install -U spacy

python -m spacy download en_core_web_sm


----------

The functions from the python files can simply be imported and used. However, some libraries are needed for each script:

DB_module.py:
- sqlite3
- os
- pandas

NL_module.py:
- re
- lemminflect
- inflect
- spacy

UML_module.py:
- os
- pandas




How to use the tool:
--------------------------------------------------------------------------------------
The master thesis "Bidirectional transformation of natural-language requirements to and from UML class models for Model-Driven Development" explains the general dataflow between the modules, the user, the database, and a plantuml-file.

Additionally, the file eval_test.py can be used as an example of how to use the individual functions of the tool.


