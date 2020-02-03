# Ultrakazoid

Ultrakazoid (UKZ for short) is a library, including a melody-building language, for writing music in the form of MIDI files.


# How I use it:

* With qpython3 on Android
* With CodeBoard keyboard on Android (I've designed the ukz-language to make it convenient specifically for this keyboard)
* In qpython3, I installed midiutil library (using pip install)
* A folder should have the ukz folder AND a song script (where songtemplate.py is)
* A folder called AMidi should be in the same folder as qpython3 in the phone
* Running the song script should (hopefully?) work. Try running songtemplate.py to see.

# Quick Architecture

## ukengine

This shouldn't be called ukengine, but it's the song-building stuff (on top of the melody-building stuff) required to actually build a whole song with several tracks.
See songtemplate.py for an example song that uses the classes here.

Instr is pretty much a setting for a MIDI track. Which program (instrument, just say a portion of a name of a MIDI program and it should work), how many octaves to shift up (because you don't want to constantly have to tell it to "shift by 4 octaves" on a track's melodies), what the volumes and loudnesses are.
(Volume means the volume you can set with a knob somewhere. "Loudness" is a term I made up, it's directly linked to the "velocity" in MIDI-speak, which means how fast was your finger going when you hit the piano key.)
The volumes/velocities are specified by a dictionary in the Instr constructor. Here's what the value with each kind of key means:
* key = None: the volume of the track (from 0 to 127, default is 96 I think)
* key = (number,number): the velocity when you play this pitch at this loudness
* key = a number: the velocity for that loudness (for all pitch numbers)
Whatever velocities aren't specified will be linearly interpolated between the nearest specified loudness values.


## Hmel, Melody

These stand for "hierarchical melody" and "flat melody".

A flat melody has the following properties:
* Start and end time (or duration)
* A list of notes
    * Each note has a pitch (which piano key the player presses), a "loudness" (linked to MIDI velocity, which means how fast the player's finger is going when he hits the piano key), a start time (when the player presses the piano key) and a duration (how long he keeps it pressed for).
* Lists of gradients (currently 2 lists as of February 2020)
    * Each list has gradients of a different kind. The 2 current kinds are: Volume gradients (e.g. for fade-in and fade-out) and Pitch bends (very relevant for guitar soloists bending the strings)

Hmel is a more complex tree-representation of a melody. It more closely matches the structure of the ukz melody-building language.
Each leaf is either a note (with a pitch, loudness, and duration, but no start or end times because these will be derived from the leaf's position within the tree) or a rest (same as a note but without the pitch and loudness, it's just silence)
There are different kinds of nodes:
* HmelSeq (sequence) has a list of child melodies. These children will be played one after the other. Each node (including leaves) has a length so that its parent can figure out how long "after" to play the next child. In ukz, use square brackets with melodies inside to play sequentially: [ c e g ]
* HmelPar (parallel) has a list as well, but they will all start playing at the same time. In ukz, use round brackets with melodies inside to play in parallel: ( c e g )
* HmelRep is like a specialized case of HmelSeq where the same child is repeated to make the list of children.

There's also the concept of pipes, which sets the start/end time(s) of a melody and adds the capability to add stuff before the start and after the end of that melody. This is useful if you want a "lead-up" to a melody but you need the start of it to be after the first few notes. Hmel stores these children in separate lists.
* HmelSeq will play the pre-children sequentially, then children, then post-children sequentially.
* HmelPar will play the pre-children all ending at time 0 (relatively speaking) then the children all starting at this same time 0. If you want several parallel lead-ups, use this pipe in a HmelPar.

## midi

This is all code directly related to MIDI.
* drumpitch.py: how your letters map to MIDI pitch numbers (part of it anyway. You also need to look at uklang/pitchdecoder.py)
* limits.py: Minima and maxima for things like pitch numbers, duration, etc.
* midinote.py: Not very much in here, but it's necessary.
* programs.py: 2 lists of all MIDI programs: one for drums, one for normal instruments.
* trackroute.py: A track route is essentially a pair (tracknumber, channelnumber). This file generates new pairs for each track in a song.
* writer.py has stuff to actually write a MIDI file

## uklr,uklang

uklr is general parser code (not necessarily ukz-specific) that I wrote. The ukz parser makes good use of the stuff in here.
I should write a document just to describe how this works... but I don't feel like it right now.
uklang is the ukz parser. The file interface.py has 
* states.py has an enum, with all the kinds of tokens and parse nodes there can be.
* tokenrules.py takes the input string, turns it into a stream of tokens.
* parserules.py takes the tokens, applies parse rules and on-the-fly traverses the parse tree to output the Hmel that the code represents.
* pitchdecoder.py says how to turn the letters in the code (a to g, and more for drums) into pitch numbers.
* melodyopmap.py says what the operators mean in the ukz language (maps ukz-language operator symbols to functions in the code).
* interface.py has the functions you will call from a song script (like songtemplate.py is doing).

## ukut

These are unit tests... sort of. Their scope is pretty wide, no mocking or anything, they're more like integration tests maybe.

test_uk_blah: Test the ukz and ukd functions, which parse ukz-code to output flat melodies.
test_pat: Test the pattern-matching functionality (in uklr/pat.py, used for regex-style parsing rules).

## utils

Yeah, obviously this is random utilities. Useful code used elsewhere.

## ukt.py

If you import this and call ukztest, you can quickly generate a one-track song, just for testing or something.

## ukz_ut_run.py

Run main from here: it runs all the "unit" tests from ukz/ukut.

