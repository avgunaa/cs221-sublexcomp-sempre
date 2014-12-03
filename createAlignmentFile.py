import os, time

KB_STORAGE_DIR = 'kbTriples'
TEXT_STORAGE_DIR = 'textTriples'
XYZ_STORAGE_DIR = 'xyzTriples'

def exactMatch(kb_directory, text_directory):

    kb_files = os.listdir(kb_directory)
    text_files = os.listdir(text_directory)

    f = open('alignment_baseline', 'w')

    for kb_file in kb_files:
        for text_file in text_files:
            if textMatch(kb_file, text_file):
                alignment = {}
                alignment['lexeme'] = text_file
                alignment['formula'] = 'ExactMatch'+ ',' + kb_file
                alignment['features'] = {}
                alignment['source'] = 'ExactMatch'
                f.write(str(alignment) + '\n')

def textMatch(kb_file, text_file):
    kb_file_list = kb_file.split('.')
    text_file_list = text_file.split()
    for word in text_file_list:
        if word not in kb_file_list[-1].split('_'):
            return False
    return True

def alignment(kb_directory, text_directory, source):

    kb_files = os.listdir(kb_directory)
    text_files = os.listdir(text_directory)

    f = open('alignment_' + source, 'w')
    # for every pair of (kb_file, text_file) we compute the various feature counts
    # if they have atleast one intersection
    for kb_file in kb_files:
        filepath = os.path.join(kb_directory, kb_file)
        fp1 = open(filepath, 'r')
        kb_lines = set(fp1.readlines())

        for text_file in text_files:
            intersect_count = 0
            filepath = os.path.join(text_directory, text_file)
            fp2 = open(filepath, 'r')
            text_lines = fp2.readlines()
            for line in text_lines:
                if line in kb_lines:
                    intersect_count += 1

            features = {}
            features["INTERSECTION_SIZE"] = intersect_count
            features["KB_SIZE"] = len(kb_lines)
            features["TEXT_SIZE"] = len(text_lines)

            alignment = {}
            alignment['formula'] = source + ',' + kb_file
            alignment['source'] = source
            alignment['features'] = features
            alignment['lexeme'] = text_file
            
            if intersect_count > 0:
                f.write(str(alignment) + '\n')
            fp2.close()
        fp1.close()


if __name__ == '__main__':
   
    exactMatch(KB_STORAGE_DIR, TEXT_STORAGE_DIR)
    #alignment(KB_STORAGE_DIR, TEXT_STORAGE_DIR, 'Template1') 
    #alignment(XYZ_STORAGE_DIR, TEXT_STORAGE_DIR, 'Template4')
