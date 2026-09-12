"""Additive pad: el timbre se construye sumando sinusoides puras (parciales)
con pesos decrecientes, en vez de restar armonicos con un filtro."""

from common import render_pad

FAUST_ADDITIVE_PAD = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 220, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'raw = os.osc(freq) * 1.0\n'
    '    + os.osc(freq * 2) * 0.5\n'
    '    + os.osc(freq * 3) * 0.33\n'
    '    + os.osc(freq * 4) * 0.22\n'
    '    + os.osc(freq * 5) * 0.14\n'
    '    + os.osc(freq * 6) * 0.09\n'
    '    + os.osc(freq * 7) * 0.05;\n'
    'env = gain * en.adsr(1.0, 0.5, 0.7, 2.0, gate);\n'
    'process = raw * env * 0.28 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_pad("additive_pad", FAUST_ADDITIVE_PAD, voices=6)
