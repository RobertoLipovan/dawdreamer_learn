from engine import run

def build_partitura():
    bpm = 130
    compases = 16
    max_beats = compases * 4.0

    return {
        "bpm": bpm,
        "compases": compases,
        "tracks": [
            # Bassline oscura en loop (notas swing en la escala de G)
            {
                "tipo": "bass",
                "ganancia": 0.35,
                "notas": [
                    [43, 0, 1.5],
                    [45, 1.5, 0.5],
                    [43, 2, 1.0],
                    [41, 3, 0.5],
                    [43, 3.5, 0.5],
                    [43, 4, 1.5],
                    [45, 5.5, 0.5],
                    [43, 6, 1.0],
                    [41, 7, 0.5],
                    [43, 7.5, 0.5],
                    [43, 8, 1.5],
                    [45, 9.5, 0.5],
                    [43, 10, 1.0],
                    [41, 11, 0.5],
                    [43, 11.5, 0.5],
                    [43, 12, 1.5],
                    [38, 13.5, 0.5],
                    [43, 14, 1.0],
                    [41, 15, 0.5],
                    [43, 15.5, 0.5],
                ],
                "send": {"reverb": 0.02},
                "automation": [
                    {"param": "cutoff", "points": [(0, 200), (8, 800), (16, 200)]},
                ],
            },
            # Lead con filtro abriendose
            {
                "tipo": "lead",
                "ganancia": 0.20,
                "notas": [
                    [67, 0, 0.5],
                    [67, 1, 0.5],
                    [67, 2, 0.5],
                    [67, 3, 0.5],
                    [67, 4, 4.0],
                    [67, 8, 0.3],
                    [69, 8.5, 0.3],
                    [71, 9, 0.3],
                    [72, 9.5, 0.3],
                    [74, 10, 4.0],
                ],
                "send": {"reverb": 0.1, "delay": 0.15},
                "automation": [
                    {"param": "cutoff", "points": [(0, 200), (16, 6000)]},
                ],
            },
            # Arpegio filtraje agudo, entra a mitad
            {
                "tipo": "arpegio",
                "ganancia": 0.10,
                "notas": [
                    [79, 8 + i * 0.25, 0.15] for i in range(0, 32, 1)
                ],
                "send": {"delay": 0.3},
                "automation": [
                    {"param": "cutoff", "points": [(8, 100), (12, 500), (16, 100)]},
                ],
            },
            # Four-on-the-floor: kick en negras, snare en 2 y 4, hat en corcheas
            {
                "tipo": "drums",
                "ganancia": 0.35,
                "kick": [0, 1, 2, 3],
                "snare": [1, 3],
                "hat": [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5],
                "swing": 0.0,
                "velocity": 0.9,
            },
        ],
    }

if __name__ == "__main__":
    run(build_partitura)