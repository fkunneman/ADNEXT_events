import os
import sys
import argparse
import requests
import datetime
import time
import codecs
import smtplib

"""
Script to collect tweets within a timeframe from twiqs
"""
parser = argparse.ArgumentParser(description = 
    "Script to collect tweets within a timeframe from twiqs")
#parser.add_argument('-k', action = 'store', nargs = '+', required = True, help = "the keywords")
#parser.add_argument('-u', action = 'store', required = True, help = "twiqs username")
#parser.add_argument('-p', action = 'store', required = True, help = "twiqs password") 
#parser.add_argument('-s', action = 'store', required = True, help = 
    #"the start time (format = YYYYMMDDHH)")
#parser.add_argument('-f', action = 'store', required = True, help = 
    #"the end time (format = YYYYMMDDHH)")
#parser.add_argument('-i', action = 'store', required = True, help = "the ip")

## most of these arguments are based on the fact that there is an input file with all events that we want to search for
## If you want to run this per event than it's probably better to change the structure

parser.add_argument('-o', action = 'store', required = True, help = "the directory to write to")
parser.add_argument('-l', action = 'store', type = int, default = 15, help = "the time to wait for query results")
parser.add_argument('-w', action = 'store', type = int, default = 1, help = "the time of repetitive querying")
parser.add_argument('-t', action = 'store', type = int, default = 120, help = "the time to wait in total between requests")
parser.add_argument('-d', action = 'store', required = True, help = "data-file to be processed")
parser.add_argument('-x', action = 'store', required = True, help = "the stopword file for filtering keywords")
parser.add_argument('-f', action = 'store', required = True, help = "The final file in which all events and added tweets are stored")
parser.add_argument('-sf', action = 'store',type=int, required = True, help = "The start of the forloop over the events")
parser.add_argument('-ef', action = 'store',type=int, required = True, help = "The end of the forloop over the events")

args = parser.parse_args()

requestwait = args.w
requestloop = int(args.l/requestwait)
inFile = args.d
events = [line.strip() for line in open(inFile,'r')]
inFileStop = args.x
outfileAll = args.f
stopWords = [line.strip().lower() for line in open(inFileStop,'r')]

totalWait = args.t
startForloop = args.sf
endForloop = args.ef

# Invariable information

pw = [line.strip() for line in open('data/pwd.txt','r')] ### getting the password from pwd.txt, probably not that secure but ok :p
pwd = pw[0].strip()
username = 'rikvannoord@gmail.com'
IP = '145.100.59.169'

#get cookie
s = requests.Session()
r = s.post("http://" + IP + "/cgi-bin/twitter", data={"NAME":username, "PASSWD":pwd})

def request_tweets(t):
    startTime = time.time()
    try:
            output1st = requests.get("http://" + IP + "/cgi-bin/twitter", params=t, cookies=s.cookies)
    except:
            print("Te druk op Twiqs om aan request te voldoen")
            output1st = False
    endTime = time.time()
    timePassed = int(endTime - startTime)
    if timePassed > 120:
        print('Druk op Twiqs, time passed: ' + str(endTime - startTime)) 		##sometimes it's just too busy to get anything
    return output1st, timePassed



def processFoundTweets(output):
	## this is to process the output we earlier dumped with "dumpoutput"
	## this could probably be nicer but since this was your initial script I didn't want to change stuff I didn't fully understand
	## so please check the process_request function
	
	newData = output.split('\n')
	tweets = []
	IDs = []
	dates = []
	for item in newData:
		try:
			tweets.append(item.split('\t')[7])
			IDs.append(item.split('\t')[6])
			dates.append(item.split('\t')[2])
		except:									## reached end of file or something went wrong on twiqs
			pass
	return tweets, IDs, dates	

def process_request(t1,t2,k):
    foundOutput = False
    tweets = 'NA'
    IDs = 'NA'
    dates = 'NA'
    payload = {'SEARCH': k, 'DATE': t1 +'00' + "-" + t2 + '23', 'DOWNLOAD':True, 'SHOWTWEETS':True}
    print("fetching",payload["SEARCH"],"in",payload['DATE'],"from twiqs\n")
    output = False
    
    while not output:
        output, timePassed = request_tweets(payload)
    splitK = k.split(',')
    splitK.sort()
    newK = ",".join(splitK)
    
    dumpoutput = '#user_id\t#tweet_id\t#date\t#time\t#reply_to_tweet_id\t#retweet_to_tweet_id\t#user_name\t#tweet\t#DATE='+payload['DATE']+'\t#SEARCHTOKEN=' + newK + '\n'
    
    if output.text[:1000] == dumpoutput or 'null' not in output.text: #If there isn't any tweet try the request again for x times.
        if 'null' not in output.text and output.text[:1000] != dumpoutput:
            print('\nBugged HTML output again\n')						## this was to catch unwanted output when Twiqs was bugged
        for i in range(0,requestloop):
            print ('Loop number: '+ str(i))
            output = False
            while not output:
                waitTime = totalWait - timePassed
                if waitTime > 0:					#Wait the required amount if there was a positive waitTime
                    time.sleep(waitTime) 			#Wait for the search done at twiqs.nl before the next request
                output, timePassed = request_tweets(payload)				
            if output.text != dumpoutput and 'null' in output.text:		## the right output is found
                foundOutput = True
                break
    else:
         foundOutput = True                
	
    if foundOutput:												## if we found something, process it
        tweets, IDs, dates = processFoundTweets(output.text)
	
    return output.text, tweets, IDs, dates

def mainCollect(window1, window2, keywords):
	## this first if is still in here from Florians file, but isn't used
	
	if keywords == "echtallesXXXXX":
		current = datetime.datetime(int(window1[:4]),int(window1[4:6]),int(window1[6:8]),int(window1[8:]),0,0)
		end = datetime.datetime(int(window2[:4]),int(window2[4:6]),int(window2[6:8]),int(window2[8:]),0,0)
		while current <= end:
			year = str(current.year)
			month = str(current.month)
			day = str(current.day)
			hour = str(current.hour)
			if len(month) == 1:
				month = "0" + month
			if len(day) == 1:
				day = "0" + day
			if len(hour) == 1:
				hour = "0" + hour
			timeobj = year+month+day+hour
			tweets = process_request(timeobj,timeobj,keywords)
			if tweets != "":
				outfile = codecs.open(args.o + timeobj + ".txt","w","utf-8")
				outfile.write(tweets)
				outfile.close()
				current = current + datetime.timedelta(hours = 1)

	else: 	## only this is used
		tweets, tweetsSingle, IDs, dates = process_request(window1,window2,keywords)
		if tweets != "":		## if we found anything
			outfile = codecs.open(args.o + str(keywords) + "-" + window1[:6] + "-" + window2[:6] + ".txt","w","utf-8")
			outfile.write(tweets)
	return tweets, tweetsSingle, IDs, dates	
			
## obtain window and keywords, this is very dependent on initial structure of event and tweets

def getWindow(event):
	## get window in we want to search for new tweets
	## this is based on the format of events you initially gave me
	
	information = event.split('\t')
	eventDate = datetime.datetime.strptime(information[0].strip(),"%Y-%m-%d")
	keywords = information[2].split(',')
	tweets = information[3].split('-----')
	allDates = []
	print(keywords)
	for tweet in tweets:
		print(tweet)
		try:
			date = tweet.split(',')[1]
			newDate = datetime.datetime.strptime(date.strip(),"%Y-%m-%d")
			allDates.append(newDate)
		except:			#sometimes something goes wrong with splitting on '-----', just ignore those tweets then
			pass		
	
	windowLeft = min(allDates)
	diff = abs(eventDate -windowLeft ).days
	maxWindow = 15
	
	if diff > maxWindow:		## 15 is the max number of days we want to search in (both ways, so 30 total)
		diff = maxWindow
	
	windowLeft = eventDate - datetime.timedelta(days=diff)
	windowRight = eventDate + datetime.timedelta(days=diff)
	return [windowLeft, eventDate, windowRight], keywords

def mainLoop():
	## This is the main loop for all events, but can be easily changed for just one line
	## First get the date window in which we want to search for tweets
	## Then obtain all keywords we want to look for
	## Search for those specific tweets and process them
	## Check if everything went well and if yes, save those extra tweets to a predefined file
	
	oldstdout = sys.stdout
	for x in range(startForloop,endForloop):				## start and end are arguments, this is based on a file with all events
		#try:	
		print('\nEvent number:', x)
		window, keywords = getWindow(events[x])			## obtain the date window and the keywords
		newKeywords = []
		
		## filter the keywords (could also mean filtering cities)
		
		for key in keywords:
			key2 = key.strip()
			if key2 not in stopWords and key2.replace(' ','_') not in stopWords and len(key2) > 1:
				newKeywords.append(key2)	
		
		keywordString = ",".join(newKeywords).replace(' ','')	## put them in right format
		diff = int((window[2] - window[0]).days) / 2			## difference between the dates
		window1 = str(window[0]).split()[0].replace('-','')		## formatting
		window2 = str(window[2]).split()[0].replace('-','')
		output, tweets, IDs, dates = mainCollect(window1, window2, keywordString)		## collect output
		noTweets = False
		
		## check if everything went well
		
		if tweets == [] or IDs == [] or dates == []:
			noTweets = True
			print('Something went wrong in the outputfile, but there was output!')
		elif tweets == 'NA' or IDs == 'NA' or dates == 'NA':
			noTweets = True
			print('No output found for this window, probably search not finished at Twiqs')
		else:	
			addTweets = []
			print('Found output!')
			for y in range(1, len(tweets)):		## skip first line
				tweetFormat = IDs[y] + ',' + dates[y] + ',' + tweets[y]  ## add ID, date and tweet, the output contains more information so you could add more
				addTweets.append(tweetFormat)
			finalAdd = '-----' + "-----".join(addTweets) ## "-----" is just for formatting to separate tweets later on
		
		outfileFinal = open(outfileAll,'a')				## save to file in my case, adding to existing file	
		sys.stdout = outfileFinal
		
		if noTweets:
			print(events[x] + '\tNA')					## if no tweets, print what we had with "NA", we can sort that out later
		else:
			print(events[x] + '\t' + finalAdd)			## if we did find tweets, add them
		sys.stdout = oldstdout
		outfileFinal.close()
		#except:
		outfileFinal = open(outfileAll,'a')
		sys.stdout = outfileFinal
		print(events[x] + '\tERROR')
		sys.stdout = oldstdout
		outfileFinal.close()
		print ('Something went wrong for this event in the try-except construction!')  ## this never occurred for me
						
			
mainLoop()				
