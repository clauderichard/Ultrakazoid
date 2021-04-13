
# class DrumPitchMidi:

#     highQ = 27
#     slap = 28
#     scratchPush = 29
#     scratchPull = 30
#     sticks = 31
#     squareClick = 32
#     metronomeClick = 33
#     metronomeBell = 34
#     acousticBassDrum = 35
#     bassDrum1 = 36
#     sideStick = 37
#     acousticSnare = 38
#     handClap = 39
#     electricSnare = 40
#     lowFloorTom = 41
#     closedHiHat = 42
#     highFloorTom = 43
#     pedalHiHat = 44
#     lowTom = 45
#     openHiHat = 46
#     lowMidTom = 47
#     hiMidTom = 48
#     crashCymbal1 = 49
#     highTom = 50
#     rideCymbal1 = 51
#     chineseCymbal = 52
#     rideBell = 53
#     tambourine = 54
#     splashCymbal = 55
#     cowbell = 56
#     crashCymbal2 = 57
#     vibraslap = 58
#     rideCymbal2 = 59
#     hiBongo = 60
#     lowBongo = 61
#     muteHiConga = 62
#     openHiConga = 63
#     lowConga = 64
#     highTimbale = 65
#     lowTimbale = 66
#     highAgogo = 67
#     lowAgogo = 68
#     cabasa = 69
#     maracas = 70
#     shortWhistle = 71
#     longWhistle = 72
#     shortGuiro = 73
#     longGuiro = 74
#     claves = 75
#     hiWoodBlock = 76
#     lowWoodBlock = 77
#     muteCuica = 78
#     openCuica = 79
#     muteTriangle = 80
#     openTriangle = 81
#     shaker = 82
#     jingleBell = 83
#     bellTree = 84
#     castanets = 85
#     muteSurdo = 86
#     openSurdo = 87

################################################

class DrumPitchUkz:
        
    ################################
    # Overlaps with piano letters

    cymbal1 = 0 # c
    cymbal2 = 1 # c^
    floorTom1 = 5 # f
    floorTom2 = 6 # f^
    gong = 7 # g
    splashCymbal = 8 # g^
    bassPedal = 11 # b

    ################################

    snare = 1024
    
    hiHatClosed2 = 2026
    hiHatClosed = 2027
    hiHatOpen = 2028
    
    rideCymbal1 = 3041
    rideCymbal2 = 3042
    rideBell = 3043
    cowbell = 3044
    
    tom1 = 4045
    tom2 = 4046
    tom3 = 4047
    tom4 = 4048
                
    metronomeClosed = 5061
    metronomeOpen = 5062
    
    jingleBell = 6063
    bellTree = 6064
        
    pitchMap = {
        bassPedal: 36,
        snare: 38,
        hiHatOpen: 46,
        hiHatClosed: 42,
        hiHatClosed2: 44,
        splashCymbal: 55,
        gong: 52,
        cymbal1: 49,
        cymbal2: 57,
        rideCymbal1: 59,
        rideCymbal2: 51,
        rideBell: 53,
        cowbell: 56,
        floorTom1: 41,
        floorTom2: 43,
        tom1: 45,
        tom2: 47,
        tom3: 48,
        tom4: 50,
        metronomeClosed: 33,
        metronomeOpen: 34,
        jingleBell: 83,
        bellTree: 84
    }

################################################
