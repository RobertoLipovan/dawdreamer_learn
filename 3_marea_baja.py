from engine import run

# "Marea Baja" - chill/lo-fi, progresion vi-IV-I-V en Do mayor (Am-F-C-G)
# Estructura (compases de 4 tiempos): intro 0-3, verso1 4-11, pre-coro 12-15,
# coro1 16-23, verso2 24-31, pre-coro 32-35, coro2 36-43, puente 44-51,
# coro final 52-59, outro 60-63.

BPM = 72
COMPASES = 64

CHORDS = [
    {"pad": [57, 60, 64], "bass": 45},  # Am
    {"pad": [53, 57, 60], "bass": 41},  # F
    {"pad": [60, 64, 67], "bass": 48},  # C
    {"pad": [55, 59, 62], "bass": 43},  # G
]

def chord(bar):
    return CHORDS[bar % 4]

def build_pad():
    notas = []
    for bar in range(COMPASES):
        c = chord(bar)
        start = bar * 4
        for n in c["pad"]:
            notas.append([n, start, 4.0])
    return notas

def build_bass(bar_start, bar_end):
    notas = []
    for bar in range(bar_start, bar_end):
        c = chord(bar)
        notas.append([c["bass"], bar * 4, 3.6])
    return notas

def build_pluck(bar_start, bar_end, sparse=False):
    notas = []
    for bar in range(bar_start, bar_end):
        c = chord(bar)
        tones = [n + 12 for n in c["pad"]]
        if sparse:
            for i, idx in enumerate([0, 2]):
                notas.append([tones[idx], bar * 4 + i * 2.0, 1.8])
        else:
            idx_seq = [0, 1, 2, 1, 0, 1, 2, 1]
            for i, idx in enumerate(idx_seq):
                notas.append([tones[idx], bar * 4 + i * 0.5, 0.45])
    return notas

def build_arpegio(bar_start, bar_end):
    notas = []
    for bar in range(bar_start, bar_end):
        c = chord(bar)
        tercera = c["pad"][1] + 12
        for i in range(8):
            notas.append([tercera, bar * 4 + i * 0.5, 0.2])
    return notas

def build_lead():
    notas = [
        # puente (44-51): "y si el mundo se detiene aqui..."
        [69, 44 * 4 + 0.0, 1.5],
        [72, 44 * 4 + 1.5, 1.0],
        [74, 44 * 4 + 2.5, 1.5],
        [72, 46 * 4 + 0.0, 2.0],
        [69, 46 * 4 + 2.0, 2.0],
        [65, 48 * 4 + 0.0, 2.0],
        [69, 48 * 4 + 2.0, 2.0],
        [72, 49 * 4 + 0.0, 1.5],
        [74, 49 * 4 + 1.5, 1.0],
        [72, 49 * 4 + 2.5, 1.5],
        [67, 50 * 4 + 0.0, 4.0],
        [64, 51 * 4 + 0.0, 2.0],
        [67, 51 * 4 + 2.0, 2.0],
    ]
    # coro final (52-59): hook sostenido doblando la nota superior del acorde
    for bar in range(52, 60):
        c = chord(bar)
        notas.append([c["pad"][-1] + 12, bar * 4, 3.8])
    return notas

def build_partitura():
    return {
        "bpm": BPM,
        "compases": COMPASES,
        "tracks": [
            {
                "tipo": "pad",
                "ganancia": 0.26,
                "notas": build_pad(),
                "send": {"reverb": 0.35},
            },
            {
                "tipo": "bass",
                "ganancia": 0.30,
                "notas": build_bass(4, 60),
                "send": {"reverb": 0.04},
                "automation": [
                    {"param": "cutoff", "points": [(0, 150), (16, 300), (36, 550), (52, 750), (64, 750)]},
                ],
            },
            {
                "tipo": "pluck",
                "ganancia": 0.20,
                "notas": (
                    build_pluck(4, 44)
                    + build_pluck(44, 52, sparse=True)
                    + build_pluck(52, 60)
                ),
                "send": {"reverb": 0.12, "delay": 0.18},
            },
            {
                "tipo": "arpegio",
                "ganancia": 0.14,
                "notas": (
                    build_arpegio(16, 24)
                    + build_arpegio(36, 44)
                    + build_arpegio(52, 60)
                ),
                "send": {"reverb": 0.18, "delay": 0.22},
            },
            {
                "tipo": "lead",
                "ganancia": 0.20,
                "notas": build_lead(),
                "send": {"reverb": 0.15, "delay": 0.12},
                "automation": [
                    {"param": "cutoff", "points": [(0, 200), (44, 200), (48, 3000), (52, 5000), (64, 6500)]},
                ],
            },
            {
                "tipo": "drums",
                "ganancia": 0.28,
                "kick": [0, 1.5, 2.75],
                "snare": [1, 3],
                "hat": [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5],
                "swing": 0.15,
                "velocity": 0.72,
            },
        ],
    }

if __name__ == "__main__":
    run(build_partitura)
