
import numpy

def parse_lcs_classifications(lines, target):
    file_score = {}
    for line in lines:
        try:
            tokens = line.strip().split()
            filename = '/'.join(tokens[0].strip().split('/')[-3:])
            classifications = tokens[1:]
            classification_target = [x for x in classifications if x.split(":")[0] == target or x.split(":")[0] == '?' + target][0]
            score = [float(classification_target.split(':')[1])]
            classification = classifications[0].split(':')[0]
            if classification == target or classification == '?' + target:
                score.append(target)
            else:
                score.append('other')
            file_score[filename] = score
        except:
            print('wrong input', line.encode('utf-8'))
    return file_score

def calculate_event_emotion_stats(scores, target):
    size = len(scores)
    classifications = [x[1] for x in scores]
    positive_classifications = classifications.count(target)
    if size > 0:
        if positive_classifications > 0:
            percent_emotion = positive_classifications / size
        else:
            percent_emotion = 0.0
        sorted_scores = sorted([x[0] for x in scores])
        mean = numpy.mean(sorted_scores)
        percentile1 = sorted_scores[int((0.5 * size))]
        percentile2 = sorted_scores[int((0.7 * size))]
        percentile3 = sorted_scores[int((0.8 * size))]
        percentile4 = sorted_scores[int((0.9 * size))]
    else:
        percent_emotion, mean, percentile1, percentile2, percentile3, percentile4 = None, None, None, None, None, None

    return [size, percent_emotion, mean, percentile1, percentile2, percentile3, percentile4]

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
