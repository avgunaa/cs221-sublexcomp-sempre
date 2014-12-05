import os, time
#import createRelationTables as script

KB_STORAGE_DIR = 'kbTriplesPeople'
TEXT_STORAGE_DIR = 'textTriples'
XYZ_STORAGE_DIR = 'xyzTriplesPeople'
KB_TRIPLES_DIR = 'kbTriplesPeople/'
TEXT_TRIPLES_DIR = 'textTriplesUnique/'
KB_CONSTANT_TRIPLES_DIR = 'kbConstantTriples/'
CONST_THRESHOLD = 3
KB_SIZE_THRESHOLD = 100
RATIO_THRESHOLD = 0.1


# Exact Match function
# Compares the strings and adds alignment if text phrase is 
# prefix/suffix/exact match of the kb relation
def exactMatch(kb_directory, text_directory):

    kb_files = os.listdir(kb_directory)
    text_files = os.listdir(text_directory)

    f = open('alignment_baseline_' + kb_directory, 'w')

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

def alignment(kb_directory, text_directory, source, kb_size_threshold, ratio_threshold):

    kb_files = os.listdir(kb_directory)
    text_files = os.listdir(text_directory)

    f = open('alignment_' + source + '_' + kb_directory + '_' + str(kb_size_threshold) + '_' + str(ratio_threshold), 'w')
    # for every pair of (kb_file, text_file) we compute the various feature counts
    # if they have atleast one intersection
    for kb_file in kb_files:
        filepath = os.path.join(kb_directory, kb_file)
        fp1 = open(filepath, 'r')
        kb_lines = set(fp1.readlines())
        if len(kb_lines) > kb_size_threshold:
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
            features["TEXT_INTERSECT_RATIO"] = float(intersect_count)/float(len(text_lines))

            alignment = {}
            alignment['formula'] = source + ',' + kb_file
            alignment['source'] = source
            alignment['features'] = features
            alignment['lexeme'] = text_file
            
            if intersect_count > 0 and features["TEXT_INTERSECT_RATIO"] > ratio_threshold:
                f.write(str(alignment) + '\n')
            fp2.close()
        fp1.close()

# @params: kb_files
# @return: a set of constant table file names to be used later in template3()
def findConstantTables(kb_files, threshold):
    const_files = set()

    for kb_file in kb_files:
        fp = open(KB_STORAGE_DIR + '/' + kb_file, 'r')
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
        fp1 = open(KB_STORAGE_DIR + '/' + kb_file, 'r')
        kb_file_category = kb_file.split('.')[0]

        for const_file in const_files:
            if(const_file == kb_file):  # don't intersect a table with itself
                continue

            # only intersect them if they belong to the same category
            const_file_category = const_file.split('.')[0]
            if(const_file_category != kb_file_category):
                continue

            fp2 = open(KB_STORAGE_DIR + '/' + const_file)
            # create a map of the current const table
            const_map = dict()

            for const_line in fp2:
                const_line_args = const_line.split('\t')
                const_map[const_line_args[0]] = const_line_args[len(const_line_args) - 1].split('\n')[0]

            # now check if the 2nd arg of kb_line exists in const_map
            while(True):
                first_spouse_args = fp1.readline().split('\t')
                if(first_spouse_args == ""):    # EOF
                    break
                first_spouse = first_spouse_args[len(first_spouse_args) - 1].split('\n')[0]
                second_spouse_args = fp1.readline().split('\t')
                second_spouse = second_spouse_args[len(second_spouse_args) - 1].split('\n')[0]

                if first_spouse in const_map and second_spouse in const_map:
                    first_spouse_const_prop = const_map[first_spouse]
                    second_spouse_const_prop = const_map[second_spouse]
                    newTableName1 = kb_file + 'AND' + const_file + 'IS' + first_spouse_const_prop
                    f1 = open(KB_CONSTANT_TRIPLES_DIR + '/' + newTableName1, 'a')
                    f1.write(first_spouse + '\t' + second_spouse + '\n')
                    newTableName2 = kb_file + 'AND' + const_file + 'IS' + second_spouse_const_prop
                    f2 = open(KB_CONSTANT_TRIPLES_DIR + '/' + newTableName2, 'a')
                    f2.write(second_spouse + '\t' + first_spouse + '\n')
                    f1.close()
                    f2.close()

                '''
                if kb_line_args[1].split('\n')[0] in const_map:
                    const_property = const_map[kb_line_args[1].split('\n')[0]]
                    newTableName = kb_file + 'AND' + const_file + 'IS' + const_property
                    f = open(KB_CONSTANT_TRIPLES_DIR + '/' + newTableName, 'a')
                    alignment = dict()
                    alignment['kb_arg0'] = kb_line_args[0]
                    alignment['kb_arg1'] = kb_line_args[1].split('\n')[0]
                    alignment['const_property'] = const_property
                    #f.write(str(alignment) + '\n')
                    f.write(kb_line_args[0] + '\t' + kb_line_args[1].split('\n')[0] + '\n')
                    f.close()
                '''

            fp2.close()

        fp1.close()


if __name__ == '__main__':
   
    #exactMatch(KB_STORAGE_DIR, TEXT_STORAGE_DIR)
    #alignment(KB_STORAGE_DIR, TEXT_STORAGE_DIR, 'Template1') 
    #alignment(XYZ_STORAGE_DIR, TEXT_STORAGE_DIR, 'Template4Subset100')
    template3(os.listdir(KB_TRIPLES_DIR), os.listdir(TEXT_TRIPLES_DIR))
 
    #alignment(KB_STORAGE_DIR, TEXT_STORAGE_DIR, 'Template1', 0, 0.1)
    #alignment(XYZ_STORAGE_DIR, TEXT_STORAGE_DIR, 'Template4', KB_SIZE_THRESHOLD, RATIO_THRESHOLD)

