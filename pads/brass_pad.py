"""Brass pad: sostenido con caracter de metales, ataque un poco mas marcado
y filtro que se abre al principio de la nota (swell tipico de seccion de brass)."""

from common import render_pad

FAUST_BRASS_PAD = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 220, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'raw = os.sawtooth(freq) + os.sawtooth(freq * 0.998) * 0.8;\n'
    'swell = en.adsr(0.25, 0.2, 0.85, 0.6, gate);\n'
    'cut = 400 + 4500 * swell;\n'
    'filt = fi.lowpass(3, cut, raw);\n'
    'env = gain * en.adsr(0.15, 0.3, 0.8, 0.9, gate);\n'
    'process = filt * env * 0.32 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_pad("brass_pad", FAUST_BRASS_PAD, voices=6)
