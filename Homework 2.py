# CS1210 Homework2
#
# This file should contain only your own work; there are no partners
# assigned or permitted for Homework assignments.
#
# I certify that the entirety of this file contains only my own work.
# I have not shared the contents of this file with anyone in any form,
# nor have I obtained or included code from any other source aside
# from the code contained in the original homework template file.
from string import punctuation
import matplotlib.pyplot as plt
import re
######################################################################
# Edit the following function definition so it returns a tuple
# containing a single string, your hawkid.
#
# THE AUTOGRADER WILL FAIL TO ASSIGN A GRADE IF YOUR HAWKID IS NOT
# PROPERLY INCLUDED IN THIS FUNCTION. CAVEAT EMPTOR.
######################################################################
def hawkid():
    '''Used by CS1210 Autograder to extract student identity from code.'''
    return(("jtkolich",))

######################################################################
# Some sample regular expressions.
RE = ( ("([A-Za-z]*)n't\\b","\\1 not"),        # "...n't" => "... not"
       ("\\bma'a?m\\b", "madam"),          # Abbrevs like Mme.?
       ("\W([a-z])-([a-z])", "\\1\\2"),    # Merge stutters like k-k-kick
       ("([a-zA-Z]*)'s","\\1 is"),         # split a "...'s" word into "... is"
       ("([a-zA-Z]*)ty","\\1"),            # turns "...ty" into "..."
       ("([A-Za-z]*)\-+([A-Za-z]*)","\\1 \\2"), #turns a double hyphen word into two words
       ("([A-Za-z]*)'m\\b","\\1 am"),           # turns words like "i'm" into "i am"
       ("([A-Za-z]*)'ll\\b","\\1 will"),             # turns words like "i'll" into "i will"
       ("([A-Za-z]*)'ve\\b","\\1 have"))         # turns words like "i've" into "i have"
######################################################################
# readFile(filename, regexes) returns a list of words read from the
# specified file. The second argument is a list of regular expressions
# that should be applied to the text before stripping punctuation from
# the words in the text.
def readFile(file, regexes = RE):
    '''This function takes a file as an argument, and returns a list of words
        contained in the file'''
    # create a empty list that will eventually contain each word
    W = []
    # iterate through each line in the file and then run through each word
    for line in open(file,'r'):
       for word in line.strip('\n').split():
           #for each word, this checks if the word is matched by a regular expression
           for i in range(len(RE)):
               # if the word is a regular expression, it is substituted as the form shown above
               if re.search(RE[i][0],word.strip(punctuation)) != None:
                   word = (re.sub(RE[i][0],RE[i][1],word.strip(punctuation)))
           # the word, in its original or changed form, is now appended to the list of total words 
           W.append(word.strip(punctuation))
    #becasue the results of re.sub will not be split up into two different words, the return statement goes back
    # through the file and 
    return [word for words in W for word in words.split()]

######################################################################
# findNouns(W, cmin=1) returns a dictionary of proper nouns (as keys)
# and their occurrance counts (as values) provided each key noun
# appears at least cmin times in the text.
def findNouns(W, cmin=1):
    '''returns a dictionary of proper nouns (as keys) and their occurrance counts (as values)
        provided each key noun appears at least cmin times in the text'''
    # common words are words that typically are at the beginning of a sentence, and therefore they look slightly
    # like nouns, but they aren't relevant to the plot so they must be removed somehow. Words that refer to someone like
    # prince, lord, or count are also removed to avoid redundancies
    commonWords = ['Then','Well', 'What', 'When', 'There', 'Here', 'They', 'This', 'Come', 'These','Meantime','His','Far',
              'The', 'That', 'Whose','She', 'Hers', 'Her', 'You', 'And', 'But', 'Now', 'Not', 'Who', 'Like', 'Wide', 'Fix',
                ' Just', 'Close', 'Our', 'Tis', 'Has', 'Had', 'Till', 'See', 'Whom', 'Those', 'That', 'Let', 'Safe','One','Count','Emperor',
                   'Fierce', 'Nor', 'Why', 'Water', 'Next', 'Swift', 'Which', 'Their', 'Each', 'All', 'High', 'Some', 'How',
                   'With', 'Wood','For', 'Yet','Wild', 'Hall', 'Such','Even','Thy','Great','Full', 'Shall', 'Through', 'From',
                   'Where', 'While', 'Soon', 'Thus','This', 'Whoe', 'Say', 'Fate', 'Thee', "O'er",'Instant',"E'en",'Still','Fast',
                   'Before','Your','Two','Three','Hear','Though','Around','Lest', 'Meanwhile', 'Once', 'Prince', 'Princess',
                   'Are','Countess','Hills','Frenchman','Guards','During','Bald','Tsar','Lord','Besides','After','Only','Having','Just','Yes']
    # create an empty dictionary to store the nouns and thie counts in
    D = {}
    # create a counter to keep track of how many nouns have been counted
    counter = 0
    #Set paramaters that are characteristic of nouns. first letter capitalized followed by lowercase letters, etc.
    ### Although the professor included "I" in his list of valid nouns, i thought that was too subjective as "I" could be
    ### referring to many different characters instead of a narrator
    for word in W:
        if len(word) >2 and word not in D and word == word.title() and  word not in commonWords and W.count(word)>cmin:
           D[word]=W.count(word)
    # display how many nouns out of the significant ones have been counted in total and how many nouns there are
    for key in D:
        counter += D[key]
    print ("Counted {} Significant Nouns Across {} Words".format(counter,len(D)))
    return(D)

######################################################################
# buildIndex(W, N) returns a dictionary of proper nouns (as keys)
# taken from N and the index value in W for each occurrance of the key
# noun.
def buildIndex(W, N):
    '''returns a dictionary of proper nouns (as keys) taken from N and the index value
        in W for each occurrance of the key noun.'''
    D = {}
    # for each of the words in N, create a dictionary key that has a list as its value
    for word in N:
        # the list should contain the position (pos) of the word only if the word at the position of enumerate (watpos) is the word
        D[word] = [pos for pos, watpos in enumerate(W) if watpos == word]
    return(D)

######################################################################
# plotChars(N, I, W, xsteps=100) uses matplotlib to plot a character
# plot like the one shown in the handout, where N is a dictionary of
# proper nouns (as returned by findNouns()), I is an index of proper
# nouns and their locations in the text (as returned by buildIndex()),
# W is a list of words in the text (as returned by readFile()) and
# xsteps is the window size within which we count occurrences of each
# character.
def plotChars(N, I, W, xsteps=100):
    '''plotChars(N, I, W, xsteps=100) uses matplotlib to plot a character plot like the one shown in the handout, where N is a dictionary of
         proper nouns (as returned by findNouns()), I is an index of proper nouns and their locations in the text (as returned by buildIndex()),
        xsteps is the window size within which we count occurrences of each character.'''
    #as sain in the homework description, k is the length of W integer divided by xsteps
    k = len(W) // xsteps
    # create empty x and y list to be used as input plot values
    for char in N:
        x = []
        y = []
        #iterate through W in steps that are k elements long and count how many times a character appears in those lengths
        for i in range(0,len(W),k):
            y.append(W[i:i+k].count(char))
            x.append((i/(len(W)))*100) 
        plt.plot(x,y,label = char)
    #basic plotting methods that matplotlib accepts
    plt.title("Character Map")
    plt.xlabel("Location (text %)")
    plt.ylabel("Number of Mentions")
    plt.legend()
    return(plt.show())

######################################################################
# plot(file='wind.txt', cmin=100, xsteps=100) is a driver that manages
# the entire analysis and plotting process. It is presented to give
# you an idea of how to use the functions you've just designed.
def plot(file='wind.txt', cmin=100, xsteps=100):
    '''Drive analysis of text contained in file.'''
    W=readFile(file)
    N=findNouns(W, cmin)
    plotChars(N, buildIndex(W, N), W, xsteps)
