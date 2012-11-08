# Fun with Words

"""
A portmanteau word is a blend of two or more words, like 'mathelete',
which comes from 'math' and 'athelete'.  You will write a function to
find the 'best' portmanteau word from a list of dictionary words.
Because 'portmanteau' is so easy to misspell, we will call our
function 'natalie' instead:

    natalie(['word', ...]) == 'portmanteauword' 

In this exercise the rules are: a portmanteau must be composed of
three non-empty pieces, start+mid+end, where both start+mid and
mid+end are among the list of words passed in.  For example,
'adolescented' comes from 'adolescent' and 'scented', with
start+mid+end='adole'+'scent'+'ed'. A portmanteau must be composed
of two different words (not the same word twice).

That defines an allowable combination, but which is best? Intuitively,
a longer word is better, and a word is well-balanced if the mid is
about half the total length while start and end are about 1/4 each.
To make that specific, the score for a word w is the number of letters
in w minus the difference between the actual and ideal lengths of
start, mid, and end. (For the example word w='adole'+'scent'+'ed', the
start,mid,end lengths are 5,5,2 and the total length is 12.  The ideal
start,mid,end lengths are 12/4,12/2,12/4 = 3,6,3. So the final score
is

    12 - abs(5-3) - abs(5-6) - abs(2-3) = 8.

yielding a score of 12 - abs(5-(12/4)) - abs(5-(12/2)) -
abs(2-(12/4)) = 8.

The output of natalie(words) should be the best portmanteau, or None
if there is none. 

Note (1): I got the idea for this question from
Darius Bacon.  Note (2): In real life, many portmanteaux omit letters,
for example 'smoke' + 'fog' = 'smog'; we aren't considering those.
Note (3): The word 'portmanteau' is itself a portmanteau; it comes
from the French "porter" (to carry) + "manteau" (cloak), and in
English meant "suitcase" in 1871 when Lewis Carroll used it in
'Through the Looking Glass' to mean two words packed into one. Note
(4): the rules for 'best' are certainly subjective, and certainly
should depend on more things than just letter length.  In addition to
programming the solution described here, you are welcome to explore
your own definition of best, and use your own word lists to come up
with interesting new results.  Post your best ones in the discussion
forum. Note (5) The test examples will involve no more than a dozen or so
input words. But you could implement a method that is efficient with a
larger list of words.
"""
import re
from collections import deque


def natalie(words):
    "Find the best Portmanteau word formed from any two of the list of words."
    possible_portmanteau = []
    for word in words:
        i = 1
        while(i < len(word)):
            other_words = [w for w in words if w != word] # any word other than the root word. Better algorithm below
            anchor_word = word[i:] # anchor word is the common word. Key is to find the anchor word. Better alogorithm below
            for ow in other_words:
                match = re.match('('+anchor_word +')' + r'.*',ow)
                if match:
                    possible_portmanteau.append((i,len(match.group(1)),len(ow)-len(match.group(1)),word[0:i]+ow))
            i = i+1
    
    scored_portmanteau = []
    best_portmanteau = None
    best_score = None
    for portmanteau in possible_portmanteau:
        start,mid,end,word = portmanteau
        length = len(word)
        ideal_start,ideal_mid,ideal_end = length/4,length/2,length/4
        score = length - abs(start-ideal_start) - abs(mid-ideal_mid) - abs(end-ideal_end)
        if not best_score or best_score < score:
            best_score = score
            best_portmanteau = word
    return best_portmanteau


# More efficient algorithm to create portmanteau
def natalie_efficient(words):
    possible_portmanteau = []
    words = deque(words)
    i = 0
    while(i < len(words)):
        word = words.popleft() # use queues to prevent another loop.
        for ow in words:
            combined_word = word + ow
            match = re.sub(r'(\w{2,})\1',r'\1',combined_word) # check for repeated words 2 or more in length
            if len(match) != len(combined_word):
                possible_portmanteau.append(match)
        words.append(word)
        i += 1
    print possible_portmanteau 
    
def test_natalie():
    "Some test cases for natalie"
    assert natalie(['adolescent', 'scented', 'centennial', 'always', 'ado']) in ('adolescented','adolescentennial')
    assert natalie(['eskimo', 'escort', 'kimchee', 'kimono', 'cheese']) == 'eskimono'
    assert natalie(['kimono', 'kimchee', 'cheese', 'serious', 'us', 'usage']) == 'kimcheese'
    assert natalie(['circus', 'elephant', 'lion', 'opera', 'phantom']) == 'elephantom'
    assert natalie(['programmer', 'coder', 'partying', 'merrymaking']) == 'programmerrymaking'
    assert natalie(['int', 'intimate', 'hinter', 'hint', 'winter']) == 'hintimate'
    assert natalie(['morass', 'moral', 'assassination']) == 'morassassination'
    assert natalie(['entrepreneur', 'academic', 'doctor', 'neuropsychologist', 'neurotoxin', 'scientist', 'gist']) in ('entrepreneuropsychologist', 'entrepreneurotoxin')
    assert natalie(['perspicacity', 'cityslicker', 'capability', 'capable']) == 'perspicacityslicker'
    assert natalie(['backfire', 'fireproof', 'backflow', 'flowchart', 'background', 'groundhog']) == 'backgroundhog'
    assert natalie(['streaker', 'nudist', 'hippie', 'protestor', 'disturbance', 'cops']) == 'nudisturbance'
    assert natalie(['night', 'day']) == None
    assert natalie(['dog', 'dogs']) == None
    assert natalie(['test']) == None
    assert natalie(['']) ==  None
    assert natalie(['ABC', '123']) == None
    assert natalie([]) == None
    return 'tests pass'

if __name__ == '__main__':
    print test_natalie()


