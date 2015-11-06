#@author: Marjan Alavi

import os.path
import re

#-----------------------------------------------

def clearTweet(s):
    #keep track of tweets which contain unicode characters in them (count even ascii unicodes, bur replace only non-ascii ones)
    global unicodeCnt
    searchresult = r1.search(s)
    if searchresult is not None:
        unicodeCnt += 1
    
    #first replace \n and \t with space character
    s = s.replace('\\n', ' ')
    s = s.replace('\\t', ' ')
    
    #replace multiple consecutive spaces with only one space
    #s = ' '.join(s.split())
    
    #first remove unicodes and then replace remaining escape characters
    result = r3.sub(r'',s)
    result = r2.sub(r'\1', result)
     
    return result

#-----------------------------------------------

if __name__ == '__main__':
    global unicodeCnt
    r1 = re.compile(r'\\u[0-9A-Fa-f]{4}') 
    '''
    but this excludes all unicode characters, we are interested keeping ascii unicode characters in the 
    basic latin category ; i.e. x0020-x007F. So I came up with the following regular expression to solve this
    '''
    #r3 = re.compile(r'\\u[^0]...|\\u.[^0]..|\\u..[^2-7].|\\u...[^0-9A-Fa-f]')
    r3 = re.compile(r'\\u[^0][0-9A-Fa-f]{3}|\\u[0-9A-Fa-f][^0][0-9A-Fa-f]{2}|\\u[0-9A-Fa-f]{2}[^2-7][0-9A-Fa-f]|\\u[0-9A-Fa-f]{3}[^0-9A-Fa-f]')

    #r2 = re.compile(r"\\(.)")
    r2 = re.compile(r"\\([^u])")
    unicodeCnt = 0
    
    currentPath = os.path.dirname(__file__)
    parentPath = (os.path.dirname(currentPath))
    
    getRelPaths = lambda x: os.path.abspath(os.path.join(parentPath, x))
    
    inpFile = getRelPaths('tweet_input/tweets.txt')
    
    outFileF1 = getRelPaths('tweet_output/ft1.txt') 
    
    #I will maintain tweets as I read/clean the file in a list, and write all results at the end to the output file   
    cleanedResList = []
    
    with open(inpFile) as inputTweets, open(outFileF1, 'w') as outCleanedTweets:
        for line in inputTweets:
            timeSubline = line.split("\"created_at\":\"",1)
            if(len(timeSubline) >= 2):
                timestamp = timeSubline[1].split('"',1)[0]
            
            textsubline = line.split("\"text\":\"",1)
            if(len(textsubline) >= 2):
                text = textsubline[1].split('","',1)[0]
                cleanedText = clearTweet(text)
                
                finalResult = cleanedText+' ('+"timestamp: "+timestamp+')'
                cleanedResList.append(finalResult)
                
                #print(finalResult)
                #print('*****')
        
        for item in cleanedResList:
            outCleanedTweets.write(item+'\n')
            
        print (str(unicodeCnt) + " tweets contained unicode.")
        outCleanedTweets.write('\n'+str(unicodeCnt) + " tweets contained unicode.\n")

#-----------------------------------------------
