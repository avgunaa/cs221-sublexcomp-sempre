import createRelationTables as script
import os.path
import ast
import os
from collections import defaultdict
from random import shuffle
import random

KB_ORDER_STORAGE_DIR = 'kbOrdering'
TEST_DATA_STORAGE_DIR = 'testData'
KB_ENTITY_INDEX_FILENAME = 'kbEntityIndex.txt'

def calculateF1(totalGuessed, correct, totalCorrect):
        p = 1.0 * correct / totalGuessed # no. of text relation pairs found in kb table / no. of text subjects found in kb table
        r = 1.0 * correct / totalCorrect # no. of text relation pairs found in kb table / no. of pairs in text relation
        return 2 * p * r / (p + r), p, r

class KbStats:   
    def __init__(self, kbFile, textFile, source, intersectCount, kbSize, textSize, f1, p, r):
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
        self.features['P'] = p
        self.features['R'] = r
        
    def __str__(self):
        return str(self.alignment)

def splitTrainTestData():
    # Set-up table storage directory
    if os.path.exists(TEST_DATA_STORAGE_DIR):
        print '\nWARNING: Data already split into training/test. Remove ' + TEST_DATA_STORAGE_DIR + 'directory to re-split.\n'
        return
    os.makedirs(TEST_DATA_STORAGE_DIR)
        
    textFiles = os.listdir(script.TEXT_STORAGE_DIR)
    
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
                
def computeKbOrdering(kbStorageDir, source):
    '''
    format: tab-joined relation and F1 score
    kbOrderings ['born in'] = ['birthplace is   0.8', ...]
    '''
    # Set-up table storage directory
    if not os.path.exists(KB_ORDER_STORAGE_DIR):
        os.makedirs(KB_ORDER_STORAGE_DIR)
    
    if not os.path.exists(KB_ORDER_STORAGE_DIR+'/'+'alignment'+'_'+source+'_'+kbStorageDir):
        os.makedirs(KB_ORDER_STORAGE_DIR+'/'+'alignment'+'_'+source+'_'+kbStorageDir)
    else:
        print "Alignment for setup already exists"
        return
    
    # Get file names
    kbFiles = os.listdir(kbStorageDir)
    textFiles = os.listdir(script.TEXT_STORAGE_DIR)
    
    # Get entity index into kb tables
    # TODO: KB_ENTITY_INDEX_FILENAME
    
    # Read in all text triples
    textTrainTriples = {}
    textTrainSubjects = {}
    for textFile in textFiles:
        tFilepath = os.path.join(script.TEXT_STORAGE_DIR, textFile)
        testFilepath = os.path.join(TEST_DATA_STORAGE_DIR, textFile)
        
        # Get training triples
        textTriples = set([])
        with open(tFilepath, 'r') as fp1: # Get text triples
            textTriples = set(fp1.readlines())
        with open(testFilepath, 'r') as testFp: # Remove test triples
            textTriples -= set(testFp.readlines())

        textTrainTriples[textFile] = set(textTriples)
        textTrainSubjects[textFile] = set([x.split()[0] for x in textTriples]) # To calculate F1 score
    
    #############################################################################
    #Just people categories for now
    #############################################################################
    #kbFiles = [x for x in kbFiles if x[:7] == 'people.']
    
    # Calculate alignment
    textStats = defaultdict(list)
    for i, kbFile in enumerate(kbFiles):
        stats = []
        kbFilepath = os.path.join(kbStorageDir, kbFile)
        kbTriples = set()
        with open(kbFilepath, 'r') as fp2:
            kbTriples = set(fp2.readlines())
        
        for textFile in textFiles:
            textTriples = textTrainTriples[textFile]
            textSubjects = textTrainSubjects[textFile]
            
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
            f1, p, r = calculateF1(totalGuessed, intersectCount, textSize)
            
            # Add new KbStat to textStats
            textStats[textFile].append(KbStats(kbFile, textFile, source, intersectCount, kbSize, textSize, f1, p, r))
        print str(i+1) + '/' + str(len(kbFiles))
        
    # Sort stats for each text relation by f1 score
    for textFile in textStats.keys():
        textStats[textFile] = sorted(textStats[textFile], key=lambda x: x.alignment['features']['F1'], reverse=True)

    # Store stats to file
    # If no intersection found with any kb table, then no alignment file created for the text relation.
    for textFile in textStats.keys():
        resultsFile = os.path.join(KB_ORDER_STORAGE_DIR+'/'+'alignment'+'_'+source+'_'+kbStorageDir, textFile)
        with open(resultsFile, 'w') as f:
            for stats in textStats[textFile]:
                f.write(str(stats) + '\n')

if __name__ == '__main__':
    #splitTrainTestData()
    computeKbOrdering('kbCombined1and3People', 'Template1234')

