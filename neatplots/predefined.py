from neatplots.colors import QualitativePalette

palettes = {
    2: {
        'poles2': QualitativePalette(2, 15),
        'pinkgrass': QualitativePalette(2, 160)
    },
    3: {
        'summer': QualitativePalette(3, 240),
        'earth': QualitativePalette(3, 60),
        'warm': QualitativePalette(3, 6, 180),
        'cold': QualitativePalette(3, 186, 180),
        'poles': QualitativePalette(3, 237, 180)
    },
    4: {
        'four': QualitativePalette(4, 120, luminance=60, chroma=90)
    },
    5: {
        'five': QualitativePalette(5, 0)
    },
    6: {
        'rainbow': QualitativePalette(6, 20)
    }
}

for d in palettes.itervalues():
    for name, palette in d.iteritems():
        vars()[name] = palette
