# CS1210 Homework3
#
# This file should contain only your own work; there are no partners
# assigned or permitted for Homework assignments.
#
# I certify that the entirety of this file contains only my own work.
# I have not shared the contents of this file with anyone in any form,
# nor have I obtained or included code from any other source aside
# from the code contained in the original homework template file.
import re
from string import punctuation
import matplotlib.pyplot as plt
import networkx as nx
from random import randint

######################################################################
# Edit the following function definition so it returns a tuple
# containing a single string, your hawkid.
######################################################################
def hawkid():
    return(("hawkid",))

######################################################################
# Regular expressions to expand contractions. Ordering reflects
# application order.
RE = ( ("([a-z])n['’]t\\b","\\1 not"),        # (provided)
       ("([a-z])['’]d\\b", "\\1 had"), 
       ("([a-z])['’]ve\\b", "\\1 have"), 
       ("([a-z])['’]s\\b", "\\1 is"),         # Messes up possessives (['’]s).
       ("([a-z])['’]m\\b", "\\1 am"),
       ("([a-z])['’]re\\b", "\\1 are"), 
       ("([a-z])['’]ll\\b", "\\1 will"),
       ("\\bma['’]a?m\\b", "madam"),	   # (provided) Abbrevs like Mme.?
       ("\W([a-z])-([a-z])", "\\1\\2"),    # (provided) Merge stutters
       ("-+", " ") )			   # (provided) Split words at hyphens.

######################################################################
# readFile(filename, regexes) returns a list of words read from the
# specified file. The second argument is a list of regular expressions
# that should be applied to the text before stripping punctuation from
# the words in the text.
def readFile(F, regexes = RE):
    '''readFile(F, regexes = RE)
           Reads book from file F and returns it in the form of a list 
           of "cleaned up" (via application of regexes) single words.'''
    # Precompile substitution regexes.
    regexes = [ (re.compile(regex[0], re.IGNORECASE), regex[1]) for regex in regexes ]
 
    # Open file for reading.
    L = []
    file = open(F, 'r')
    for line in file:
        # Ditch empty lines or lines that are all caps
        if line.strip() != '' and line.upper() != line:
            # Apply regex corrections to the resulting string
            # and collect surviving lines.
            for regex in regexes:
                line = regex[0].sub(regex[1], line)
            L.append(line)
    file.close()

    # Produce a word list.
    W = ' '.join(L).split()
    print("Read {} words".format(len(W)))

    # Return the list of words, stripping punctuation as you go.
    return([ w.strip(punctuation) for w in W if len(w.strip(punctuation)) > 0 ])

######################################################################
# findNouns(W, cmin=1) returns a dictionary of proper nouns (as keys)
# and their occurrance counts (as values) provided each key noun
# appears at least cmin times in the text.
def findNouns(W, cmin=1):
    '''findNouns(W, cmin=1)
           Identifies a set of proper nouns from word list W. Proper nouns
           are words that only appear in capitalized form. Returns a dictionary
           of proper nouns occurring at least cmin times with their respective
           occurrance count as the value.'''
    # Count noun candidates
    N = {}
    # Scan words in book for nouns (or noun clusters?)
    for w in W:
        # A noun appears titlecase; moreover, aside from 'I' is longer
        # than 1 letter.
        if w.capitalize() == w and (len(w)>1 or w == 'I'):
            # A noun candidate
            if w.lower() not in N:
                N[w.lower()] = 1
            elif N[w.lower()] > 0:
                N[w.lower()] = N[w.lower()] + 1
    print("Found {} candidate nouns".format(len(N)))

    # Now discard nouns that appeared elsewhere in lowercase or didn't
    # appear often enough to matter.
    for w in W:
        if (w.lower() in N and (w == w.lower() or N[w.lower()] < cmin)):
            del N[w.lower()]
    print("Retaining {} common nouns".format(len(N)))
    return(N)

######################################################################
# buildIndex(W, N) returns a dictionary of proper nouns (as keys)
# taken from N and the index value in W for each occurrance of the key
# noun.
def buildIndex(W, N):
    '''buildIndex(W, N)
           Takes as input a word list W and a proper noun dictionary
           N with noun:count entries and returns a dictionary with
           noun:list-of-indeces entries, where each index is a list of 
           locations in W.'''
    # Initialize the index.
    I = { noun:[] for noun in N }

    # Construct an index.
    for i in range(len(W)):
        if W[i].lower() in I:
            I[W[i].lower()].append(i)
    return(I)

######################################################################
# plotChars(N, I, W, xsteps=10) uses matplotlib to plot a character
# plot like the one shown in the handout, where N is a dictionary of
# proper nouns (as returned by findNouns()), I is an index of proper
# nouns and their locations in the text (as returned by buildIndex()),
# W is a list of words in the text (as returned by readFile()) and
# xsteps is the window size within which we count occurrences of each
# character.
def plotChars(N, I, W, xsteps=10):
    '''plotChars(N, I, W, xsteps=10)
           Takes as input an index of proper nouns N (format noun:occurrances),
           a similar index I (format noun:list-of-indeces), and
           a word list W, producing a plot of character activity as
           a function of location in the book represented by W.
           Optional argument xsteps governs the granularity of the plot.'''
    # Plot characters in C according to their index.
    # Helper function.
    def occur(c, I, lo, hi):
        return( len([ loc for loc in I[c] if loc >= lo and loc < hi ]) )

    # Can step over keys of either I or N, although if I use N, I can
    # recompute N and reuse previously computed I (provided new N has
    # fewer nouns than the N used to buildIndex()).
    C = { c:([0] + [ occur(c, I, i*len(W)//xsteps, (i+1)*len(W)//xsteps) for i in range(0, xsteps) ]) for c in N.keys() }
    ymax = round(1.3*max([ max(v) for v in C.values() ]))

    # Plot title and axis labels.
    plt.title('Character plot')
    plt.axis( [ 0, xsteps, 0, ymax ] )
    plt.xlabel('Location (text%)')
    plt.ylabel('Mentions')
    if xsteps > 10:
        plt.xticks([ x for x in range(0, xsteps+1, xsteps//10) ], [ str(p) for p in range(0, 101, 10) ])
    else:
        plt.xticks(list(range(xsteps)), [ str(p) for p in range(0, 101, 100//xsteps) ])
    plt.yticks([ y for y in range(0, ymax, ymax//10) ])

    # Set up characters.
    for c in C.keys():
        plt.plot( [ x for x in range(xsteps+1) ], C[c], label=c.capitalize() )
    # Show labels.
    plt.legend(loc='upper left')
    # Display it.
    plt.show()

######################################################################
# mapChars(N, I. imin, imax, dmax) uses networkx and matplotlib to
# plot a graph linking characters (nodes) to each other with a set of
# weighted edges, where each edge represents the number of occurrences
# of the two characters within dmax words of each other for each
# character occurrance between words imin and imax in the text.
def mapChars(N, I, imin, imax, dmax):
    edges = []
    # i am sorting N that way i can iterate through the different keys of I in a more efficient way
    S = sorted(N)
    #For the first word in S, find the weight of word 1 and word 2, then word 1 and word 3, and so on.
    #This code also makes sure that words arent compared twice
    for i in range(len(N)):
        for x in range(i+1,len(N)):
            weight = []
            # step through each index (location) of a certian word, and if it is in a specific range and the difference between
            # the location of said word, and any locations of the second word is less than dmax, then another item will be
            # appended to the list
            for loc1 in I[S[i]]:
                for loc2 in I[S[x]]:
                    if loc1 in range(imin,(imax+1)) and abs(loc1-loc2) < dmax:
                        weight.append(1)
            #make a list of tuples called edges that can be used in the add_edges_from method
            #However, if the weight is 0, then the item shouldnt be appended
            if len(weight) !=0:
                edges.append((S[i], S[x], {'weight': len(weight) }))
    # perform graph functions and show the graph
    G = nx.Graph()
    G.add_nodes_from(I)
    G.add_edges_from(edges)
    nx.draw_spring(G, title = 'Character Map', with_labels = True)
    plt.show()

######################################################################
# plot(file='wind.txt', cmin=100, xsteps=10) is a driver that manages
# the entire analysis and plotting process. It is presented to give
# you an idea of how to use the functions you've just designed.
def plot(file='wind.txt', cmin=100, xsteps=10):
    '''plot(file='wind.txt', cmin=100, xsteps=10)
           Convenient driver function to test system as a whole.'''
    W=readFile(file)
    N=findNouns(W, cmin)
    I=buildIndex(W, N)
    plotChars(N, I, W, xsteps)
    for i in range(xsteps):
        # Do something with mapChars() here
        mapChars(N, I, int((len(W)//xsteps)*i), int((len(W)//xsteps)*(i+1)), dmax = int(len(W)//xsteps)//2)
    
