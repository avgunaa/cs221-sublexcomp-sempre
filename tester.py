import sys, os
from collections import defaultdict
import ast

TEST_TEXT_STORAGE_DIR = 'testData'
sourceToDir = {'Template1':'kbTriplesPeople', 'Template4':'template4dir', 'testing':'kbTriplesPeople'}

def testAlignment(alignment_file):
    alignment = {}
    with open(alignment_file, 'r') as fp:
      for line in fp:
        a = ast.literal_eval(line)
       # if a['lexeme'] in alignment:
       #   if alignment[a['lexeme']]['features']['TEXT_INTERSECT_RATIO'] < a['features']['TEXT_INTERSECT_RATIO']:
       #     alignment[a['lexeme']] = a
       # else:
        alignment[a['lexeme']] = a

    #print alignment
    fail_count = 0
    success_count = 0
    test_files = os.listdir(TEST_TEXT_STORAGE_DIR)
    for test_file in test_files:
        filepath = os.path.join(TEST_TEXT_STORAGE_DIR, test_file)
        # if alignment exists for the text relation
        if test_file in alignment:
          num_lines = sum(1 for line in open(filepath, 'r'))
          success_count += num_lines
          #with open(filepath, 'r') as fp_t:
          #  match = alignment[test_file]
          #  for line in fp_t:
          #    linesplit = line.split()
          #    entityOne = line[0]
          #    entityTwo = line[1]
          #    # check if entityTwo is the answer for any relation in the alignment
          #    found_match = False
          #    kb_file = match['formula']
          #    directory = sourceToDir[match['source']]
          #    kbpath = os.path.join(directory, kb_file)
          #    with open(filepath, 'r') as fp_kb:
          #      for line2 in fp_kb:
          #        if line == line2:
          #          found_match = True
          #          break
          #    if found_match:
          #        break
          #    if found_match:
          #        success_count += 1
          #    else:
          #        fail_count += 1

        # no alignment exists for the text relation
        else:
          num_lines = sum(1 for line in open(filepath, 'r'))
          fail_count += num_lines
    print success_count 
    return float(success_count)/float((fail_count + success_count))

if __name__ == '__main__':
    alignment_file = sys.argv[1]
    result = testAlignment(alignment_file)
    print result
    
