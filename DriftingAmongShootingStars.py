from midiutil import *
from ukz import *
from random import *

################################

# for FluidR3

rainprog = 4

officialName = \
 f"FluidR3_DASS"
song = Song()

# (82,100,36) was good too
# (48,60,36) was good too
# (33,80,24) was good too.
# not sustained though but good
# (58,100,24) was kind of good
actualbass = song.addTrack(\
	Instrument({"": [\
	MidiInstrument(44,3,[45]*9),\
	MidiInstrument(45,2,[50]*9) \
	,MidiInstrument(33,2,70)\
	#,MidiInstrument(33,1,70)
	]}))

# (4,100,36) is good!
bass = song.addTrack(\
	Instrument({"":\
	[MidiInstrument(4,3,100),\
	MidiInstrument(5,3,80)\
	]}))

# (2,100,72) is good, 
# sounds kind of like Google Play!
# 5/8 are kind of good,
# but 2 is better i think.
# (10/11/98,100,84) are kind of good,
# but 2 is better i think.
# 4 is good, but there's no kick to it.
# 2 and 4 are both good.
rain = song.addTrack(\
	Instrument({"": [\
	MidiInstrument(4,6,[110]*7 + [120]*2),\
	#MidiInstrument(4,7,[110]*9),\
	MidiInstrument(2,6,[30]*7 + [60]*2),\
	MidiInstrument(5,6,[90]*8)\
	#MidiInstrument(8,6,[100]*8)\
	]}))
	
# either (44,90,60) or (44,90,48) is good
# but with pitch 48 i barely hear the soprano
# maybe have volume below 90
# so you don't drown out the rain.
# ok (44,85,60) is good!
choir = song.addTrack(\
	Instrument({"":\
	[MidiInstrument(44,5,[80]*8)\
	,MidiInstrument(52,5,[60]*8)\
	]}))

# (5,90,72): I can't hear it!
# (4,100,84) is good!
bell = song.addTrack(\
	Instrument({"":\
	[MidiInstrument(4,7,[100]*8)]}))

#####################################

bassLines = [
 translateChord(\
 [0,5,7,10,14,10,7,5,\
  0,5,7,10,-2,5,8,10,\
  -4,2,3,7,10,7,3,2,\
  -4,2,3,7,-2,2,3,10], 12), \
 translateChord(\
	[0,10,14,15,17,15,14,10,\
  0,10,14,15,-2,10,14,15,\
  -4,7,8,12,15,14,12,10,\
  -4,7,8,12,-2,7,8,14], 12), \
 translateChord(\
 [0,7,11,12,14,12,11,7,\
  0,7,11,12,-5,7,11,12,\
  -7,7,11,12,14,12,11,7,\
  -7,7,11,12,-5,7,11,12], 15),\
 translateChord(\
 [0,7,11,12,14,12,11,7,\
  0,7,11,12,0,7,11,12], 15)
   ]


def playBass1(pitches,playAll=False):
    durs = [8,7,6,5] + [4,3,3,3]*3
    durs = durs*2
    i = 0
    for (p,dur) in zip(pitches,durs):
        i16 = i%16
        if i16<=3 or i16>=8 or playAll:
            bass.addNote(p,dur)
        bass.forward(1)
        i = i+1
def playActualBass(pitches,playAll=False):
    pis = [0,8,12,16,24,28]
    durv = iter([8,4,4]*2)
    #durv = Cyclev([8,4,4])
    lp = len(pitches)
    for pind in pis:
        if pind>=lp:
            return
        p = pitches[pind]
        dur = next(durv)
        actualbass.playNote(p,dur)
        
def playBassLine(\
	lineIndex,\
	playAll=False):
    actualbass.curTime = bass.curTime
    playActualBass(\
    	bassLines[lineIndex],\
    	playAll)
    playBass1(\
    	bassLines[lineIndex],\
    	playAll)
    	

def playRain1(transIndices):
    scale = Scale([0,2,3,5,7,8,10])
    durs = [8,4,4,16]
    inds = [7,4,5,2]
    for (dur,ind) in zip(durs,inds):
        for t in transIndices:
            p = scale[ind+t]
            rain.addNote(p,8)
        rain.forward(dur)
def playRainTriple(scaleIndices,transIndices):
    scale = Scale([0,2,3,5,7,8,10])
    durs = ["1/2","1/2",31]
    for (dur,ind) in zip(durs,scaleIndices):
        if ind:
            for t in transIndices:
                p = scale[ind+t]
                rain.addNote(p,8)
        rain.forward(dur)
def playRain15(transIndices):
    playRainTriple([7,11,14],transIndices)
def playRain2(transIndices):
    scale = Scale([0,2,3,5,7,8,10])
    inds = [7,4,6,3,5,4,1,2,4,1,3,0,2,-1,1,2,0]
    for ind in inds:
        for t in transIndices:
            p = scale[ind+t]
            rain.addNote(p,8)
            rain.forward(1/2)
            rain.addNote(p+12,8)
        rain.forward(1/2)
    rain.forward(15)
def playRain25(transIndices):
    playRainTriple([7,11,16],transIndices)
def playRain3():
    rais1 = [0,7,11,12,14,7,16,12,\
     17,16,12,19,17,16,14,12]
    rais2 = [0,7,11,12,14,7,16,12,17,16,14,12,11,14,12,19]
    raim1 = [7,12,19,19,19,14,19,19,24,24,19,24,24,24,19,19]
    raim2 = [7,12,19,19,19,14,19,19,24,24,19,19,19,19,19,24]
    rains = zip(rais1+rais2,raim1+raim2)
    dur = 4
    for (a,b) in rains:
        bell.curTime = rain.curTime
        bell.addNote(a-9,dur)
        bell.forward(1)
        rain.addNote(a-9,dur)
        rain.forward("1/3")
        rain.addNote(b-9,dur)
        rain.forward("1/3")
        rain.addNote(a+3,dur)
        rain.forward("1/3")
def playRain4():
    rais1 = [12,11,9,7,9,7,5,4,7,5,4,2,5,4,2,0]
    rais1 = translateChord(rais1,12)
    rais2 = [0,7,11,12,14,7,16,12,17,16,14,12,11,14,12,19]
    raim1 = [19,19,12,12,12,12,12,12,12,12,7,7,7,7,7,7]
    raim2 = [7,12,19,19,19,14,19,19,24,24,19,19,19,19,19,24]
    dur = 4
    
    rains = zip(rais1+rais2,raim1+raim2)
    for (a,b) in rains:
        bell.curTime = rain.curTime
        bell.addNote(a-9,dur)
        bell.forward(1)
        rain.addNote(a-9,dur)
        rain.forward("1/3")
        rain.addNote(b-9,dur)
        rain.forward("1/3")
        rain.addNote(a+3,dur)
        rain.forward("1/3")
def playRain5(pitches):
    durs = ["1/3","1/3","94/3"]
    for (dur,p) in zip(durs,pitches): 
        rain.addNote(p,16)
        rain.forward(dur)

def legTims(tims,ln):
    baset = -2
    lastt = -2
    for t in tims:
        if baset>=0:
            if t > lastt+1:
                yield (baset,lastt-baset+1)
                baset = t
                lastt = baset
            else:
                lastt = t
        else:
            baset = t
            lastt = baset
    if baset>=0 :
        yield (baset,lastt-baset+1)
        
def shredLegato(track,chords,ln):
    numcd = len(chords)
    # ln = time for one beat
    m = {}
    tim = 0
    for cd in chords:
        for p in cd:
            ts = m.get(p,None)
            if ts:
                ts.append(tim)
            else:
                m[p] = [tim]
        tim = tim + 1
    baset = track.curTime
    for (p,tims) in m.items():
        ts = list(legTims(\
        	tims,numcd))
        for (t,d) in ts:
            tt = baset + ln*t
            dd = d*ln
            track.curTime = tt
            #print(p,',',tt,',',dd)
            track.addNote(p,dd)
    return 4
    
def chordDescend(pitches,steps):
    n = len(pitches)
    ret = []
    for s in steps:
        n = n-s
        r = []
        for i in range(0,n):
            r.append(pitches[i])
        ret.append(r)
    return ret

#####################################
# Play the song

playBassLine(0,False)
playBassLine(0,False)
song.goto(bass)

playBassLine(0,False)
playRain1([0])
playBassLine(0,False)
playRain1([2])
song.goto(bass)

playBassLine(0,True)
playRain15([0])
playBassLine(0,True)
playRain15([2])
song.goto(bass)

################

playBassLine(1,False)
playRain1([0])
playBassLine(1,False)
playRain1([0,2])
song.goto(bass)

playBassLine(1,True)
playRain15([0])
playBassLine(1,True)
playRain15([2])
song.goto(bass)

playBassLine(1,True)
playRain2([0])
playBassLine(1,True)
playRain2([2])
song.goto(bass)

playBassLine(1,True)
playRain25([0])
playBassLine(1,True)
playRain25([2])
song.goto(bass)

################

playBassLine(2,False)
playRain1([2])
playBassLine(2,False)
playRain1([4])
song.goto(bass)

playBassLine(2,True)
playRain1([3])
song.goto(bass)

playBassLine(2,True)
playRain25([2])

shredLegato(choir, [ \
	 [3],\
	 [3,7],\
	 [3,7,10],\
	 [2,5,10,14],\
	 [3,7,10,15],\
	 [3,7,10,19],\
	 [3,8,10,20],\
	 [3,5,10,14,22],\
	 \
	 [3,7,10,15],\
	 [3,7,10,15],\
	 [3,7,10,15],\
	 [-2,2,8,14],\
  [-4,8,12,15],\
  [-4,8,12,15],\
  [-4,8,12,15],\
  [-2,2,10,14,17],\
  \
  [3,7,10,15,19],\
	 [3,7,10,15,19],\
	 [3,7,10,15,17],\
	 [-2,2,8,14,17],\
  [-4,3,8,12,15,20],\
  [-4,3,8,12,15,20],\
  [-4,3,8,12,15,19],\
  [-2,2,10,14,20],\
  \
  [3,7,10,15,22],\
	 [3,7,10,15,20],\
	 [3,7,10,15,19],\
	 [-2,2,8,14,17],\
  [-4,8,12,15,20],\
  [-4,8,12,15,19],\
  [-4,8,12,15,20],\
  [-2,2,10,14,22],\
  \
  [3,7,10,15,19,27],\
	 [3,7,10,15,20,26],\
	 [3,7,10,15,19,24],\
	 [-2,2,8,14,17,22],\
  [-4,8,12,15,20,24],\
  [-4,8,12,15,19,22],\
  [-4,8,12,15,20,24],\
  [-2,3,10,14,17,22,26],\
  \
  ] + chordDescend(\
   [3,10,14,15,22,26,27],\
   [0,1,1,0,1,1,1,0]) \
 , 4)

song.goto(bass)

rain.curLoudness = fortissimo

for k in range(0,2):
    playBassLine(2,True)
    playRain3()

song.goto(bass)

for k in range(0,2):
    playBassLine(2,True)
    playRain4()

song.goto(rain)

playBassLine(3,False)

#bass.addNote(3,16)
bell.curTime = rain.curTime
bell.addNote(15,16)
bell.forward(16)
playRain5([15,22,27])
playBassLine(3,False)

#rain.forward(16)

song.goto(rain)

bass.addNote(3,16)
bass.forward(16)
bell.addChord([15],16)
bell.forward(16)
playRain5([15,22,27])

tempo = 200
songLength = rain.curTime \
 * 60 / tempo
    
song.write(tempo,officialName)
