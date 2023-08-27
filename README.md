BiT-ReNU - BIdirectional Transformation of Requirements in Natural Language and UML class models
------------------------------------------------------------------------------------------------------
DOI: [![DOI](https://zenodo.org/badge/606422705.svg)](https://zenodo.org/badge/latestdoi/606422705)


A tool for transforming requirements in UML/NL into NL/UML with the use of a SQL database as an intermediate model.


- by Markus Bimassl
- as part of the master thesis "Bidirectional transformation of natural-language requirements to and from UML class models for Model-Driven Development"
- at Vienna University of Economics and Business




Tool description:
--------------------------------------------------------------------------------------
This tool can import requirements in natural language (NL) or as a UML class model in the plantuml notation. The tool is then able to transform the imported requirements into a db-schema that functinos as an intermediate model. The tool can also transform the intermediate model into NL/UML, enabling the transformation from NL/UML into UML/NL.

NOTE: The tool has limitations that are described in the master thesis "Bidirectional transformation of natural-language requirements to and from UML class models for Model-Driven Development" by Markus Bimassl.




File descriptions:
--------------------------------------------------------------------------------------

BiT-ReNU example script:
------------------------
bitrenu.py:
File to try out BiT-ReNU.



BiT-ReNU Modules:
-----------------
The code for the tool is located in "python_scripts"

DB_module.py:
Holds all functions that are needed to connect to the database, as well as read and write to it.

NL_module.py:
Holds all functions that are needed to transform requirements from NL into the intermediate model representation, as well as the reverse transformations from the intermediate model into NL.

UML_module.py:
Holds all functions that are needed to transform requirements from a UML class model into the intermediate model representation, as well as the reverse transformations from the intermediate model into a UML class model.



Additional BiT-ReNU files:
--------------------------
project_databases:
The folder where BiT-ReNU stores the project databases.


Test scripts:
-------------
The scripts that were used to perform several validation and performance tests.

test_AN.py:
"AN" -> "Alterations in NL"
All tests were UML is tranformed into NL, then NL is changed, and then NL is
transformed back to UML.

test_AU.py:
"AU" -> "Alterations in UML"
All tests were NL is transformed into UML, then UML is changed, and then UML is
transformed back to NL.

test_BT.py:
"BT" -> "Bidirectional Transformation"
Tests were the roundtripping (UML -> NL -> UML, NL -> UML -> NL) is tested.

test_PT.py:
"PT" -> "Performance Tests"
Tests that measure execution time and memory usage of one-way (NL -> UML or 
UML -> NL) transformations.


Test files and documentation:
-----------------------------
Additional files for testing. Input/Output files and documentation. Can be found
in the "Test_files" folder.

AN:
All files used/created during the "Alterations in NL" tests.

AU:
All files used/created during the "Alterations in UML" tests.

BT:
All files used/created during the "Bidirectional Transformation" tests.

PT:
All files used/created during the "Performance Tests" tests.




Additional files/folder:
-----------------------
requirements.txt:
The used python modules.

IREB_modeling_practice_exam:
The IREB CPRE-AL Modeling practice exam. The sample class model/requirements for
the performed tests was derived from one of the exam models. 

SLR:
Holds the documentation of the systematic literature search that was conducted as part of the master thesis.




How to install and run the tool:
--------------------------------------------------------------------------------------

Dependencies can be found in the requirements.txt file.

Additional steps might be needed to install the used ML-model for spacy:
(code taken from https://spacy.io/usage)

pip install -U pip setuptools wheel

pip install -U spacy

python -m spacy download en_core_web_sm





How to use the tool:
--------------------------------------------------------------------------------------
The master thesis "Bidirectional transformation of natural-language requirements to and from UML class models for Model-Driven Development" explains the general dataflow between the modules, the user, the database, and a plantuml-file.

Additionally, the file bitrenu.py can be used as an example of how to use the individual functions of the tool.


