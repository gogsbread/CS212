"""
Logic Puzzle
------------

You will write code to solve the following logic puzzle:

1. The person who arrived on Wednesday bought the laptop.
2. The programmer is not Wilkes.
3. Of the programmer and the person who bought the droid,
   one is Wilkes and the other is Hamming. 
4. The writer is not Minsky.
5. Neither Knuth nor the person who bought the tablet is the manager.
6. Knuth arrived the day after Simon.
7. The person who arrived on Thursday is not the designer.
8. The person who arrived on Friday didn't buy the tablet.
9. The designer didn't buy the droid.
10. Knuth arrived the day after the manager.
11. Of the person who bought the laptop and Wilkes,
    one arrived on Monday and the other is the writer.
12. Either the person who bought the iphone or the person who bought the tablet
    arrived on Tuesday.

You will write the function logic_puzzle(), which should return a list of the
names of the people in the order in which they arrive. For example, if they
happen to arrive in alphabetical order, Hamming on Monday, Knuth on Tuesday, etc.,
then you would return:

['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']

(You can assume that the days mentioned are all in the same week.)
"""
import itertools

PERSONS = ['Wilkes','Hamming','Knuth','Minsky','Simon']

def logic_puzzle():
    wilkes,hamming,knuth,minsky,simon = PERSONS
    ordering = list(itertools.permutations(PERSONS))
    return next([mon,tue,wed,thu,fri] for (mon,tue,wed,thu,fri) in ordering
           for (laptop,droid,tablet,iphone,_) in ordering
            for (programmer,writer,manager,designer,_) in ordering
                        if(wed == laptop and programmer != wilkes and \
                        (programmer == hamming and droid == wilkes) and \
                        (writer != minsky) and \
                        (knuth != manager and tablet != manager) and \
                        ((mon == simon and tue == knuth) or (tue == simon and wed == knuth) or (wed == simon and thu == knuth) or (thu == simon and fri == knuth)) and \
                        (thu != designer) and (fri != tablet) and (designer != droid) and (manager == simon)
                        and ((laptop == mon and wilkes == writer) or (laptop == writer and wilkes == mon)) and \
                        ((iphone == tue) or (tablet == tue)))
                )

def test_unit():
    assert ['Wilkes', 'Simon', 'Knuth', 'Hamming', 'Minsky'] == logic_puzzle()
    print 'test pass'

if __name__ == '__main__':
    test_unit()
    
