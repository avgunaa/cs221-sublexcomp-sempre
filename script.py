from collections import defaultdict

def getFreebaseTriples(filename):
    fb_triples = defaultdict(list)
    with open(filename,"r") as fp:
        for line in fp:
            linesplit = line.split()
            fb_triples[linesplit[1]].append((linesplit[0],linesplit[2]))
    return fb_triples

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
    text_triples = defaultdict(list)
    with open(filename,"r") as fp:
        for line in fp:
            linesplit = line.split()
            arg1 = linesplit[0]
            arg2 = linesplit[-1]
            reln = ' '.join(linesplit[1:len(linesplit)-2])
            better_reln = get_better_relation(linesplit[1:-1], arg2)
            if len(better_reln) <= len(reln) and better_reln != "":
                reln = better_reln
            text_triples[reln].append((arg1, arg2))
    return text_triples

if __name__ == '__main__':
    freebase_file = '../data/freebase_subset.ttl'
    textdata_file = '../data/linked-arg2-binary-extractions.txt'
    # fb_data contains dictionary of reln -> list of entity pairs (for example, fb_data[fb:POB] = [('fb:barrack_obama, fb:honolulu'), (fb:gunaa, fb:chennai)])
    # similar format for text_data (for example, text_data['born in'] = [('fb:barrack_obama, fb:honolulu'), (fb:gunaa, fb:chennai)])

    fb_data = getFreebaseTriples(freebase_file)
    text_data = getTextTriples(textdata_file)
    print len(fb_data)
    print len(text_data)
