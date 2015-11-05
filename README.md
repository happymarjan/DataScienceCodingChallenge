@Marjan Alavi
I've written the code in python and have documented the provided codes with comments in the code. I've not used any special libraries; I've just used python collections, itertools and re modules.
I've counted the total number of tweets that contained unicode(even ascii unicodes in basic latin category). However, I do the replacement only for unicodes outside this category. This is easy to change in the code, but I understood this from the specification.  
I've cleaned hashtags of feature 2 based on what I did for feature 1, as been stated in problem definition. So, I did not do any further check to make sure the hashtag conforms to Twitter definitions for an acceptable hashtag.   
