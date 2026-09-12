"""Noise/textural pad: construido a partir de ruido filtrado en vez de un
oscilador tonal; la fundamental solo se insinua via un bandpass resonante."""

from common import render_pad

FAUST_NOISE_PAD = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 220, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'tono = os.osc(freq) * 0.3;\n'
    'raw = tono + (no.noise : fi.resonbp(freq, 25, 1)) + (no.noise : fi.resonbp(freq * 2, 15, 0.5));\n'
    'env = gain * en.adsr(1.5, 0.6, 0.7, 2.2, gate);\n'
    'process = raw * env * 0.5 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_pad("noise_pad", FAUST_NOISE_PAD, voices=4)
