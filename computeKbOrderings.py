import createRelationTables as script
import os.path
import ast
from collections import defaultdict

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

class stats{
    
}

def computeKbOrderings(dataDir):
    '''
    format: tab-joined relation and F1 score
    kbOrderings ['born in'] = ['birthplace is   0.8', ...]
    '''
    # If file exists, read in map and return
    filepath = os.path.join(self.directory, KB_ORDERING_FILENAME)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            str = f.read()
            return ast.literal_eval(str)
        
    # Calculate self.kbOrderings
    for textRelation in :
        kbStats = []
        for kbRelation in :
            kbStats.append
    
    
    # Store map to file, serialized
    with open(filepath, 'w') as f:
        f.write(str(self.kbOrderings))
        
if __name__ == '__main__':
    print computeKbOrderings(script.GINA_DATA_RELATIVE_DIR)
