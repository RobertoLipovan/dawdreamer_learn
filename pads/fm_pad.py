"""FM pad: modulacion de frecuencia clasica (portadora modulada por otro
oscilador), da timbres cristalinos/metalicos con pocos parametros."""

from common import render_pad

FAUST_FM_PAD = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 220, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'ratio = 2.01;\n'
    'mod_idx = en.adsr(1.0, 0.6, 0.4, 1.5, gate) * 2.5;\n'
    'modulator = os.osc(freq * ratio);\n'
    'carrier = os.osc(freq + modulator * freq * mod_idx);\n'
    'detune = os.osc(freq * 1.003 + modulator * freq * mod_idx * 0.9);\n'
    'raw = carrier + detune * 0.5;\n'
    'env = gain * en.adsr(0.8, 0.4, 0.7, 1.8, gate);\n'
    'process = raw * env * 0.4 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_pad("fm_pad", FAUST_FM_PAD, voices=6)
