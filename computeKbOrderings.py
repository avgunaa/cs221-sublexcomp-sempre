import createRelationTables as script
import os.path
import ast
import os
from collections import defaultdict

KB_ORDER_STORAGE_DIR = 'kbOrdering'

def calculateF1(totalGuessed, correct, totalCorrect):
        p = 1.0 * correct / totalGuessed # no. of text relation pairs found in kb table / no. of text subjects found in kb table
        r = 1.0 * correct / totalCorrect # no. of text relation pairs found in kb table / no. of pairs in text relation
        return 2 * p * r / (p + r)

class KbStats{
    def __init__(self, alignment):
        self.alignment = alignment
     
    def setStats(self, kbFile, source, lexeme, intersectCount, kbSize, textSize, f1, best):
        self.alignment = {}
        self.features = {}
        
        self.alignment['formula'] = kbFile
        self.alignment['source'] = source
        self.alignment['features'] = self.features
        self.alignment['lexeme'] = text_file
        
        self.features['INTERSECTION_SIZE'] = intersectCount
        self.features['KB_SIZE'] = kbSize
        self.features['TEXT_SIZE'] = textSize
        self.features['F1'] = f1
        self.features['BEST'] = best
        
    def __str__(self):
        return str(self.alignment)
}

def computeKbOrderings(dataDir):
    '''
    format: tab-joined relation and F1 score
    kbOrderings ['born in'] = ['birthplace is   0.8', ...]
    '''
    # Set-up table storage directory
    script.setupStorageDirectory(KB_ORDERING_FILENAME)
    
    # Get file names
    kbFiles = os.listdir(script.KB_STORAGE_DIR))
    textFiles = os.listdir(script.TEXT_STORAGE_DIR)
    
    # Calculate self.kbOrderings
    for tFile in textFiles:
        tFilepath = os.path.join(script.TEXT_STORAGE_DIR, tFile)
        with open(tFilepath, 'r') as fp1:
            tTriples = set(fp1.readlines())
            
            stats = []
            for kbFile in kbFiles:
                kbFilepath = os.path.join(script.KB_STORAGE_DIR, kbFile)
                with open(kbFilepath, 'r') as fp2:
                    kbTriples = set(fp2.readlines())
                    
                    stats.append(KbStats(kbFile, source, lexeme, intersectCount, kbSize, textSize, fa, best))
            
            # Sort stats
            # TODO
                    
            # Store stats to file
            '''
            with open(filepath, 'w') as f:
                f.write(str(kbStats))
            '''
if __name__ == '__main__':
    print computeKbOrderings(script.GINA_DATA_RELATIVE_DIR)
