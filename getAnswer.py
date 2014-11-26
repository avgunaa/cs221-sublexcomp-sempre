import createRelationTables as script
import os.path
import ast
from collections import defaultdict


KB_ID_TO_RELATIONS_FILENAME = 'kbIdToRelations.txt'
KB_ORDERING_FILENAME = 'kbOrdering.txt'


def getTextToKbId (textStr):
    kbId = [textStr]
    if script.isATextDate(kbId):
        kbId = getTimeToKbTime(textStr)
    return kbId
    
def getTextToKbTime(textStr):
    kbTime = []
    dateSplit = text.split('-')
    for x in range(len(dateSplit), 0, -1):
        kbTime.append('"' + '-'.join(dateSplit[:x]) + '"^^xsd:datetime')
    return kbTime

def calculateF1(totalGuessed, correct, totalCorrect):
        p = 1.0 * correct / totalGuessed # no. of text relation pairs found in kb table / no. of text subjects found in kb table
        r = 1.0 * correct / totalCorrect # no. of text relation pairs found in kb table / no. of pairs in text relation
        return 2 * p * r / (p + r)
        
class questionAnswerer:
    def __init__(self, dataDir):
        self.directory = dataDir
        self.kbIdToRelations = defaultdict(set)
        self.computeKbIdToRelations()
        self.kbOrderings = {}
        self.computeKbOrderings()
    
    def computeKbIdToRelations(self):
        # If file exists, read in map and return
        filepath = os.path.join(self.directory, KB_ID_TO_RELATIONS_FILENAME)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                str = f.read()
                self.kbIdToRelations = ast.literal_eval(str)
                return
        
        # Calculate self.computeKbIdToRelations
        # TODO
        
        # Store map to file, serialized
        with open(filepath, 'w') as f:
            f.write(str(self.kbIdToRelations))
            
    def computeKbOrderings(self):
        '''
        format: tab-joined relation and F1 score
        kbOrderings ['born in'] = ['birthplace is   0.8', ...]
        '''
        # If file exists, read in map and return
        filepath = os.path.join(self.directory, KB_ORDERING_FILENAME)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                str = f.read()
                self.kbOrderings = ast.literal_eval(str)
                return
            
        # Calculate self.kbOrderings
        # TODO
        
        # Store map to file, serialized
        with open(filepath, 'w') as f:
            f.write(str(self.kbOrderings))
            
    def getAnswer(self, subject, textRelation):
        kbId = getTextToKbIds(subject)
        
        # Get closest knowledge base relations ordering
        textFilename = script.getRelationFilename(textRelation)
        kbOrdering = self.kbOrderings[textFilename]
        
        # Filter knowledge base relations list to ones containing the subject
        filteredKb = []
        for kb in kbOrdering:
            relation, score = kb.split('\t')
            if relation in self.kbIdToRelations[kbId]:
                filteredKb.append(kb)
                
        # Calculate answer
        def getObject(topRelation, kbId):
            # TODO
            return 
            
        topRelation, topScore = filteredKb[0].split('\t')
        answer = getObject(topRelation, kbId)
        return answer
        
if __name__ == '__main__':
    QA = questionAnswerer(script.GINA_DATA_RELATIVE_DIR)
    
    subject = ''
    textRelation = ''
    print QA.getAnswer(subject, textRelation)