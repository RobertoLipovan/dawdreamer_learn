"""Music box pluck: timbre cristalino -- fundamental + armonicos altos puros,
ataque instantaneo y decay corto en el cuerpo pero con una cola de "shimmer"
mas larga en los armonicos superiores."""

from common import render_pluck

FAUST_MUSIC_BOX_PLUCK = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 440, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'cuerpo = en.ar(0.0005, 0.15, gate);\n'
    'shimmer = en.ar(0.001, 0.9, gate);\n'
    'raw = os.osc(freq) * cuerpo\n'
    '    + os.osc(freq * 2) * 0.5 * shimmer\n'
    '    + os.osc(freq * 4) * 0.3 * shimmer\n'
    '    + os.osc(freq * 8) * 0.15 * shimmer;\n'
    'process = raw * gain * 0.5 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_pluck(
        "music_box_pluck", FAUST_MUSIC_BOX_PLUCK, voices=8,
        reverb={"room_size": 0.6, "damping": 0.3, "wet_level": 0.32, "dry_level": 0.72, "width": 0.9},
    )
