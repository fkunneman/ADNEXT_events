
import sys

import gen_functions

infile = sys.argv[1]
default_fields = int(sys.argv[2])

with open(infile, 'r', encoding = 'utf-8') as f_in:
    tweets = f_in.readlines()

cleaned_tweets = gen_functions.cleanup_tweets(tweets, default_fields)
with open(infile[:-4] + '_cleaned.txt', 'w', encoding = 'utf-8') as f_out:
    f_out.write(''.join(cleaned_tweets))
