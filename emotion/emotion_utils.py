
import numpy

def parse_lcs_classifications(lines, target):
    file_score = {}
    for line in lines:
        try:
            tokens = line.strip().split()
            filename = '/'.join(tokens[0].strip().split('/')[-3:])
            classifications = tokens[1:]
            classification_target = [x for x in classifications if x.split(":")[0] == target or x.split(":")[0] == '?' + target][0]
            score = float(classification_target.split(':')[1])
            file_score[filename] = score
        except:
            print('wrong input', line.encode('utf-8'))
    return file_score

def calculate_event_emotion_stats(scores):
    size = len(scores)
    #mean = numpy.mean(scores)
    #median = numpy.median(scores)
#    print(size, scores)
#    print(int((0.9 * size)))
    sorted_scores = sorted(scores)
    percentile1 = sorted_scores[int((0.5 * size))]
    percentile2 = sorted_scores[int((0.7 * size))]
    percentile3 = sorted_scores[int((0.8 * size))]
    percentile4 = sorted_scores[int((0.9 * size))]
    return [size, percentile1, percentile2, percentile3, percentile4]

def filename2tweetindex(filename):
    parts = filename.split('/')
    filedir = int(parts[1].split('_')[1])
    start_index = 25000 * filedir
    f = parts[2][:-4]
    while f[0] == '0':
        if len(f) == 1:
            break
        else:
            f = f[1:]
    return start_index + int(f)
