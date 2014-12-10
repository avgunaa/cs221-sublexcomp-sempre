import sys, os
from collections import defaultdict
import ast

TEST_TEXT_STORAGE_DIR = 'testData'
sourceToDir = {'Template1':'kbTriples', 'Template4':'xyzTriples', 'testing':'kbTriplesPeople', 'Combined1and4':'kbCombined', 'Template1234':'kbCombined1and3People'}

def testAlignment(alignment_dir, test):

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
            num_lines = sum(1 for line in open(filepath, 'r'))
            f_align = open(alignmentpath, 'r')
            alignments = f_align.readlines()
            if test == 'test1':
                # Add 1 to success count
                success_count += num_lines

            elif test == 'test2':
                # Add max F1 score to success count
                alignment = ast.literal_eval(alignments[0])
                F1_score = float(alignment['features']['F1'])
                success_count += num_lines * F1_score
            
            elif test == 'test3':
                # Add max F1 score / sum(F1 scores) to success count
                f_align = open(alignmentpath, 'r')
                alignments = f_align.readlines()
                F1_scores = []
                for line in alignments:
                    alignment = ast.literal_eval(line)
                    F1_scores.append(float(alignment['features']['F1']))
                success_count += num_lines * F1_scores[0]/(sum(F1_scores))
            
            else:
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
    testCode = sys.argv[2]
    result = testAlignment(alignment_dir, testCode)
    print result
    
