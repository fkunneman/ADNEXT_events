
import os
import sys

import docreader
import emotion_utils

classification_dir_before = sys.argv[1]
target_before = sys.argv[2]
classification_dir_after1 = sys.argv[3]
target_after1 = sys.argv[4]
classification_dir_after2 = sys.argv[5]
target_after2 = sys.argv[6]
event_info_dir = sys.argv[7]
event_dir_before = sys.argv[8]
event_dir_after = sys.argv[9]
outdir = sys.argv[10]

print('collecting files')
classification_files_before = os.listdir(classification_dir_before)
classification_files_after1 = os.listdir(classification_dir_after1)
classification_files_after2 = os.listdir(classification_dir_after2)
# eventfiles = os.listdir(event_info_dir)
# before_tweets = os.listdir(event_dir_before)
# after_tweets = os.listdir(event_dir_after)

print('collecting event data before')
for event in classification_files_before:
    event_id = event[:-4]
    print(event_id)
    new_tweets = []
    with open(classification_dir_before + event) as classifications_in:
        lines = classifications_in.readlines()
        file_score = emotion_utils.parse_lcs_classifications(lines, target_before)
    files = sorted(file_score.keys())
    doc_tweets = event_dir_before + 'tweets_' + event_id + '.csv'
    dr = docreader.Docreader()
    dr.parse_doc(doc_tweets)
    for f in files:
        index = emotion_utils.filename2tweetindex(f)
        tweet = dr.lines[index]
        new_tweets.append([float(file_score[f]), tweet[0], tweet[2], tweet[3], tweet[4], tweet[5]])
    new_tweets_sorted = sorted(new_tweets, key = lambda k : k[0], reverse = True)
    new_tweets_sorted = [[str(y) for y in x] for x in new_tweets_sorted]
    eventfile = event_info_dir + 'sequence_' + event_id + '.txt'
    with open(eventfile, 'r', encoding = 'utf-8') as event_in:
        tokens = event_in.readlines()[0].split('\t')
        event_terms = tokens[0] 
        event_date = tokens[1]
        with open(outdir + event_id + '_' + target_before + '.txt', 'w', encoding = 'utf-8') as sout:
            sout.write(event_terms + '\t' + event_date + '\n')
            sout.write('\n'.join(['\t'.join(x) for x in new_tweets_sorted]))

print('collecting event data after')
for event in classification_files_after1:
    event_id = event[:-4]
    print(event_id)
    new_tweets = []
    with open(classification_dir_after1 + event) as classifications_in:
        lines = classifications_in.readlines()
        file_score = emotion_utils.parse_lcs_classifications(lines, target_after1)
    files = sorted(file_score.keys())
    doc_tweets = event_dir_after + 'tweets_' + event_id + '.csv'
    dr = docreader.Docreader()
    dr.parse_doc(doc_tweets)
    for f in files:
        index = emotion_utils.filename2tweetindex(f)
        tweet = dr.lines[index]
        new_tweets.append([float(file_score[f]), tweet[0], tweet[2], tweet[3], tweet[4], tweet[5]])
    new_tweets_sorted = sorted(new_tweets, key = lambda k : k[0], reverse = True)
    new_tweets_sorted = [[str(y) for y in x] for x in new_tweets_sorted]
    eventfile = event_info_dir + 'sequence_' + event_id + '.txt'
    with open(eventfile, 'r', encoding = 'utf-8') as event_in:
        tokens = event_in.readlines()[0].split('\t')
        event_terms = tokens[0]
        event_date = tokens[1]
        with open(outdir + event_id + '_' + target_after1 + '.txt', 'w', encoding = 'utf-8') as sout:
            sout.write(event_terms + '\t' + event_date + '\n')
            sout.write('\n'.join(['\t'.join(x) for x in new_tweets_sorted]))

for event in classification_files_after2:
    event_id = event[:-4]
    print(event_id)
    new_tweets = []
    with open(classification_dir_after2 + event) as classifications_in:
        lines = classifications_in.readlines()
        file_score = emotion_utils.parse_lcs_classifications(lines, target_after2)
    files = sorted(file_score.keys())
    doc_tweets = event_dir_after + 'tweets_' + event_id + '.csv'
    dr = docreader.Docreader()
    dr.parse_doc(doc_tweets)
    for f in files:
        index = emotion_utils.filename2tweetindex(f)
        tweet = dr.lines[index]
        new_tweets.append([float(file_score[f]), tweet[0], tweet[2], tweet[3], tweet[4], tweet[5]])
    new_tweets_sorted = sorted(new_tweets, key = lambda k : k[0], reverse = True)
    new_tweets_sorted = [[str(y) for y in x] for x in new_tweets_sorted]
    eventfile = event_info_dir + 'sequence_' + event_id + '.txt'
    with open(eventfile, 'r', encoding = 'utf-8') as event_in:
        tokens = event_in.readlines()[0].split('\t')
        event_terms = tokens[0] 
        event_date = tokens[1]
        with open(outdir + event_id + '_' + target_after2 + '.txt', 'w', encoding = 'utf-8') as sout:
            sout.write(event_terms + '\t' + event_date + '\n')
            sout.write('\n'.join(['\t'.join(x) for x in new_tweets_sorted]))

