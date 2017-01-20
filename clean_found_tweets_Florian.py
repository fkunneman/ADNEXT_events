#!/usr/bin/env python3

## File for cleaning the found tweets from twiqs (basically ucto parsing en removing retweets)

import ucto,sys, datetime

inFile = sys.argv[1]

#Set a file to use as tokeniser rules, this one is for English, other languages are available too:
settingsfile = "/vol/customopt/uvt-ru.obsolete/etc/ucto/tokconfig-nl"	## this should probably be changed since it says obsolete now...

tokenizer = ucto.Tokenizer(settingsfile)

output = [0,0]

allTweetsCount = 0
count = 0

## again looping over a file, but can be changed for just 1 event

for line in open(inFile,'r'):
	lineSplit = line.strip().split('\t')
	tweetSplit = lineSplit[5]
	oldTweetsTemp = lineSplit[4]					## the oldtweets are in the same file for me, but that isn't necessarily the case
	oldTweets = [x.strip() for x in oldTweetsTemp]
	if '-----'  not in tweetSplit:					## check if there is output found for this event (this works due to the earlier formatting in collect_tweets_integrated.py)
		output[0] += 1
		continue									## no output from Twiqs for this event
	else:	
		output[1] += 1
		foundTweetsTemp = tweetSplit.split('-----')	## split for tweets
		foundTweets = list(set(foundTweetsTemp))	## ignore double tweets	
		# allTweetsCount += len(foundTweets)		## counting all found tweets 	
		keepTweets = []
		for tweet2 in foundTweets:
			try:
				tweet = tweet2.strip()
				if tweet in oldTweets or not tweet:			# remove tweets already found, empty tweets and retweets
					continue
				else:
					splitTweet = tweet.split(',')
					textTweet = ",".join(splitTweet[2:])	## only get the text and not user and date	
					if textTweet[0:3] == 'RT ':				## Deleting retweets! Very important. They could be removed earlier in the process also.
						continue
					dateTweet = datetime.datetime.strptime(splitTweet[1].strip(),"%Y-%m-%d")
					dateTweetString = splitTweet[1].strip()
					user = splitTweet[0].strip()
					
					tokenizer.process(textTweet)
					tokenList = []
					tempString = ''
					
					## Ucto just splits all specials character by spaces. This is tricky, since we want sentences to end with the character (. ! ?) directly
					## behind the previous word, but we for hashtags/ @'s and left parentheses we want the space first. Sometimes it messes up a smiley but usually 
					## this approach works well.
					
					for token in tokenizer:
						newToken = str(token)
						if len(newToken) == 1:
							if newToken.isdigit() or newToken.isalpha():
								tempString += ' ' + str(token)
							else:
								tempString += str(token)	
						else:
							tempString += ' ' + str(token)
					
					## the tokenizer splits hashtags (and @'s), so we change them back
					
					newString = tempString.strip().replace('# ',' #').replace('@ ',' @').replace('( ',' (')
					parsedTweet = " ".join(newString.split())	## ignore double spaces	
					fullTweet = user + ',' + dateTweetString + ',' + parsedTweet
					keepTweets.append(fullTweet)				## add the fullTweet to the list
			except:
				pass	
		
		stringTweet = "-----".join(keepTweets)					## this is just for formatting reasons
		
		## here I just printed the final output and redirected the output in the terminal
		## it prints the original event number first so we keep things clear, then the original information from the event and then the new events (that are kept)
		
		print((str(output[0] + output[1])) + '\t' + lineSplit[0] + '\t' + lineSplit[1] + '\t' + lineSplit[2] + '\t' + lineSplit[3] + '\t' +lineSplit[4] + '\t'	+ stringTweet)

#print('Aantal goeie events:', output[1],'\n', 'Aantal gefaalde events:', output[0])			
