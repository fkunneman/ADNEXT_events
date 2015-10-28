import sys,re, numpy
import datetime

inFile = sys.argv[1] ## inputfile with the tweets

def compareLists(list1,list2):
	same = 0
	for item in list1:
		if item not in list2:
			same = 1
			break
	return same		

## rank tweets based on the 4 features. Make sure that they are first sorted just by feature 1, then feature 2, etc. Note the "-" by feature 3, ensuring that the order is different there (ascending instead of descending)

def rankTweets(tweetList):
	
	## this is the function for the actual ranking (basically the next line)
	
	sortedTweetList = sorted(tweetList, key = lambda x: (x[0], x[1],-x[2],x[3]),reverse=True)
	
	## This was just for comparing the lists (to see how often feature 1,2,3 or 4 matters in the ranking)
	
	#sortedTweetList2 = sorted(tweetList, key = lambda x: (x[0], x[1],x[2]),reverse=True)
	#sortedTweetList3 = sorted(tweetList, key = lambda x: (x[0], x[1]),reverse=True)
	#sortedTweetList4 = sorted(tweetList, key = lambda x: (x[0]),reverse=True)
			
	usefulItems = []
	usefulTweets = []

	for counter, item in enumerate(sortedTweetList):
		foundDouble = False
		addItem = item[0:4]										## take the 4 features from addItem (rest is for keeping track)
		for nextCounter, nextItem in enumerate(usefulTweets):
			overlap = len(set(item[5]) & set(nextItem[5])) / max(len(set(item[5])),len(nextItem[5])) # calculate overlap
			if overlap > 0.8:
				foundDouble = True								## too much overlap, ignore tweet
				break
		if not foundDouble and addItem not in usefulItems:		## if not too much overlap and we didn't add it already, add tweet to useful tweets
			usefulItems.append(addItem)
			usefulTweets.append(item)
			
		else:
			usefulTweets.append(item)
												
	finalTweetList = []
	c = 0
	
	## finally add the 7 best tweets and return just those 7, but ofcourse this could be more or less
	
	numTweets = 7
	
	for y in usefulTweets:
		if c < numTweets:
			#print(y[0:4])  ## print this to check if it works
			c+=1
		finalTweetList.append(y[4].strip())
	print('\n')
	return finalTweetList	

def extractTweetInformation(line,tweetList):
	splitLine = line.strip().split('\t')
	dateEvent = datetime.datetime.strptime(splitLine[1].strip(),"%Y-%m-%d")
	keywordsTemp = [x.replace('_',' ').strip() for x in splitLine[3].split(',')] ## get keywords
	
	scores = [x.strip() for x in splitLine[4].split(',')]
	
	keywords = []
	dictKeys = dict()			## create dict to get a score for keywords that don't have an actual score (e.g. score #feyenoord the same as just "feyenoord")
	counter = 0
	
	## add new keywords to the keywords, e.g. add #ajax if only ajax is a keyword, account for spaces (e.g. "ziggo dome" becomes #ziggodome)
	
	for key in keywordsTemp:
		if key not in keywords:
			keywords.append(key)
			dictKeys[key] = float(scores[counter])
		if '#' not in key: 
			if ' ' not in key:
				key2 = '#' + key
			else:
				key2 = '#' + key.replace(' ','')
	
			if key2 not in keywords:
				keywords.append(key2)
				dictKeys[key2] = float(scores[counter])
		
		if '@' not in key and ' ' not in key:
			key3 = '@' + key
			if key3 not in keywords:
				keywords.append(key3)
				dictKeys[key3] = float(scores[counter])	
		counter += 1			
	
	
	if len(splitLine) < 7 or 'oslo' in splitLine[3]:			## delete failed events and Norwegian events. I don't know if you want this in the actual live version :p
		niks = 3
	else:
		newTweets = splitLine[6].split('-----')
		for tweetOld in newTweets:
			tweet = tweetOld.lower()
			if 'http:' in tweet:								## delete the weird broken links in output due to the parser. Ucto automatically splits numbers
				spaceTweet = tweet.split()						## so http://dfd45fd7 becomes http://dfd 45 fd 7 in a tweet. They contain basically no information anyway, 
				foundHTTP = False								## so I deleted them
				fixedTweet = ''
				for part in spaceTweet:
					if foundHTTP:
						if any(char.isdigit() for char in part):
							fixedTweet += part
						else:
							fixedTweet += ' ' + part	
					else:
						fixedTweet += ' ' + part		
							
					if 'http' in part:
						foundHTTP = True
				fixedSplit = fixedTweet.split()
				for part in fixedSplit:
					if 'http:' in part:
						fixedTweet = fixedTweet.replace(part,'')

				tweet = fixedTweet			
			
			## this is to work with the format: user,date,tweet
				
			if ',' in tweet:
				splitTweet = tweet.split(',')
				if len(splitTweet) > 2:
					textTweet = ' ' + ",".join(splitTweet[2:]).strip() + '  '			## get everything after the second comma as a string
					wordsTweet = textTweet.strip().split()
					if splitTweet[1].count('-') == 2:									## only try to get the date if it's formatted as a date (sometimes this goes wrong)
						dateTweet = datetime.datetime.strptime(splitTweet[1].strip(),"%Y-%m-%d")
						absDiffDays = abs((dateTweet - dateEvent).days)
						diffDays = (dateTweet - dateEvent).days
						keywordCount = 0
						scores = 0
						for item in keywords:
							item2 = ' ' + item + ' '
							if item2 in textTweet: 				## check if keyword appears in tweet and if so, add 1 to keywordCount
								keywordCount += 1
								scores += dictKeys[item]			
						if keywordCount > 1 or len(keywordsTemp) == 1:											## I'm only adding tweets that contain 2 keywords or more,
																												## but you could change that in the live version			
							tweetList.append([keywordCount, scores, absDiffDays,diffDays, tweet, wordsTweet])	## add the feature list		
	return tweetList

## loop over file with initial event format + the found extra tweets

for line in open(inFile):
	splitLine = line.split('\t')
	tweetList = (extractTweetInformation(line,[]))
	
	if tweetList:		## check if we found something
		rankedTweetList = rankTweets(tweetList)
		stringRankedTweets = "-----".join(rankedTweetList)
		splitLine[6] = stringRankedTweets	 ## the found tweets are replaced by the ranked tweets
		#print("\t".join(splitLine).strip()) ## just print, but could also be print to file
		


	
