# Ultrakazoid

Ultrakazoid (UKZ for short) is a library, including a melody-building language, for writing music in the form of MIDI files.


# How I use it:

* With qpython3 on Android
* With CodeBoard keyboard on Android (I've designed the ukz-language to make it convenient specifically for this keyboard)
* Song scripts should go in the same folder where "ukz" folder is. (exception for sit_scripts, test_scripts.py handles directories properly)
* Running the song script should work.
* Result will be a Midi file in a folder called AMidi, in the same folder as qpython3 in the phone

# Quick Architecture

## ukz/interface

The song-building stuff (on top of the melody-building stuff) required to actually build a whole song with several tracks.
See sit_scripts folder for examples.

In the Song constructor, the string you pass must be in the skz language (ukz/ukzlang/skzgrammar.py), which makes a SongConfig object.

Then repeatedly call song.play(s) where each string s is in ukz language (ukz/ukzlang/ukzgrammar.py) representing a multi-track melody.
These melodies will be concatenated in the end (played sequentially).

## ukz/melody, ukz/ukzlang/hmel.py

These stand for "hierarchical melody" and "flat melody".

A flat melody has the following properties:
* Start and end time (or duration)
* A list of notes
    * Each note has a pitch (which piano key the player presses), a "loudness" (linked to MIDI velocity, which means how fast the player's finger is going when he hits the piano key), a start time (when the player presses the piano key) and a duration (how long he keeps it pressed for).
* A list of gradients. Often used kinds are: Volume gradients (e.g. for fade-in and fade-out) and Pitch bends (very relevant for guitar soloists bending the strings)

Hmel is a tree-representation of a melody, used only in the ukz melody-building language.
Each leaf is either a note (with a pitch, loudness, and duration, but no start or end times because these will be derived from the leaf's position within the tree) or a rest (same as a note but without the pitch and loudness, it's just silence)
Then there are nodes:
* HmelSeq (sequence) has a list of child melodies. These children will be played one after the other. In ukz, use square brackets with melodies inside to play sequentially: [ c e g ]
* HmelPar (parallel) has a list as well, but they will all start playing at the same time. In ukz, use round brackets with melodies inside to play in parallel: ( c e g )

There's also the concept of pipes, which sets the start/end time(s) of a melody and adds the capability to add stuff before the start and after the end of that melody. This is useful if you want a "lead-up" to a melody but you need the start of it to be after the first few notes. Hmel stores these children in separate lists.
* HmelSeq will play the pre-children sequentially, then children, then post-children sequentially.
* HmelPar will play the pre-children all ending at time 0 (relatively speaking) then the children all starting at this same time 0. If you want several parallel lead-ups, use this pipe in a HmelPar.

## ukz/songconfig

A SongConfig object tells you how ukzlang code translates into actual midi stuff. Like what instrument each channel plays, what volumes and velocities will be played, etc.

## ukz/midi

This is all code directly related to MIDI writing. As of April 2021 I'm dealing with all the byte logic myself without an external library.

## ukz/uklr,ukz/ukzlang

uklr is general parser code (not necessarily ukz-specific) that I wrote. The ukz and skz parsers makes good use of the stuff in here.

## test_ukz

These are unit tests... sort of. Their scope is pretty wide, no mocking or anything, they're more like integration tests maybe.

test_ukz/test_scripts: These run the scripts in sit_scripts folder, and check that the output midi file matches those in good_midi_files folder. If these pass then the engine is probably doing ok.

## utils

Yeah, obviously this is random utilities. Useful code used elsewhere.

## ukz_ut_run.py

Run main from here: it runs all the tests from test_ukz (UT and script tests).

