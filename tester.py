import sys, os
from collections import defaultdict
import ast

TEST_TEXT_STORAGE_DIR = 'testData'
sourceToDir = {'Template1':'kbTriplesPeople', 'Template4':'xyzTriplesPeople', 'testing':'kbTriplesPeople'}

def testAlignment(alignment_dir):

    #print alignment
    fail_count = 0
    success_count = 0
    test_files = os.listdir(TEST_TEXT_STORAGE_DIR)
    index = 1

    for test_file in test_files:
        print str(index)+'/'+str(len(test_files))
        index += 1
        filepath = os.path.join(TEST_TEXT_STORAGE_DIR, test_file)
        alignmentpath = os.path.join(alignment_dir, test_file)
        
        # if alignment exists for the text relation
        if os.path.exists(alignmentpath):
          #num_lines = sum(1 for line in open(filepath, 'r'))
          #success_count += num_lines
          
          f_align = open(alignmentpath, 'r')
          alignments = f_align.readlines()

          # Check if each text entry is matched by one of the alignments
          with open(filepath, 'r') as fp_t:
              for line_t in fp_t:
                found_match = False
                for line in alignments:
                    alignment = ast.literal_eval(line)
                    kb_file = alignment['formula']
                    directory = sourceToDir[alignment['source']]
                    kbpath = os.path.join(directory, kb_file)
                    with open(kbpath, 'r') as fp_kb:
                        for line_kb in fp_kb:
                            if line_t == line_kb:
                                found_match = True
                                break
                        if found_match:
                            break
                if found_match:
                    success_count += 1
                else:
                    fail_count += 1

        # no alignment exists for the text relation
        else:
          num_lines = sum(1 for line in open(filepath, 'r'))
          fail_count += num_lines
    print success_count 
    return float(success_count)/float((fail_count + success_count))

if __name__ == '__main__':
    alignment_dir = sys.argv[1]
    result = testAlignment(alignment_dir)
    print result
    
