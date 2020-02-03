from ukz import *

print("Constructing song object...")
officialName = "Alien Shores"
song = Song()

bass = song.addTrack(44,5,95)
left = song.addTrack(\
	[ (88,4,85), (4,4,85) ])
right = song.addTrack(5,5,110)
numWhistles = 2
whistles = song.addTracks(\
	numWhistles,78,5,100)
numChoir = 4
choir = song.addTracks(\
	numChoir,52,5,110)
shore = song.addTrack(122,0,70)

################

def flowing(pitches,durations,ln):
    mel = Melody()
    for (p,d) in zip(pitches,durations):
        if p is None:
            mel.forward(d)
        else:
            mel.playNote(p,d)
    return mel.stretchTo(ln)
def flow(mel,ps,durs,ln):
    mel.playMelody(flowing(ps,durs,ln))

def leftCatchUpTo(track,mel):
    dt = track.curTime - left.curTime
    for i in range(0,dt//32):
        left.playMelody(mel)
        
def mkLeft(a,b,c,d):
    return shred([a,b,c,a,b,c,d,c]*2,4)
lm1 = \
 mkLeft(0,7,11,12) | \
 mkLeft(1,8,11,12)
lm2 = \
 mkLeft(8,12,15,16) | \
 mkLeft(7,12,15,16)
lm15 = \
 mkLeft(5,8,12,13) | \
 mkLeft(4,8,12,13)
lm4 = \
 mkLeft(8,12,19,20) | \
 mkLeft(7,14,19,20)

bm1 = shred([0,1]).stretched(16)
bm2 = rhythmic(zip(\
	[0,4,0],[8,4,4])) \
	| rhythmic(zip(\
	[1,4,1],[8,4,4]))
bm1_7 = rhythmic(zip(\
	[0,4,0],[8,4,4])) \
	| shred([1]).stretched(16)
	
def choirGoto(t):
    for i in range(0,numChoir):
        choir[i].goto(t)
def choirForward(dt):
    for i in range(0,numChoir):
        choir[i].forward(dt)
def playSingleChoir(i,pitch,dur,fadeIn,fadeOut):
    choir[i].addFadeIn(fadeIn)
    choir[i].playNote(pitch,dur)
    choir[i].addFadeOut(-fadeOut)
def playchoir1(a,b,c,atEnd=False,xtra=False):
    t = choir[0].curTime
    for i in range(1,numChoir):
        if choir[i].curTime != t:
            raise ValueError(f"choir{i} not in sync with choir[0]")
    playSingleChoir(0,a,20,0,8)
    choir[1].forward(8)
    playSingleChoir(1,b,20,0,8)
    dur3 = 32 if atEnd and not xtra else 20
    fade3 = 12 if atEnd and not xtra else 8
    choir[2].forward(16)
    playSingleChoir(2,c,dur3,0,fade3)
    if xtra:
        dur3 = 32 if atEnd else 20
        fade3 = 12 if atEnd else 8
        choir[3].forward(24)
        playSingleChoir(3,c-1,dur3,0,fade3)
    # all choirs must have moved by 32
    choirGoto(t+32)
    
def whistle1(windex,trans,linger=0,inclHigh=False):
    m = Melody()
    m.curLoudness = fortissimo
    m.forward(4)
    m.playNote(8,4)
    flow(m,\
    	[20,19,18,17], \
    	[34,2,2,2], 8)
    m.playNote(16,linger + 7)
    if inclHigh:
        m = m & \
         m.translated(12)\
         .louded(piano)
    m.translate(trans)
    w = whistles[windex]
    w.addFadeIn(0)
    w.playMelody(m)
    w.addFadeOut(-3)
    w.forward(9-linger)
def whistle2(windex,trans,hi,dim=False,inclHigh=False):
    m = Melody()
    m.curLoudness = fortissimo
    m.forward(4)
    m.playNote(20 if hi else 17,4)
    if dim:
        flow(m,\
        	[8,9,10,11,12,13,14], \
        	[9] + [1]*6, 8)
    else:
        flow(m,\
        	[8,9,10,11,12,13,14,15], \
        	[9] + [1]*7, 8)
    m.playNote(15 if dim else 16,7)
    if inclHigh:
        m = m & \
         m.translated(12)\
         .louded(piano)
    m.translate(trans)
    w = whistles[windex]
    w.addFadeIn(0)
    w.playMelody(m)
    w.addFadeOut(-3)
    w.forward(9)
    
################
# Intro

bass.forward(16)
shore.addFadeIn(24)

bass.playMelody(bm1)
bass.playMelody(bm2)

left.goto(bass)

bass.playMelody(bm2)
bass.playMelody(bm1_7)
bass.forward(32)

leftCatchUpTo(bass,lm1)

shore.goto(left)
shore.addFadeOut(-16)

################
# Normal 0 to 1

song.goto(left)

for i in range(0,4):
    left.playMelody(lm1)
    
rm1 = ukz("""
  (CEGB)/2 .*5/2
  (gCEF#) *9 ..
  [F# G F#*4] % 2
  (g#C#E)/2 .*5/2
  (g#C#D#) *5
  [.*4 E*4 D#*3 .]%4
""")
    
#rm1 = Melody()
#rm1.playChord([12,16,19,23],"1/2",None,3)
#rm1.playChord([7,12,16,18],9)
#rm1.forward(2)

#rm1.playMelody(shred([18,19,18])\
#	.rhythmized([1,1,4])
#	.stretchedTo(2))
#
#rm1.playChord([8,13,16],"1/2",-1,3)
#rm1.playChord([8,13,15],5)
#rm1.forward("4/3")
#rm1.playNote(16,"4/3")
#rm1.playNote(15,"3/3")
#rm1.forward("1/3")
rm1.playNote(15,"1/3")
rm1.playNote(16,"1/3")
rm1.playNote(15,"2/3")
rm1.playNote(13,"4/3")
rm1.playNote(8,"4/3")
#
rm1.playNote(11,"1")
rm1.playNote(12,"3/2")
rm1.forward("1/2")
rm1.playNote(12,"1/3")
rm1.playNote(14,"1/3")
rm1.playNote(16,"17/3")
rm1.playNote(19,"4/3")
rm1.playNote(18,"3/3")
rm1.forward("1/3")
rm1.playNote(18,"1/3")
rm1.playNote(19,"1/3")
rm1.playNote(18,"2/3")
rm1.playNote(16,"4/3")
rm1.playNote(15,"4/3")
#
rm1.playNote(16,"1/3")
rm1.playNote(18,"1/3")
rm1.playNote(20,"22/3")
rm1.forward("3/3")
flow(rm1, \
	[23,22,21,20,19,18,17,16,15,14], \
	[35] + list(range(25,0,-1)), \
	7)
rm1.playNote(13,3)
rm1.playNote(12,"39/6",None,"7/3")
rm1.playNote(16,"25/6",None,"1/3")
rm1.playNote(19,"23/6",None,"1/3")
rm1.playNote(23,"21/6")
flow(rm1, \
 [24,23,20,23,20,19,20,19], \
 [6,6,4,4,4,3,3,3], "13/2")
flow(rm1, \
 [17,16,15,16,15], \
 [9,7,1,1,9], 9)
flow(rm1, \
 [None] + list(range(13,23)), \
 [10,10,6,6,6,5,5,5,5,4,4,4], 7)
rm1.playNote(23,"8/3")
rm1.playNote(21,"1/3")
rm1.playNote(23,"1/3")
rm1.playNote(21,"8/3")
rm1.playNote(19,2)
rm1.forward(1)
rm1.playNote(24,"30/5",None,"2/5")
rm1.playNote(23,"28/5",None,"2/5")
rm1.playNote(19,"26/5",None,"2/5")
rm1.playNote(16,"24/5",None,"24/5")
flow(rm1,[15,14],[1]*4,1)
rm1.playNote(13,"5/3",None,2)
rm1.playNote(13,"1/3")
rm1.playNote(14,"1/3")
rm1.playNote(13,"22/3")

right.playMelody(rm1)
whistles[0].playMelody(rm1)

################
# Drama 1

song.goto(left)
shore.addFadeIn(-16)

whistle1(0,0)
whistles[1].forward(16)
whistle1(1,4)
left.playMelody(lm15)

for w in whistles:
    w.goto(left)
whistle2(0,0,False,False)
whistles[1].forward(16)
whistle2(1,4,True,False)
left.playMelody(lm15)

bass.goto(left)
bass.curLoudness = mezzopiano
bass.playChord([5,8],16)
bass.playChord([4,8],8)
bass.playChord([4,10],8)
bass.playChord([5,8],16)
bass.playChord([4,8],8)
bass.playChord([4,10],4)
bass.playChord([4,8],4)

for w in whistles:
    w.goto(left)
whistle1(0,0)
whistles[1].forward(16)
#whistle1(1,4)
left.playMelody(lm15)
	
for w in whistles:
    w.goto(left)
whistle2(0,0,False,False)
whistles[1].forward(16)
whistle2(1,4,True,True)
left.playMelody(lm15)

################
# Normal 1 to 2

song.goto(left)

bass.curLoudness = mezzopiano
for i in range(0,3):
    bass.playChord([0,7],8)
    bass.playChord([4,11],4)
    bass.playChord([0,7],4)
    bass.playChord([1,8],8)
    bass.playChord([4,11],4)
    bass.playChord([1,8],4)
bass.playChord([0,7],8)
bass.playChord([4,11],4)
bass.playChord([0,7],4)
bass.playChord([1,8],16)
    
right.forward(64)
right.curLoudness = fortissimo
right.addNote(0,16)
right.addNote(12,16,)
right.forward(32)
right.addNote(19,16)
right.addNote(7,16)
right.forward(16)
right.addNote(20,16)
right.addNote(8,16)
    
for i in range(0,4):
    left.playMelody(lm1)

    
################
# Drama 2

song.goto(left)
shore.forward(8)
shore.addFadeOut(-16)

playchoir1(8,20,19)
playchoir1(8,20,19)
for i in range(0,2):
    left.playMelody(lm2)

choirForward(32)
bass.goto(left)
bass.playChord([8],8)
bass.playChord([8,12],"9/3")
bass.playChord([8,12],"9/3")
bass.playChord([8,14],"6/3")
bass.playChord([7,12],8)
highL = (piano+mezzopiano)/2
bass.addChord([19],8,highL)
bass.playChord([7,12],8)

playchoir1(8,20,19,True)
bass.playChord([8,12,20],8)
bass.playChord([8,12,20],4)
bass.playChord([8,14,18],4)
bass.addChord([7,19],16)
bass.playChord([12],24)

for i in range(0,2):
    left.playMelody(lm2)
    
################
# Normal 2 to 3

song.goto(left)
shore.addFadeIn(-16)

for i in range(0,4):
    left.playMelody(lm1)

whistles[0].forward(48)
whistle1(0,0,4)
whistles[1].forward(80)
whistle1(1,3,4)

################
# Drama 3

song.goto(left)
shore.addFadeOut(-32)
bass.curLoudness = mezzopiano

bass.playChord([8],8)
bass.playChord([8,12],8)
bass.playChord([7,14],8)
bass.playChord([11],4)
bass.playChord([7],4)
choirForward(32)

playchoir1(8,20,19)
bass.forward(32)

bass.playChord([8],8)
bass.playChord([8,12],"9/3")
bass.playChord([8,14],"9/3")
bass.playChord([8,15],"6/3")
bass.playChord([7,14],16,None,8)
highL = (piano+mezzopiano)/2
bass.playChord([19],8,highL)
choirForward(32)

playchoir1(8,20,19,True,True)
bassT = bass.curTime
bass.playChord([8],16)
bass.playChord([7],16)
bass.curTime = bassT
bass.curLoudness = highL
bass.playChord([15,20],16)
bass.playChord([14,19],16)

for i in range(0,4):
    left.playMelody(lm4)
    
################
# Outro

song.goto(left)
shore.addFadeIn(-32)

bass.curLoudness = mezzoforte

outroT = bass.curTime
bass.curLoudness = highL
for i in range(0,4):
    bass.playChord([24],16)
    bass.playChord([25],16)
    
bass.curTime = outroT
bass.curLoudness = mezzoforte
for i in range(0,3):
    bass.playChord([0,7,12],8)
    bass.playChord([3,10,12],4)
    bass.playChord([0,7,12],4)
    bass.playChord([1,8,13],8)
    bass.playChord([4,11,13],4)
    bass.playChord([1,8,13],4)
for i in range(0,1):
    bass.playChord([0,7,12],8)
    bass.playChord([3,10,12],4)
    bass.playChord([0,7,12],4)
    bass.playChord([1,8,13],8)
    bass.playChord([1,8,13],8)

choirForward(48)
playchoir1(8,20,19,False,True)
choirForward(32)
playchoir1(8,20,19,False,False)

for i in range(0,4):
    left.playMelody(lm1)

shore.goto(left)
shore.forward(48)
shore.addFadeOut(-48)
finalTime = shore.curTime

################
# All the shores

shoreInitPitch = 24
shoreFinalPitch = 48

shorePitchInc = -1 if shoreFinalPitch < shoreInitPitch else 1
shore.goto(0)
numShores = (shoreFinalPitch - shoreInitPitch)*shorePitchInc + 1
shoreDt = finalTime / numShores
for i in range(0,numShores):
    timeFrac = i / numShores
    shoreTime = timeFrac * finalTime
    shorePitch = i*shorePitchInc + shoreInitPitch
    shore.playNote(shorePitch,shoreDt)

################

bass.choirize()

print("Writing song file...")
song.write(216,officialName)
