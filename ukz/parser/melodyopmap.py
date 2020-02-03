from ukz.melody import Melody

# How to apply an operator to a (flat, not hierarchical) melody.
ukzOpMap = {
    '*': Melody.stretch,
    '/': Melody.contract,
    '=': Melody.stretchTo,
    '_': Melody.durSet,
    '_*': Melody.durStretch,
    '_/': Melody.durContract,
    '_+': Melody.durExtend,
    '_-': Melody.durShorten,
    '^': Melody.setLoudness,
    'x': Melody.repeat,
    'x=': Melody.repeatUntil2,
    '+': Melody.translateUp,
    '-': Melody.translateDown,
    '~': Melody.bend,
    '<': Melody.backward,
    '<<': Melody.insertMelody,
    '$': Melody.atScale,
    '$$': Melody.atScale2 }
