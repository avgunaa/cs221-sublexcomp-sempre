from collections import defaultdict
import os
import shutil

# TODO (Gunaa and Diane): edit your own relative dir paths and 'git push' to easily switch out in the scripts
GINA_DATA_RELATIVE_DIR = '../../Dropbox'
GUNAA_DATA_RELATIVE_DIR = '..'
DIANE_DATA_RELATIVE_DIR = '../data'

# Knowledge base and text triples storage directories
KB_STORAGE_DIR = 'kbTriplesUnique'
TEXT_STORAGE_DIR = 'textTriplesUnique'
XYZ_STORAGE_DIR = 'xyzTriplesUnique'

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
                fp.write("\n".join(triples[key]) + '\n')
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
        fb_triples = defaultdict(set)
        count = 0
        for line in fp:
            linesplit = line.split()
            relation = linesplit[1][3:]  # Remove 'fb:' prefix
            entityOne = linesplit[0]
            entityTwo = linesplit[2][:-1]  # Remove '.' suffix
            fb_triples[relation].add( entityOne + "\t" + entityTwo )
            
            # Prevent running out of memory (MemoryError)
            count += 1
            if count > 100000:
                writeTriplesToFile(fb_triples, KB_STORAGE_DIR)
                fb_triples = defaultdict(set)
                count = 0
        writeTriplesToFile(fb_triples, KB_STORAGE_DIR)

def isATextDate(str):
    return str[:3] != 'fb:'
    
def getTextTriples(filename):
    '''
    text_triples contains dictionary of reln -> list of strings of tab-separated entity pairs
    Example: text_triples['born in'] = ['fb:barrack_obama  fb:honolulu',  'fb:gunaa    fb:chennai']
    '''
    # Set-up table storage directory
    setupStorageDirectory(TEXT_STORAGE_DIR)
    
    text_triples = defaultdict(set)
    with open(filename,"r") as fp:
        for line in fp:
            linesplit = line.split("\t")
            arg1 = linesplit[0]
            reln = linesplit[1]
            arg2 = linesplit[-1].rstrip() # Remove '\n' suffix
            
            # If arg2 is a date...
            if isATextDate(arg2):
                # Store just the year
                arg2 = arg2.split('-')[0]
                '''
                # pick the date with highest granularity
                otherDate = linesplit[-2][5:] # Remove 'TIME:' prefix
                if len(otherDate) > len(arg2):
                    arg2 = otherDate
                '''
            text_triples[reln].add(arg1 + "\t" + arg2)
    writeTriplesToFile(text_triples, TEXT_STORAGE_DIR)

def getXYZRelations(kb_dir):

    kb_files = os.listdir(kb_dir)
    # Set-up table storage directory
    setupStorageDirectory(XYZ_STORAGE_DIR)
 
    count = 1
    for kb_file1 in kb_files:
        file1_dict = defaultdict(set)
        file1_dict.clear()

        with open(kb_dir + '/' + kb_file1, 'r') as fp1:
          for line in fp1:
            linesplit = line.split()
            entityOne = linesplit[0]
            entityTwo = linesplit[1]
            file1_dict[entityOne].add(entityTwo)
        num_lines1 = sum(1 for line in open(kb_dir + '/' + kb_file1))

        for kb_file2 in kb_files:
            print count
            count += 1
            intersection = []
            seen = set()
            entrycount = 0
            num_lines2 = sum(1 for line in open(kb_dir + '/' + kb_file2))
            
            with open(kb_dir + '/' + kb_file2, 'r') as fp2:
              for line in fp2:
               if line not in seen:
                seen.add(line)
                linesplit = line.split()
                entityOne = linesplit[0]
                entityTwo = linesplit[1]
                if entityTwo in file1_dict:
                  for entity in file1_dict[entityTwo]:
                    intersection.append(entityOne + '\t' + entity)
                  #if len(intersection) > 100000:
                  #    f = open(XYZ_STORAGE_DIR + '/' + kb_file2 + '^' + kb_file1, 'a')
                  #    for entry in intersection:
                  #      f.write(entry + '\n')
                  #    intersection = []
                  #    f.close()
                  if len(intersection) > num_lines1 + num_lines2:
                    break

            if len(intersection):
              f = open(XYZ_STORAGE_DIR + '/' + kb_file2 + '^' + kb_file1, 'a')
              for entry in intersection:
                f.write(entry + '\n')
              intersection = []
              f.close()
            fp2.close()
        fp1.close()

if __name__ == '__main__':
    freebase_file = os.path.join(GUNAA_DATA_RELATIVE_DIR, 'data/freebase_subset.ttl')
    textdata_file = os.path.join(GUNAA_DATA_RELATIVE_DIR, 'data/linked-arg2-binary-extractions.txt')
    
    #getFreebaseTriples(freebase_file)
    #getTextTriples(textdata_file)
    
    getXYZRelations(KB_STORAGE_DIR)
