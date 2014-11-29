from collections import defaultdict
import os
import shutil

# TODO (Gunaa and Diane): edit your own relative dir paths and 'git push' to easily switch out in the scripts
GINA_DATA_RELATIVE_DIR = '../../Dropbox'
GUNAA_DATA_RELATIVE_DIR = ''
DIANE_DATA_RELATIVE_DIR = '../data'

# Knowledge base and text triples storage directories
KB_STORAGE_DIR = 'kbTriples'
TEXT_STORAGE_DIR = 'textTriples'

# Text triples storage file name quirks
INVALID_NAMES = {'' : 'null', 'con' : 'notCon'}
WEIRD_SYMBOLS = {'\\': '(bslash)', '/': '(fslash)', '*': '(star)', ':': '(semicolon)'}

def getRelationFilename(key):
    '''
    Replace invalid names/characters for file names
    '''
    filename = key
    if filename in INVALID_NAMES.keys():
        filename = INVALID_NAMES[filename]
    for symbol in WEIRD_SYMBOLS.keys():
        filename = filename.replace(symbol, WEIRD_SYMBOLS[symbol])
    return filename

def writeTriplesToFile(triples, directory):
    for key in triples.keys():
        filename = getRelationFilename(key)
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, 'a+') as fp:
                fp.write("\n".join(triples[key]))   
        except IOError:
            print key

def setupStorageDirectory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)
    
def getFreebaseTriples(filename):
    '''
    fb_triples contains dictionary of reln -> list of strings of tab-separated entity pairs
    Example: fb_triples[POB] = ['fb:barrack_obama fb:honolulu', 'fb:gunaa fb:chennai']
    '''
    # Set-up table storage directory
    setupStorageDirectory(KB_STORAGE_DIR)
        
    with open(filename,"r") as fp:
        fb_triples = defaultdict(list)
        count = 0
        for line in fp:
            linesplit = line.split()
            relation = linesplit[1][3:]  # Remove 'fb:' prefix
            entityOne = linesplit[0]
            entityTwo = linesplit[2][:-1]  # Remove '.' suffix
            fb_triples[relation].append( entityOne + "\t" + entityTwo )
            
            # Prevent running out of memory (MemoryError)
            count += 1
            if count > 100000:
                writeTriplesToFile(fb_triples, KB_STORAGE_DIR)
                fb_triples = defaultdict(list)
                count = 0
        writeTriplesToFile(fb_triples, KB_STORAGE_DIR)

'''
def string_contains(string, sub):
    lstring = string.lower()
    lsub = sub.lower()
    return True if lsub in lstring else False

def get_better_relation(linesplit, arg2):
    better_reln = ""
    for i in range(len(linesplit)-1, -1, -1):
        if string_contains(arg2, linesplit[i]):
            better_reln = linesplit[i] + better_reln
        else:
            break
    return ' '.join(linesplit[0:i+1])
'''

def isATextDate(str):
    return str[:3] != 'fb:'
    
def getTextTriples(filename):
    '''
    text_triples contains dictionary of reln -> list of strings of tab-separated entity pairs
    Example: text_triples['born in'] = ['fb:barrack_obama  fb:honolulu',  'fb:gunaa    fb:chennai']
    '''
    # Set-up table storage directory
    setupStorageDirectory(TEXT_STORAGE_DIR)
    
    text_triples = defaultdict(list)
    with open(filename,"r") as fp:
        for line in fp:
            linesplit = line.split("\t")
            arg1 = linesplit[0]
            reln = linesplit[1]
            arg2 = linesplit[-1].rstrip() # Remove '\n' suffix

            '''
            better_reln = get_better_relation(linesplit[1:-1], arg2)
            if len(better_reln) <= len(reln) and better_reln != "":
                reln = better_reln
            '''
            
            # If arg2 is a date, pick the date with highest granularity
            if isATextDate(arg2):
                otherDate = linesplit[-2][5:] # Remove 'TIME:' prefix
                if len(otherDate) > len(arg2):
                    arg2 = otherDate
            
            text_triples[reln].append(arg1 + "\t" + arg2)
    writeTriplesToFile(text_triples, TEXT_STORAGE_DIR)

if __name__ == '__main__':
    freebase_file = os.path.join(GINA_DATA_RELATIVE_DIR, 'data/freebase_subset.ttl')
    textdata_file = os.path.join(GINA_DATA_RELATIVE_DIR, 'data/linked-arg2-binary-extractions.txt')
     
    #getFreebaseTriples(freebase_file)
    getTextTriples(textdata_file)
    
