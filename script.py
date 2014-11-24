from collections import defaultdict
import os
import shutil

# TODO (Gunaa and Diane): edit your own relative dir paths and 'git push' to easily switch out in the main function
GINA_DATA_RELATIVE_DIR = '../../Dropbox'
GUNAA_DATA_RELATIVE_DIR = ''
DIANE_DATA_RELATIVE_DIR = ''

# Knowledge base and text triples storage directories
KB_STORAGE_DIR = 'kbTriples'
TEXT_STORAGE_DIR = 'textTriples'

# Text triples storage file name quirks
INVALID_NAMES = {'' : 'null', 'con' : 'notCon'}
WEIRD_SYMBOLS = {'\\': '(bslash)', '/': '(fslash)', '*': '(star)', ':': '(semicolon)'}

def writeTriplesToFile(triples, directory):
    for key in triples.keys():
        # Replace invalid names/characters for file names
        name = key
        if name in INVALID_NAMES.keys():
            name = INVALID_NAMES[name]
        for symbol in WEIRD_SYMBOLS.keys():
            name = name.replace(symbol, WEIRD_SYMBOLS[symbol])
            
        table_filename = os.path.join(directory, name)
        try:
            with open(table_filename, 'a+') as fp:
                fp.write("\n".join(triples[key]))   
        except IOError:
            print key
            
def getFreebaseTriples(filename):
    '''
    fb_triples contains dictionary of reln -> list of strings of tab-separated entity pairs
    Example: fb_triples[POB] = ['fb:barrack_obama fb:honolulu', 'fb:gunaa fb:chennai']
    '''
    # Set-up table storage directory
    if os.path.exists(KB_STORAGE_DIR):
        shutil.rmtree(KB_STORAGE_DIR)
    os.makedirs(KB_STORAGE_DIR)
        
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

def getTextTriples(filename):
    '''
    text_triples contains dictionary of reln -> list of strings of tab-separated entity pairs
    Example: text_triples['born in'] = ['fb:barrack_obama  fb:honolulu',  'fb:gunaa    fb:chennai']
    '''
    # Set-up table storage directory
    if os.path.exists(TEXT_STORAGE_DIR):
        shutil.rmtree(TEXT_STORAGE_DIR)
    os.makedirs(TEXT_STORAGE_DIR)
    
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
            text_triples[reln].append(arg1 + "\t" + arg2)
    writeTriplesToFile(text_triples, TEXT_STORAGE_DIR)

if __name__ == '__main__':
    freebase_file = os.path.join(GINA_DATA_RELATIVE_DIR, 'data/freebase_subset.ttl')
    textdata_file = os.path.join(GINA_DATA_RELATIVE_DIR, 'data/linked-arg2-binary-extractions.txt')
     
    getFreebaseTriples(freebase_file)
    getTextTriples(textdata_file)
    