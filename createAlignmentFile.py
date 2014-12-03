import os, time

KB_STORAGE_DIR = 'kbTriples'
TEXT_STORAGE_DIR = 'textTriples'
XYZ_STORAGE_DIR = 'xyzTriples'
KB_TRIPLES_DIR = 'kbTriples/'
TEXT_TRIPLES_DIR = 'textTriples/'
KB_CONSTANT_TRIPLES_DIR = 'kbConstantTriples/'
CONST_THRESHOLD = 3

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
    kb_file_list = kb_file.split('.')[-1].split('_')
    text_file_list = text_file.split()
    if text_file_list == kb_file_list[0:len(text_file_list)] or text_file_list == kb_file_list[len(kb_file_list) - len(text_file_list):]:
        return True
    return False
    #for word in text_file_list:
    #    if word not in kb_file_list[-1].split('_'):
    #        return False
    #return True

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

# @params: kb_files
# @return: a set of constant table file names to be used later in template3()
def findConstantTables(kb_files, threshold):
    const_files = set()

    for kb_file in kb_files:
        fp = open(KB_TRIPLES_DIR + kb_file, 'r')
        argSet = set()

        for line in fp:
            # two arguments each line are separated by a tab
            args = line.split('\t')
            const = args[len(args) - 1].split('\n')[0]
            argSet.add(const)
        
	# if the number of properties is not larger than a threshold, mark this as a const table
        if(len(argSet) <= threshold):
            const_files.add(kb_file)

        fp.close()
    
    return const_files


def template3(kb_files, text_files):
    # TODO
    # Aligns patterns of the form
    #   X -> Y
    #   |
    #   v
    #   C

    # find constant tables
    const_files = findConstantTables(kb_files, CONST_THRESHOLD)
    
    # create a dir to put results
    if not os.path.exists(KB_CONSTANT_TRIPLES_DIR):
        os.makedirs(KB_CONSTANT_TRIPLES_DIR)

    # intersect all kbtables with const tables and create new tables
    for kb_file in kb_files:
        fp1 = open(KB_TRIPLES_DIR + kb_file, 'r')

        for const_file in const_files:
            if(const_file == kb_file):  # don't intersect a table with itself
                continue

            fp2 = open(KB_TRIPLES_DIR + const_file)
            # create a map of the current const table
            const_map = dict()

            for const_line in fp2:
                const_line_args = const_line.split('\t')
                const_map[const_line_args[0]] = const_line_args[len(const_line_args) - 1].split('\n')[0]

            # now check if the 2nd arg of kb_line exists in const_map
            for kb_line in fp1:
                kb_line_args = kb_line.split('\t')

                if kb_line_args[1].split('\n')[0] in const_map:
                    const_property = const_map[kb_line_args[1].split('\n')[0]]
                    newTableName = kb_file + 'AND' + const_file + 'IS' + const_property
                    f = open(KB_CONSTANT_TRIPLES_DIR + '/' + newTableName, 'a')
                    alignment = dict()
                    alignment['kb_arg0'] = kb_line_args[0]
                    alignment['kb_arg1'] = kb_line_args[1]
                    alignment['const_property'] = const_property
                    f.write(str(alignment) + '\n')
                    f.close()

            fp2.close()

        fp1.close()


if __name__ == '__main__':
   
    exactMatch(KB_STORAGE_DIR, TEXT_STORAGE_DIR)
    #alignment(KB_STORAGE_DIR, TEXT_STORAGE_DIR, 'Template1') 
    #alignment(XYZ_STORAGE_DIR, TEXT_STORAGE_DIR, 'Template4')
