#@author: Marjan Alavi

import os.path
from collections import defaultdict
from collections import OrderedDict
import itertools
import time
import re

#-----------------------------------------------

def clearTweet(s):
    #first replace \n and \t with space character
    s = s.replace('\\n', ' ')
    s = s.replace('\\t', ' ')
    
    #replace multiple consecutive spaces to only one space 
    #s = ' '.join(s.split())
    
    #first remove unicodes and then replace remaining escape characters
    result = r3.sub(r'',s)
    result = r2.sub(r'\1', result)
     
    return result

#-----------------------------------------------

if __name__ == '__main__': 
    #r1 = re.compile(r'\\u[0-9A-Fa-f]{4}') 
    '''
    but this excludes all unicode characters, we are interested keeping ascii unicode characters in the 
    basic latin category ; i.e. x0020-x007F. So I came up with the following regular expression to solve this
    '''
    #r3 = re.compile(r'\\u[^0]...|\\u.[^0]..|\\u..[^2-7].|\\u...[^0-9A-Fa-f]')
    r3 = re.compile(r'\\u[^0][0-9A-Fa-f]{3}|\\u[0-9A-Fa-f][^0][0-9A-Fa-f]{2}|\\u[0-9A-Fa-f]{2}[^2-7][0-9A-Fa-f]|\\u[0-9A-Fa-f]{3}[^0-9A-Fa-f]')

    #r2 = re.compile(r"\\(.)")
    r2 = re.compile(r"\\([^u])")
    
    hashtagsDict = OrderedDict() 
    nodeDict = defaultdict(list)
    degreeDict = defaultdict(lambda: 0)
        
    currentPath = os.path.dirname(__file__)
    parentPath = (os.path.dirname(currentPath))
    getRelPaths = lambda x: os.path.abspath(os.path.join(parentPath, x))
    
    inpFile = getRelPaths('tweet_input/tweets3.txt')    
    
    outFileF2 = getRelPaths('tweet_output/ft2.txt')
    
    with open(inpFile) as inputTweets, open(outFileF2, 'w') as outAvgHashtags:
        for line in inputTweets:
            timeSubline = line.split("\"created_at\":\"",1)
            if(len(timeSubline) >= 2):
                timestamp = timeSubline[1].split('"',1)[0]
                timestampInEpoch = time.mktime(time.strptime(timestamp,"%a %b %d %H:%M:%S +0000 %Y"))
            else:  #the tweet does not have timestamp field, or is malformed, so skip to next tweet
                continue
            
            textsubline = line.split("\"text\":\"",1)
            if(len(textsubline) >= 2):
                text = textsubline[1].split('","',1)[0]
                text = clearTweet(text)

            hashtags = ""
            if text is not None:
                #Some hashtags currently have no characters remaining because of the cleaning step, lets exclude those empty hashtags 
                hashtagsList = [tag for tag in text.split() if (tag.startswith("#") and tag!="#")]
                hashtagsList = list(set(hashtagsList)) #well,lets make sure there is no duplicates there
                     
                hashtags = ', '.join(hashtagsList)

                finalResult = hashtags+' ('+"timestamp: "+timestamp+')'
            else:
                finalResult ='('+"timestamp: "+timestamp+')'
                
            allowedEpochMin = timestampInEpoch - 60 #any epoch smaller than this minimum is considered old 
             
             
            '''
            initially, for the first tweet, this hashtagsDict dictionary is empty. Then, it gets filled further down in the code. 
            It is defined as an ordered dictionary so as to maintain order of the added keys. This (ordered) dictionary is basically 
            a dictionary of time epochs as keys and list of separate hashtag pairs as values. This will be very helpful for deleting 
            old tweets.
            '''
            for t in hashtagsDict.keys():
                if t < allowedEpochMin:
                    #some tweets are old enough, lets remove associated edges for corresponding hashtags in old tweets
                    for tagPair in hashtagsDict[t]: 
                        pr0 = tagPair[0]
                        pr1 = tagPair[1]
                        listpr0 = nodeDict.get(pr0)
                        #note that as Twitter hashtags in a tweet are limited to certain number (because of 140 character limit), even remove() function O(n) would take
                        #constant time in practice. Alternatively, I could put the whole list in a new list without putting the deleted items
                        if pr1 in listpr0: listpr0.remove(pr1)
                        listpr1 = nodeDict.get(pr1)
                        if pr0 in listpr1: listpr1.remove(pr0)
                      
                    #and finally remove old time epochs from the dictionary keys  
                    hashtagsDict.pop(t, None)
                  
                #The dict is ordered(and tweets are time-ordered based on spec.), so as soon as I get to a key with a time epoch larger than the allowed minimum, I break from the loop and stop further time tests  
                else:
                    break
                    
            
            
            #Lets define all different combinations of hashtag pairs. (The order of hashtag pairs does not matter, so I use combinations for this task)
            tagPairs = [list(x) for x in itertools.combinations(hashtagsList, 2)]
            
            for pair in tagPairs:
                #lets make sure hashtags are case-insensitive
                pair0 = pair[0].encode('utf-8').lower()
                pair1 = pair[1].encode('utf-8').lower()  
                
                #the graph is not a directed graph, so lets preserve just one ordering; based on a simple comparison             
                if pair1 > pair0:
                    tagTuple = (pair0,pair1)
                else:
                    tagTuple = (pair1,pair0)
                ##print (tagTuple)
          
                #here is where the aforementioned ordered dictionary gets filled
                hashtagsDict.setdefault(timestampInEpoch,[]).append(tagTuple)
                
                #A dictionary of lists for each node, so I know each node has an edge to which other nodes; so as to be able to keep track of degree updates.
                nodeDict[pair0].append(pair1)
                nodeDict[pair1].append(pair0)

            totalDegree = 0.0
            
            '''
            I access the adjacency list for a given node, remove any duplicates(note that duplicates is very possible here and part f the reason of why this
             code works!) and obtain the degree of that node. I keep degrees for all nodes in a dictionary with degree initialized to zero
            '''
            for item in nodeDict:
                val = nodeDict[item] 
                degreeDict[item] = len(set(val))
                totalDegree += degreeDict[item]
            degreeDictLen = len(degreeDict) 
            #If the number of nodes that I have at the moment is positive, I calculate the vaerage degree
            if degreeDictLen > 0:
                totalDegree = round(totalDegree/degreeDictLen,2)
                
                ##print (totalDegree)
                
                #writing the average degree to the file
                outAvgHashtags.write(str(totalDegree) + '\n')
        print ('done')
                        
#-----------------------------------------------
 
