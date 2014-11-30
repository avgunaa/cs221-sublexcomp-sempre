import os, time

KB_TRIPLES_DIR = 'kbTriples/'
TEXT_TRIPLES_DIR = 'textTriples/'

# finds the current time in milliseconds
current_milli_time = int(round(time.time() * 1000))

def template1(kb_files, text_files):
    # Aligns patterns of the form
    #   X -> Y

    f = open('alignment', 'w')
    # for every pair of (kb_file, text_file) we compute the various feature counts
    # if they have atleast one intersection
    for kb_file in kb_files:
        fp1 = open(KB_TRIPLES_DIR + kb_file, 'r')
        kb_lines = set(fp1.readlines())
        for text_file in text_files:
            intersect_count = 0
            fp2 = open(TEXT_TRIPLES_DIR + text_file, 'r')
            text_lines = fp2.readlines()
            for line in text_lines:
                if line in kb_lines:
                    intersect_count += 1
            features = {}
            features["INTERSECTION_SIZE"] = intersect_count
            features["KB_SIZE"] = len(kb_lines)
            features["TEXT_SIZE"] = len(text_lines)
            alignment = {}
            alignment['formula'] = kb_file
            alignment['source'] = 'Template1'
            alignment['features'] = features
            alignment['lexeme'] = text_file
            if intersect_count > 0:
                f.write(str(alignment) + '\n')
            fp2.close()
        fp1.close()

def template2(kb_files, text_files):
    # TODO
    # Aligns patterns of the form
    #   X -> M -> Z

def template3(kb_files, text_files):
    # TODO
    # Aligns patterns of the form
    #   X -> Y
    #   |
    #   v
    #   C

if __name__ == '__main__':
    
    kb_files = os.listdir(KB_TRIPLES_DIR)
    text_files = os.listdir(TEXT_TRIPLES_DIR)
    print len(kb_files), len(text_files)
    
    template1(kb_files, text_files) 

