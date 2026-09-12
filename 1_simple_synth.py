from engine import run

def build_partitura():
    bpm = 90
    compases = 16
    max_beats = compases * 4.0

    return {
        "bpm": bpm,
        "compases": compases,
        "tracks": [
            {
                "tipo": "pad",
                "ganancia": 0.30,
                "notas": [
                    [69, 0, max_beats],
                    [72, 0, max_beats],
                    [76, 0, max_beats],
                ],
                "send": {"reverb": 0.4},
            },
            {
                "tipo": "bass",
                "ganancia": 0.30,
                "notas": [
                    [45, 0, 4],
                    [48, 4, 4],
                    [45, 8, 4],
                    [48, 12, 4],
                ],
                "send": {"reverb": 0.05},
            },
            {
                "tipo": "arpegio",
                "ganancia": 0.18,
                "notas": [
                    [76, i * 0.5, 0.25] for i in range(0, compases * 8, 1)
                ],
                "send": {"reverb": 0.15, "delay": 0.1},
            },
            {
                "tipo": "drums",
                "ganancia": 0.32,
                "kick": [0, 1, 2, 3],
                "snare": [1, 3],
                "hat": [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5],
                "swing": 0.0,
                "velocity": 0.8,
            },
        ],
    }

if __name__ == "__main__":
    run(build_partitura)