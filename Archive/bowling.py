"""
UNIT 1: Bowling:

You will write the function bowling(balls), which returns an integer indicating
the score of a ten-pin bowling game.  balls is a list of integers indicating 
how many pins are knocked down with each ball.  For example, a perfect game of
bowling would be described with:

    >>> bowling([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10])
    300

The rules of bowling are as follows:

(1) A game consists of 10 frames. In each frame you roll one or two balls,
except for the tenth frame, where you roll one, two, or three.  Your total
score is the sum of your scores for the ten frames.
(2) If you knock down fewer than ten pins with your two balls in the frame,
you score the total knocked down.  For example, bowling([8, 1, 7, ...]) means
that you knocked down a total of 9 pins in the first frame.  You score 9 point
for the frame, and you used up two balls in the frame. The second frame will
start with the 7.
(3) If you knock down all ten pins on your second ball it is called a 'spare'
and you score 10 points plus a bonus: whatever you roll with your next ball.
The next ball will also count in the next frame, so the next ball counts twice
(except in the tenth frame, in which case the bonus ball counts only once).
For example, bowling([8, 2, 7, ...]) means you get a spare in the first frame.
You score 10 + 7 for the frame; the second frame starts with the 7.
(4) If you knock down all ten pins on your first ball it is called a 'strike'
and you score 10 points plus a bonus of your score on the next two balls.
(The next two balls also count in the next frame, except in the tenth frame.)
For example, bowling([10, 7, 3, ...]) means that you get a strike, you score
10 + 7 + 3 = 20 in the first frame; the second frame starts with the 7.

"""
FRAMES = 10

def bowling(balls,debug=False):
    "Compute the total score for a player's game of bowling."
    score = 0
    index = 0 # tracks where does the next frame start
    frame = 1
    while(frame <= FRAMES):
        frame_score,increment = score_frame(index,balls)
        if debug:
            print 'frame_score:%s increment:%s' %(frame_score,increment)
        score += frame_score 
        index += increment # increment returns a value for the number of balls in the previous frame. It could be '1' for a strike or '2' for a normal throw 
        frame += 1
    return score

def score_frame(index,balls):
    frame_score = 0
    increment = 2

    if isStrike(index,balls):
        #strike is tricky because strike can happen in a bowler's first attempt or second. The score could be [10] or [0,10]. Hence the ball counting logic and increment logic should vary.
        for i in range(index,scoring_balls(index,balls,'3 if balls[index] == 10 else 4')):
            frame_score += balls[i]
        increment = 1 if balls[index] == 10 else 2
    elif isSpare(index,balls):
        for i in range(index,scoring_balls(index,balls,'3')):
            frame_score += balls[i]
    else: # normal throw
        for i in range(index,scoring_balls(index,balls,'2')):
            frame_score += balls[i]
    return frame_score,increment

def scoring_balls(index,balls,expr):# returns the number of balls that should be scored.Say, may score additional 2 balls and spare may score additional 1 ball etc..
    return min(index+eval(expr),len(balls))

def isStrike(index,balls):
    return balls[index] == 10
    '''for i in range(index,scoring_balls(index,balls,'2')):
        if balls[i] == 10:#strike can happen in either one of the balls
            return True
    return False'''

def isSpare(index,balls):
    spare_score = 0
    for i in range(index,scoring_balls(index,balls,'2')):
        spare_score += balls[i]
    return spare_score == 10

def test_bowling():
    assert   0 == bowling([0] * 20)
    assert  20 == bowling([1] * 20)
    assert  80 == bowling([4] * 20)
    assert 190 == bowling([9,1] * 10 + [9])
    assert 300 == bowling([10] * 12)
    assert 200 == bowling([10, 5,5] * 5 + [10])
    assert  11 == bowling([0,0] * 9 + [10,1,0])
    assert  12 == bowling([0,0] * 8 + [10, 1,0])
    assert 168 == bowling([9, 1, 0, 10, 10, 10, 6, 2, 7, 3, 8, 2, 10, 9, 0, 9, 1, 10])
    print 'tests pass'

def test_unit():
    assert 60 == bowling([3]*20)
    assert 67 == bowling([8,2] + [3]*18)
    assert 70 == bowling([10] + [3]*18)
    assert 147 == bowling([8,2]*2 + [7]*16)
    assert 190 == bowling([9,1] * 10 + [9])
    print 'unit tests pass'

if __name__ == '__main__':
    #test_unit()
    test_bowling()
