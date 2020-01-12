from google_play_scraper import app
from pprint import pprint

def listToText (lis, filename):
    with open(filename + '.txt', 'w+', encoding="utf-8") as lis1:
        for each in lis:
            lis1.write(each)
            lis1.write('\n')

def getGoogleReview(appid):
    result = app(
        appid,
        lang='en', # defaults to 'en'
        country='us' # defaults to 'us'
    )
    return result

def getComments(result, lis):

    for field in result['comments']:
        print(field)
        # print(type(field))
        lis.append(field)
        print('\n')




appList = ['com.rbc.mobile.android', 'com.rbcinsurance.groupbenefits.mybenefitsapp','com.rbc.mobile.wallet','com.rbc.clientmobility.us.cas.prod', 'com.rbcc.mobile.android', 'com.rbc.mobile.uin0', 'com.rbc.mobile.rjj0'] #rbc
appList2 = ['com.td', 'com.td.myspend', 'com.td.myloyalty', 'com.tdbank', 'com.td.android', 'com.td.insurance', 'com.devexperts.tdmobile.platform.android.ameritrade', 'com.td.tdwheels'] #td
appList3 = ['com.scotiabank.scotiaconnect', 'com.scotiabank.banking', 'com.scotiabank.scotiaitrade.itrade'] #scotia
appList4 = ['com.bmo.mobile', 'com.bmo.investorline', 'com.bmo.business.mobile', 'com.bmoharris.netxinvestor', 'com.bmomarkets.mobile'] #bmo
testList = []
bankingListRBC = []
insuranceListRBC = []
investmentListRBC = []
bankingListMaster = []
insuranceListMaster = []
investmentListMaster = []

# bankingList = [appList[0], appList[2], appList[4], appList[5], appList[6]]
# insuranceList = [appList[1]]
# investmentList = [appList[3]]

# pprint(result1)
# for each in result:
#     print(each)

#these are
result1 = getGoogleReview(appList[0])
result2 = getGoogleReview(appList[1])
result3 = getGoogleReview(appList[2])
result4 = getGoogleReview(appList[3]) #not using this one because only two comments
result5 = getGoogleReview(appList[4])
result6 = getGoogleReview(appList[5])
result7 = getGoogleReview(appList[6])

resultsList = [result1, result2, result3, result5, result6, result7]

bankingAppsRBC = [result1, result3, result5, result6, result7]
insuranceAppsRBC = [result2]
investmentAppsRBC = [result4]

bankingAppsMaster = [getGoogleReview(appList2[0]), getGoogleReview(appList2[1]), getGoogleReview(appList2[2]), getGoogleReview(appList2[3]), getGoogleReview(appList2[4]), getGoogleReview(appList2[7]), getGoogleReview(appList3[0]), getGoogleReview(appList3[1]), getGoogleReview(appList4[0]), getGoogleReview(appList4[2])]
insuranceAppsMaster = [getGoogleReview(appList2[5])]
investmentAppsMaster = [getGoogleReview(appList2[6]), getGoogleReview(appList3[2]), getGoogleReview(appList4[1]), getGoogleReview(appList4[3]), getGoogleReview(appList4[4])]






# pprint(result2)

        # print(type(result['comments']))

    # print(len(result['comments']))
    # print('\n')

# getComments(result1, testList)
# print(len(testList))
# pprint(testList)
# getComments(result2)
# getComments(result3)
# getComments(result4)
# getComments(result5)
# getComments(result6)
# getComments(result7)

def organizeComments(organizedApps, organizedList, outFileName):
    for each in organizedApps:
        getComments(each, organizedList)
    print(len(organizedList))
    listToText(organizedList, outFileName)

organizeComments(resultsList, testList, 'RBC_aggregate_googleplaydata')

organizeComments(bankingAppsRBC, bankingListRBC, 'RBC_banking_googleplaydata')

organizeComments(investmentAppsRBC, investmentListRBC, 'RBC_investment_googleplaydata')

organizeComments(insuranceAppsRBC, insuranceListRBC, 'RBC_insurance_googleplaydata')

organizeComments(bankingAppsMaster, bankingListMaster, 'banking_googleplaydata_master')

organizeComments(investmentAppsMaster, investmentListMaster, 'investment_googleplaydata_master')

organizeComments(insuranceAppsMaster, insuranceListMaster, 'insurance_googleplaydata_master')

# for each in resultsList:
#     getComments(each, testList)
# print(len(testList))
#
# for each in bankingAppsRBC:
#     getComments(each, bankingListRBC)
# print(len(bankingListRBC))
#
# for each in investmentAppsRBC:
#     getComments(each, investmentListRBC)
# print(len(investmentListRBC))
#
# for each in insuranceAppsRBC:
#     getComments(each, insuranceListRBC)
# print(len(insuranceListRBC))

# for item in testList:
#     print(item)

# listToText(testList, 'RBC_googleplaydata')
#
# print(len(masterList))
