"""Reese bass: dos sierras detuneadas batiendo entre si (el "phasing" tipico
del drum & bass) mas un filtro resonante que las une en una sola masa grave."""

from common import render_bass

FAUST_REESE_BASS = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 55, 20, 500, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'raw = os.sawtooth(freq * 0.99) + os.sawtooth(freq * 1.01) + os.sawtooth(freq) * 0.5;\n'
    'filt = fi.resonlp(800, 5, 1, raw);\n'
    'env = gain * en.ar(0.01, 0.3, gate);\n'
    'process = filt * env * 0.32 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_bass("reese_bass", FAUST_REESE_BASS, voices=3)
