"""Acid bass: sierra a traves de un filtro paso-bajo muy resonante con
envolvente propia (la formula TB-303) -- el squelch caracteristico del acid."""

from common import render_bass

FAUST_ACID_BASS = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 55, 20, 500, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'raw = os.sawtooth(freq);\n'
    'fenv = en.ar(0.005, 0.25, gate);\n'
    'cut = 300 + 3500 * fenv;\n'
    'filt = fi.resonlp(cut, 18, 1, raw);\n'
    'env = gain * en.ar(0.005, 0.3, gate);\n'
    'process = filt * env * 0.3 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_bass("acid_bass", FAUST_ACID_BASS, voices=3)
