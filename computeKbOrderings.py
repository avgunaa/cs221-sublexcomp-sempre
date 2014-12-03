import createRelationTables as script
import os.path
import ast
import os
from collections import defaultdict
from random import shuffle
import random

KB_ORDER_STORAGE_DIR = 'kbOrdering'
TEST_DATA_STORAGE_DIR = 'testData'

def calculateF1(totalGuessed, correct, totalCorrect):
        p = 1.0 * correct / totalGuessed # no. of text relation pairs found in kb table / no. of text subjects found in kb table
        r = 1.0 * correct / totalCorrect # no. of text relation pairs found in kb table / no. of pairs in text relation
        return 2 * p * r / (p + r)

class KbStats():
    def __init__(self, alignment):
        self.alignment = alignment
     
    def setStats(self, kbFile, textFile, source, intersectCount, kbSize, textSize, f1, best):
        self.alignment = {}
        self.features = {}
        
        self.alignment['formula'] = kbFile
        self.alignment['source'] = source
        self.alignment['features'] = self.features
        self.alignment['lexeme'] = textFile
        
        self.features['INTERSECTION_SIZE'] = intersectCount
        self.features['KB_SIZE'] = kbSize
        self.features['TEXT_SIZE'] = textSize
        self.features['F1'] = f1
        self.features['BEST'] = best
        
    def __str__(self):
        return str(self.alignment)

def splitTrainTestData():
    script.setupStorageDirectory(TEST_DATA_STORAGE_DIR)
    
    textFiles = os.listdir(script.TEXT_STORAGE_DIR)
    
    # Calculate self.kbOrderings
    for textFile in textFiles:
        tFilepath = os.path.join(script.TEXT_STORAGE_DIR, textFile)
        textTriples = []
        with open(tFilepath, 'r') as fp1:
            textTriples = list(set(fp1.readlines()))
            
        # Randomly divide into train and test data, 90/10
        shuffle(textTriples)
        count = len(textTriples)/10 + int(round(random.random() * (len(textTriples) % 10))) # To allow relations with low triple count a chance to be test data
        
        with open(os.path.join(TEST_DATA_STORAGE_DIR, textFile), 'w') as testFp:
            for textTriple in textTriples[:count]:
                testFp.write(textTriple)
                
def computeKbOrderings(kbStorageDir, source):
    '''
    format: tab-joined relation and F1 score
    kbOrderings ['born in'] = ['birthplace is   0.8', ...]
    '''
    # Set-up table storage directory
    script.setupStorageDirectory(KB_ORDER_STORAGE_DIR)
    
    # Delete results file if it exists already
    resultsFilepath = os.path.join(KB_ORDER_STORAGE_DIR, source)
    if os.path.exists(resultsFilepath):
        os.remove(resultsFilepath)
        
    # Get file names
    kbFiles = os.listdir(kbStorageDir)
    textFiles = os.listdir(script.TEXT_STORAGE_DIR)
    
    # Calculate self.kbOrderings
    for textFile in textFiles:
        tFilepath = os.path.join(script.TEXT_STORAGE_DIR, textFile)
        testFilepath = os.path.join(TEST_DATA_STORAGE_DIR, textFile)
        
        # Get training triples
        textTriples = set([])
        with open(tFilepath, 'r') as fp1: # Get text triples
            textTriples = set(fp1.readlines())
        with open(testFilepath, 'r') as testFp: # Remove test triples
            textTriples -= set(testFp.readlines())

        stats = []
        textTriples = set(textTriples)
        textSubjects = set([x.split()[0] for x in textTriples]) # To calculate F1 score
        
        for kbFile in kbFiles:
            kbFilepath = os.path.join(script.KB_STORAGE_DIR, kbFile)
            kbTriples = set()
            with open(kbFilepath, 'r') as fp2:
                kbTriples = set(fp2.readlines())
                
            intersection = textTriples & kbTriples
            # Early exit if no intersecting triples
            if len(intersection) is 0:
                continue
                
            #source
            intersectCount = len(intersection)
            kbSize = len(kbTriples)
            textSize = len(textTriples)
            
            # Calculate F1 score
            kbSubjects = [x.split()[0] for x in kbTriples]
            totalGuessed = 0
            for x in kbSubjects:
                if x in textSubjects:
                    totalGuessed += 1
            f1 = calculateF1(totalGuessed, intersectCount, textSize)
            
            # Add new KbStat to stats
            stats.append(KbStats(kbFile, textFile, source, intersectCount, kbSize, textSize, f1, False))
            print '.'
        
        # Sort stats
        sortedStats = sorted(stats, key=lambda x: x.alignment['features']['F1'], reverse=True)
        sortedStats[0].alignment['features']['BEST'] = True
        
        # Store stats to file
        with open(resultsFilepath, 'a') as f:
            for s in stats:
                f.write(str(s))
        print '\nDone\n'

if __name__ == '__main__':
    #splitTrainTestData()
    computeKbOrderings(script.KB_STORAGE_DIR, 'testing')
