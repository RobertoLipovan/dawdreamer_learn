"""Granular pad (aproximacion): en vez de una nube real de grains programados,
se simula la textura granular modulando tono/ruido con varios LFOs rapidos y
desincronizados entre si, que imitan la densidad/aleatoriedad de los grains."""

from common import render_pad

FAUST_GRANULAR_PAD = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 220, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'grain1 = 0.5 + 0.5 * os.osc(7.3);\n'
    'grain2 = 0.5 + 0.5 * os.osc(11.7);\n'
    'grain3 = 0.5 + 0.5 * os.osc(5.1);\n'
    'tono = os.osc(freq) + os.osc(freq * 1.5) * 0.4;\n'
    'textura = no.noise : fi.resonbp(freq * 2, 20, 1);\n'
    'raw = tono * grain1 * 0.6 + textura * grain2 * 0.3 + os.osc(freq * 3.0) * grain3 * 0.2;\n'
    'env = gain * en.adsr(1.0, 0.5, 0.7, 2.0, gate);\n'
    'process = raw * env * 0.35 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_pad("granular_pad", FAUST_GRANULAR_PAD, voices=4)
