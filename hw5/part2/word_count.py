# word_count.py
# ===================================================
# Implement a word counter that counts the number of
# occurrences of all the words in a file. The word
# counter will return the top X words, as indicated
# by the user.
# ===================================================
#Name: Michael Kim
#class :CS 261 -400
#date June 1 2020

import re
from hash_map import HashMap

"""
This is the regular expression used to capture words. It could probably be endlessly
tweaked to catch more words, but this provides a standard we can test against, so don't
modify it for your assignment submission.
"""
rgx = re.compile("(\w[\w']*\w|\w)")

def hash_function_2(key):
    """
    This is a hash function that can be used for the hashmap.
    """

    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash

def top_words(source, number):
    """
    Takes a plain text file and counts the number of occurrences of case insensitive words.
    Returns the top `number` of words in a list of tuples of the form (word, count).

    Args:
        source: the file name containing the text
        number: the number of top results to return (e.g. 5 would return the 5 most common words)
    Returns:
        A list of tuples of the form (word, count), sorted by most common word. (e.g. [("a", 23), ("the", 20), ("it", 10)])
    """

    keys = []

    ht = HashMap(100,hash_function_2)


    # This block of code will read a file one word as a time and
    # put the word in `w`. It should be left as starter code.
    with open(source) as f:
        for line in f:
            words = rgx.findall(line)
            for w in words:
                keys.append(w.lower())
                #appends the individual words to the list of words shown above

        #preliminary loop
        for i in set(keys):
            #iterates through the words once and puts every unique word in the hash table
            #if the word is repeated, the value in the hash is merely updated to 0
            ht.put(i,0)

        #counting loop will count the words
        for i in keys:
            #iterates through list and retrieves the associated value
            value=ht.get(i)
            value+=1
            #increases the value by one
            ht.put(i,value)
            #replaces the old value with the new incremented value
        sortedList=[]
        #new list of words and word counts
        #appending iterator
        for i in keys:
            #gets every value in the hash table
            value=ht.get(i)
            #appends the above list with each key value pair as a list
            sortedList.append([i,value])


        #to remove duplicated hash values
        res=[]
        for i in sortedList:
            #for every entry in list
            if i not in res:
                #if theres a repetition, not included
                res.append(i)
        #function to sort the list from greatest to least
        def Sort(list):
            list.sort(key=lambda x: x[1], reverse=True)
            return list
        Sort(res)
        #use it on the filtered list
        res=res[:number]
        #cut the list down to the appropriate number of entries
        final_list=[]


        #final list for the tuples
        for i in res:

        #iterates and appends list as tuples
             final_list.append( tuple(i))
        return final_list



