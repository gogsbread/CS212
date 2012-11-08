# Unit 5: Probability in the game of Darts

"""
In the game of darts, players throw darts at a board to score points.
The circular board has a 'bulls-eye' in the center and 20 slices
called sections, numbered 1 to 20, radiating out from the bulls-eye.
The board is also divided into concentric rings.  The bulls-eye has
two rings: an outer 'single' ring and an inner 'double' ring.  Each
section is divided into 4 rings: starting at the center we have a
thick single ring, a thin triple ring, another thick single ring, and
a thin double ring.  A ring/section combination is called a 'target';
they have names like 'S20', 'D20' and 'T20' for single, double, and
triple 20, respectively; these score 20, 40, and 60 points. The
bulls-eyes are named 'SB' and 'DB', worth 25 and 50 points
respectively. Illustration (png image): http://goo.gl/i7XJ9

There are several variants of darts play; in the game called '501',
each player throws three darts per turn, adding up points until they
total exactly 501. However, the final dart must be in a double ring.

Your first task is to write the function double_out(total), which will
output a list of 1 to 3 darts that add up to total, with the
restriction that the final dart is a double. See test_darts() for
examples. Return None if there is no list that achieves the total.

Often there are several ways to achieve a total.  You must return a
shortest possible list, but you have your choice of which one. For
example, for total=100, you can choose ['T20', 'D20'] or ['DB', 'DB']
but you cannot choose ['T20', 'D10', 'D10'].
"""

def test_darts():
    "Test the double_out function."
    assert double_out(170) == ['T20', 'T20', 'DB']
    assert double_out(171) == None
    assert double_out(100) in (['T20', 'D20'], ['DB', 'DB']) # Could be problem area. I am not specifically looking for this. That is why i should start with 0,60,59..
    print 'test_darts pass'

"""
My strategy: I decided to choose the result that has the highest valued
target(s) first, e.g. always take T20 on the first dart if we can achieve
a solution that way.  If not, try T19 first, and so on. At first I thought
I would need three passes: first try to solve with one dart, then with two,
then with three.  But I realized that if we include 0 as a possible dart
value, and always try the 0 first, then we get the effect of having three
passes, but we only have to code one pass.  So I creted ordered_points as
a list of all possible scores that a single dart can achieve, with 0 first,
and then descending: [0, 60, 57, ..., 1].  I iterate dart1 and dart2 over
that; then dart3 must be whatever is left over to add up to total.  If
dart3 is a valid element of points, then we have a solution.  But the
solution, is a list of numbers, like [0, 60, 40]; we need to transform that
into a list of target names, like ['T20', 'D20'], we do that by defining name(d)
to get the name of a target that scores d.  When there are several choices,
we must choose a double for the last dart, but for the others I prefer the
easiest targets first: 'S' is easiest, then 'T', then 'D'.
"""


def double_out(total):
    """Return a shortest possible list of targets that add to total,
    where the length <= 3 and the final element is a double.
    If there is no solution, return None."""
    single = range(1,21)
    double = [score * 2 for score in single] + [50]
    triple = [score * 3 for score in single]
    bulls_eye = [25,50]
    points = []
    dart_scores = [0] + sorted(set(triple + double + single + bulls_eye),reverse = True)
    #print dart_scores
    possible_ways = [(dart1,dart2,dart3) 
                        for dart1 in dart_scores 
                        for dart2  in dart_scores 
                        for dart3 in double 
                        if dart1+dart2+dart3 == total]
    if len(possible_ways) > 0:
        for score in possible_ways[0]: # assuming [0] to be the best possible because the scores are sorted in reverse which internally assumes the player hit the triple points in the first attempt
            if score != 0:
                if score in triple:
                    points.append('T' + str(score/3))
                elif score in bulls_eye:
                    points.append('SB' if score == 25 else 'DB')
                elif score in double:
                    points.append('D' + str(score/2))
                else:
                    points.append('S' + str(score))
    return points if len(points) > 0 else None
    


"""
It is easy enough to say "170 points? Easy! Just hit T20, T20, DB."
But, at least for me, it is much harder to actually execute the plan
and hit each target.  In this second half of the question, we
investigate what happens if the dart-thrower is not 100% accurate.

We will use a wrong (but still useful) model of inaccuracy. A player
has a single number from 0 to 1 that characterizes his/her miss rate.
If miss=0.0, that means the player hits the target every time.
But if miss is, say, 0.1, then the player misses the section s/he
is aiming at 10% of the time, and also (independently) misses the thin
double or triple ring 10% of the time. Where do the misses go?
Here's the model:

First, for ring accuracy.  If you aim for the triple ring, all the
misses go to a single ring (some to the inner one, some to the outer
one, but the model doesn't distinguish between these). If you aim for
the double ring (at the edge of the board), half the misses (e.g. 0.05
if miss=0.1) go to the single ring, and half off the board. (We will
agree to call the off-the-board 'target' by the name 'OFF'.) If you
aim for a thick single ring, it is about 5 times thicker than the thin
rings, so your miss ratio is reduced to 1/5th, and of these, half go to
the double ring and half to the triple.  So with miss=0.1, 0.01 will go
to each of the double and triple ring.  Finally, for the bulls-eyes. If
you aim for the single bull, 1/4 of your misses go to the double bull and
3/4 to the single ring.  If you aim for the double bull, it is tiny, so
your miss rate is tripled; of that, 2/3 goes to the single ring and 1/3
to the single bull ring.

Now, for section accuracy.  Half your miss rate goes one section clockwise
and half one section counter-clockwise from your target. The clockwise 
order of sections is:

    20 1 18 4 13 6 10 15 2 17 3 19 7 16 8 11 14 9 12 5

If you aim for the bull (single or double) and miss on rings, then the
section you end up on is equally possible among all 20 sections.  But
independent of that you can also miss on sections; again such a miss
is equally likely to go to any section and should be recorded as being
in the single ring.

You will need to build a model for these probabilities, and define the
function outcome(target, miss), which takes a target (like 'T20') and
a miss ration (like 0.1) and returns a dict of {target: probability}
pairs indicating the possible outcomes.  You will also define
best_target(miss) which, for a given miss ratio, returns the target 
with the highest expected score.

If you are very ambitious, you can try to find the optimal strategy for
accuracy-limited darts: given a state defined by your total score
needed and the number of darts remaining in your 3-dart turn, return
the target that minimizes the expected number of total 3-dart turns
(not the number of darts) required to reach the total.  This is harder
than Pig for several reasons: there are many outcomes, so the search space 
is large; also, it is always possible to miss a double, and thus there is
no guarantee that the game will end in a finite number of moves.
"""
ZONES = {'S':1,'D':2,'T':3}
SECTIONS = ['20', '1', '18', '4', '13', '6', '10', '15', '2', '17', '3', '19', '7', '16', '8', '11', '14', '9', '12','5']
RINGS = ['OFF','D','S','T','S','SB','DB']

def get_adjacents(cell,items):
    if cell == None:
        return items
    else:
        for index,item in enumerate(items):
            if item == cell:
                return [items[index-1],items[index],items[index+1]]

def get_adjacent_sections(section):
    if section == None:
        return SECTIONS
    else:
        index = SECTIONS.index(section)
        return [SECTIONS[index-1],SECTIONS[index],SECTIONS[(index+1)%len(SECTIONS)]]

def get_adjacent_rings(ring):
    index = RINGS.index(ring)
    if index == 0: #OFF
        return [RINGS[index],RINGS[index+1],RINGS[(index+2)]]
    elif index == len(RINGS) - 1: #DB
        return [RINGS[index-2],RINGS[index-1],RINGS[(index)]]
    else:
        return [RINGS[index-1],RINGS[index],RINGS[(index+1)]]

def get_neighbors(target):
    ring,section = get_ring(target),get_section(target)
    if section == None:
        return SECTIONS
    else:
        return [ r+s for r in get_adjacents(ring,RINGS) for s in get_adjacents(section,SECTIONS)]

def get_ring(target):
    if target in ('SB','DB','OFF'):
        return target
    else:
        return target[0]

def get_section(target):
    if target in ('SB','DB','OFF'):
        return None
    else:
        return target[1:]

def prob_test():
    T20 = DandT_miss_prob('T20',0.1)
    assert T20.Prob.topProb == 0.05
    assert T20.Target.zone == 'T'
    assert int(T20.Target.sector) == 20
    S18 = S_miss_prob('S10',0.02)
    assert S18.Prob.prob == 0.004
    SB = Bull('SB')
    assert SB.sector == 'B'
    assert SB.target == 'SB'
    assert SB.zone == 'S'
    SB = B_miss_prob('SB',0.5)
    assert SB.Prob.topProb == 0.375
    assert SB.Prob.bottomProb == 0.125
    #assert SB.Prob.leftProb == SB.Prob.rightProb == 0.25
    DB = B_miss_prob('DB',0.5)
    assert DB.Prob.top1 == 0.49995
    assert get_adjacents('T',RINGS) == ['S','T','S']
    assert get_adjacents('D',RINGS) == ['OFF','D','S']
    assert get_adjacents('20',SECTIONS) == ['5','20','1']
    assert set(get_neighbors('T20')) == set(['T20','T5','T1','S1','S5','S20'])
    assert len(get_neighbors('T20')) == 9
    assert same_outcome(outcome('T20', 0.1), 
                        {'T20': 0.81, 'S1': 0.005, 'T5': 0.045, 
                         'S5': 0.005, 'T1': 0.045, 'S20': 0.09})
    print 'prob tests pass'

def outcome(target, miss):
    "Return a probability distribution of [(target, probability)] pairs."
    target_ring = get_ring(target)
    target_section = get_section(target)
    sections = get_adjacent_sections(target_section) #gets all sections
    rings = get_adjacent_rings(target_ring)
    miss_conversion = {'S':miss/5.0,'DB':miss * 3.0}
    if target_ring in miss_conversion:
        miss = miss_conversion[target_ring]
    ring_prob_dist = {'S':(miss*0.5,1.0-miss,miss*0.5),'D': (miss*0.5,1.0-miss,miss*0.5),'T':(miss*0.5,1.0-miss,miss*0.5),'SB':((1.0 - miss),miss*0.25),'DB':(miss/3,1.0 - miss)} # take this out
    section_prob_dist = {'S':(miss*0.5,1.0-miss,miss*0.5),'T':(miss*0.5,1.0-miss,miss*0.5),'D':(miss*0.5,1.0-miss,miss*0.5)}
    prob_dist = {} 
    ring_probs = ring_prob_dist[target_ring]
    if target_ring in ('SB','DB'):
        section_prob = 1.0 - miss 
        prob_dist['SB'] = round(ring_probs[0] * section_prob,4)
        prob_dist['DB'] = round(ring_probs[1] * section_prob,4)
        remaining_prob = 1.0 - (prob_dist['SB'] + prob_dist['DB'])
        for section in sections:
            prob_dist['S'+section] = round(remaining_prob / 20,4)
    else:
        section_probs = section_prob_dist[target_ring]
        for i,section in enumerate(sections):
            section_prob = section_probs[i]
            for j,ring in enumerate(rings):
                zone = (ring + section) if ring != 'OFF' else 'OFF'
                ring_prob = round(ring_probs[j] * section_prob,4)
                if(ring_prob > 0.0):
                    prob_dist[zone] = ring_prob  + (prob_dist[zone] if zone in prob_dist else 0.0)
    return prob_dist 

def best_target(miss):
    "Return the target that maximizes the expected score."
    ring_scores = {'S':1,'D':2,'T':3,'SB':25,'DB':50,'OFF':0}
    rings = ['S','D','T']
    miss_conversion = {'S':miss/5.0,'DB':miss * 3.0}
    if miss in miss_conversion:
        miss = miss_conversion[miss]

    best_hit = None
    for section in SECTIONS:
        for ring in rings:
            prob_dist = outcome(ring+section,miss)
            probable_score = 0.0
            for target in prob_dist:
                probable_score += prob_dist[target] * ring_scores[get_ring(target)] * int('1' if get_section(target) == None else get_section(target))
            #print score,prob
            if (best_hit is None) or (best_hit[1] < probable_score) :
                best_hit = (ring+section,probable_score)
    #print best_hit[1]
    return best_hit[0]
    
def same_outcome(dict1, dict2):
    "Two states are the same if all corresponding sets of locs are the same."
    return all(abs(dict1.get(key, 0) - dict2.get(key, 0)) <= 0.0001
               for key in set(dict1) | set(dict2))

def test_darts2():
    assert best_target(0.0) == 'T20'
    assert best_target(0.1) == 'T20'
    assert best_target(0.4) == 'T19'
    assert same_outcome(outcome('T20', 0.0), {'T20': 1.0})
    assert same_outcome(outcome('T20', 0.1), 
                        {'T20': 0.81, 'S1': 0.005, 'T5': 0.045, 
                         'S5': 0.005, 'T1': 0.045, 'S20': 0.09})
    assert (same_outcome(
            outcome('SB', 0.2),
            {'S9': 0.016, 'S8': 0.016, 'S3': 0.016, 'S2': 0.016, 'S1': 0.016,
             'DB': 0.04, 'S6': 0.016, 'S5': 0.016, 'S4': 0.016, 'S20': 0.016,
             'S19': 0.016, 'S18': 0.016, 'S13': 0.016, 'S12': 0.016, 'S11': 0.016,
             'S10': 0.016, 'S17': 0.016, 'S16': 0.016, 'S15': 0.016, 'S14': 0.016,
             'S7': 0.016, 'SB': 0.64}))
    assert (same_outcome(outcome('D20',0.4),{'OFF': 0.2, 'D20': 0.36, 'S1': 0.04, 'S5': 0.04, 'S20': 0.12, 'D5': 0.12, 'D1': 0.12}))
    assert (same_outcome(outcome('T20',1.0),{'S1': 0.5, 'S5': 0.5}))
    assert (same_outcome(outcome('S17',0.5),{'D17': 0.045, 'S3': 0.045, 'S2': 0.045, 'T2': 0.0025, 'T3': 0.0025, 'T17': 0.045, 'S17': 0.81, 'D2': 0.0025, 'D3': 0.0025}))
    assert (same_outcome(outcome('DB',0.1),{'S9': 0.022, 'S8': 0.022, 'S3': 0.022, 'S2': 0.022, 'S1': 0.022, 'DB': 0.49, 'S6': 0.022, 'S5': 0.022, 'S4': 0.022, 'S19': 0.022, 'S18': 0.022, 'S13': 0.022, 'S12': 0.022, 'S11': 0.022, 'S10': 0.022, 'S17': 0.022, 'S16': 0.022, 'S15': 0.022, 'S14': 0.022, 'S7': 0.022, 'S20': 0.022, 'SB': 0.07}))
    print 'tests pass'
if __name__ == '__main__':
    test_darts()
    test_darts2()
