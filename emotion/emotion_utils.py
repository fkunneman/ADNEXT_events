
import numpy

def parse_lcs_classifications(lines, target):
    seen_files = []
    scores = []
    for line in lines:
        try:
            tokens = line.strip().split()
            filename = '/'.join(tokens[0].strip().split('/')[-3:])
            if not filename in seen_files:
                seen_files.append(filename)
                classifications = tokens[1].split()
                classification_target = [x for x in classifications if x.split(":")[0] == target or x.split(":")[0] == '?' + target]
                score = float(classification_target.split(':')[1])
                scores.append(score)
            else:
                continue
        except:
            print('wrong input', line.encode('utf-8'))
    return scores

def calculate_event_emotion_stats(scores):
    size = len(scores)
    if size > 0:
        mean = numpy.mean(scores)
        median = numpy.median(scores)
    else:
        mean = '-'
        median = '-'
    return [size, mean, median]