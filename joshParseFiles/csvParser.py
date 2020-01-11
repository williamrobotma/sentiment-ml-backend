import os
import csv
import re

csvFileName = 'banktweets.csv'
def listToText (lis, filename):
    with open(filename + '.txt', 'w+') as lis1:
        for each in lis:
            lis1.write(each)
            lis1.write('\n')


print(os.getcwd())
filepath = os.getcwd() + "\\"
tweetList = []

# configFile = "dataConfig.txt"
# configs = []
# with open(filepath + configFile) as cFile:
#     for c in cFile:
#         entry = c.split('=',1)
#         entry0 = entry[1].replace('\n','')
#         entry[1] = entry0
#         configs.append(entry)
# config = (dict(configs))
#
# dataFile = config['dataFile']


with open(csvFileName) as csv_file:
    csv_reader = csv.reader(csv_file)

    for line in csv_reader:
        print(line[1])
        # print(type(line[1]))
        pureString = re.findall(r"'(.*?)'", line[1])
        # print(pureString)
        tweetList.extend(pureString)

print(tweetList)
listToText(tweetList, 'banktweetsDataList')