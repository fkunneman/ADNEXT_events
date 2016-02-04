
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
    mean = numpy.mean(scores)
    median = numpy.median(scores)
#    print(size, scores)
#    print(int((0.9 * size)))
    sorted_scores = sorted(scores)
    percentile = sorted_scores[int((0.9 * size))]
    return [size, mean, median, percentile]

def filename2tweetindex(filename):
    parts = filename.split('/')
    filedir = int(parts[1].split('_')[1])
    start_index = 25000 * filedir
    f = parts[2][:-4]
    print(parts, f)
    while f[0] == '0':
        if len(f) == 1:
            break
        else:
            f = f[1:]
    return start_index + int(f)
