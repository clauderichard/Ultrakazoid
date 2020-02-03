from ukz.ukmelody import Melody,Event,Note,Notes,Events

# How to apply an operator to a (flat, not hierarchical) melody.
ukzMelodyOpMap = {
    '=': Melody.expandTo,
    'x': Melody.repeat,
    'x=': Melody.repeatUntil,
    '~': Melody.pitchBendWithMelody,
    'o': Melody.volumeBendWithMelody,
    '<<': Melody.injectMelody,
    '<_': Melody.zipDurations,
    '&': Melody.lock,
    '¬': Melody.durationUntilEnd
}

ukzMelodyForAllOpMap = {
  Melody.forAllTime: {
    '*': Event.expand,
    '/': Event.contract,
    '>': Event.forward,
    '<': Event.backward,
  },
  Melody.forAllNotes: {
    '°': Note.setL,
    '_': Event.setD,
    '_*': Event.durExpand,
    '_/': Event.durContract,
    '_+': Event.durExtend,
    '_-': Event.durShorten,
    '+': Note.translateUp,
    '-': Note.translateDown,
    '$': Note.atScale1,
    '$$': Note.atScale2
  }
}