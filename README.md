Sublexical Compositionality in Semantic Parsing
***************************************************************************************
Code:

***************************************************************************************
createRelationTables.py
  createRelationTables.py contains the functions getFreebaseTriples() and 
  getTextTriples() which take as input the data file and splits it into multiple
  files based on the relation between entities.
  For example, we create file "fb:place_of_birth" containing entity pairs.
  We also use the getXYZRelations() to obtain the relations formed by joining the kb tables.
  A subset of this data is present in kbTriples and textTriples in the data directory

  To Run :
    python createRelationTables

***************************************************************************************
template3Tables.py
  This file takes care of mostly template 3 and handles the creation of constant files.
  Exact match is also handled in this case.
  To Run
    python template3Tables.py

***************************************************************************************
computeKbOrderings.py
  computeKbOrdering.py is the file which aligns the text relations with the kb relations.
  It computes the features for the alignment and orders them based on the F1-score.
  To Run:
    python computeKbOrderings.py

***************************************************************************************
tester.py
  Four different testing methods have been implemented.
  To Run:
    python tester.py [ALIGNMENT DIRECTORY] [TEST METHOD]

***************************************************************************************
Data and test:

Entire data is present in www.stanford.edu/~avgunaa/sublex_comp/

Subset of the data has been provided in the zip file. The data used for sample evaluation is 
available in the kbTriples/ and textTriples/ directories.

Example alignment is present in kbOrdering/ directory and was obtained by running the computeKbOrderings.py
To run the tester on this alignment, use the following command:
  python tester.py data/kbOrdering/alignment_Template1 test1

The values obtained were as follows
alignment_Template1
test1 = 5.8
test2 = 0.72
test3 = 5.7
test4 = 0.48

alignment_Template4
test1 = 4.2
test2 = 0.17
test3 = 4.2
test4 = 0.02

***************************************************************************************

