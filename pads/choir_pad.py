"""Choir pad: filtros de formantes (bandpass) sobre una fuente de sierra con
vibrato leve, buscando un timbre "vocal" sintetico."""

from common import render_pad

FAUST_CHOIR_PAD = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 220, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'vibrato = 1 + 0.008 * os.osc(5.2);\n'
    'src = os.sawtooth(freq * vibrato) + os.sawtooth(freq * vibrato * 1.002) * 0.6;\n'
    'raw = (src : fi.resonbp(700, 10, 1)) + (src : fi.resonbp(1150, 10, 0.6)) + (src : fi.resonbp(2600, 10, 0.3));\n'
    'env = gain * en.adsr(0.8, 0.4, 0.75, 1.8, gate);\n'
    'process = raw * env * 0.4 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_pad("choir_pad", FAUST_CHOIR_PAD, voices=6)
