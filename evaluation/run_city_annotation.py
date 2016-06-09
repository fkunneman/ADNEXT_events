
import sys,re, random,time

eventfile = sys.argv[1]
outfile = sys.argv[2]
index = int(sys.argv[3])

out_w = open(outfile, 'a', encoding = 'utf-8')

print('\nUSER INFORMATION:\n\nDit is het programma voor het annoteren van de locatie van events. Succes!\n\n')

with open(eventfile, encoding = 'utf-8') as ef:
    out = []
    lines = ef.readlines()
    while index < len(lines):
        line = lines[index]
        tokens = line.strip().split('\t')
        date = tokens[0]
        terms = tokens[1]
        locs = tokens[2].split('|')
        loc = locs[0].split(' / ')[0]
        tweets = tokens[3].split('-----')
        print('EVENT', index, '\n')
        print('Datum:\t\t', date),
        print('Keywords:\t', terms.encode('utf-8'), '\n')
        print('ORIGINAL TWEETS FOR EVENT:\n')
        for tweet in tweets[:10]:
            print(tweet.encode('utf-8'))
        time.sleep(0.25)
        print('\nMOGELIJKE LOCATIE:\n',loc)
        useful = 'NA'
        print('geef j / n / [andere locatie] \n')
        inputUser = input()
        if inputUser == 'j':
            tokens.append('C')
        elif inputUser == 'n':
            tokens.append('N')
        else:
            tokens.append(inputUser)
        print('Weet je het zeker? (j/n/v)')
        ipu = input()
        if ipu == 'j':
            out_w.write('\t'.join([str(index)] + tokens) + '\n')
            index += 1
        elif ipu == 'v':
            index -= 1
