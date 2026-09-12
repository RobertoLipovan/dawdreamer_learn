"""Supersaw lead: pila de sierras detuneadas (7 voces) con filtro abriendose
al ataque -- el lead trance/EDM de referencia, ancho y brillante."""

from common import render_lead

FAUST_SUPERSAW_LEAD = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 440, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'raw = os.sawtooth(freq) + os.sawtooth(freq * 1.007) + os.sawtooth(freq * 0.993)\n'
    '    + os.sawtooth(freq * 1.014) * 0.7 + os.sawtooth(freq * 0.986) * 0.7\n'
    '    + os.sawtooth(freq * 1.021) * 0.5 + os.sawtooth(freq * 0.979) * 0.5;\n'
    'fenv = en.adsr(0.03, 0.25, 0.7, 0.2, gate);\n'
    'cut = 800 + 6000 * fenv;\n'
    'filt = fi.lowpass(3, cut, raw);\n'
    'env = gain * en.adsr(0.01, 0.15, 0.8, 0.25, gate);\n'
    'process = filt * env * 0.22 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_lead("supersaw_lead", FAUST_SUPERSAW_LEAD, voices=3)
