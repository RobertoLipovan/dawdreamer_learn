"""FM bass: portadora modulada por otra a ratio 1:1, con el indice de
modulacion cayendo tras el ataque -- el "DX bass" punchy y metalico."""

from common import render_bass

FAUST_FM_BASS = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 55, 20, 500, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'ratio = 1.0;\n'
    'mod_env = en.ar(0.005, 0.2, gate) * 4;\n'
    'modulator = os.osc(freq * ratio);\n'
    'carrier = os.osc(freq + modulator * freq * mod_env);\n'
    'env = gain * en.ar(0.005, 0.3, gate);\n'
    'process = carrier * env * 0.45 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_bass("fm_bass", FAUST_FM_BASS, voices=3)
