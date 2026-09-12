"""Wobble bass: un LFO rapido mueve el corte de un filtro resonante sobre
sierras detuneadas -- el "wobble" tipico del dubstep."""

from common import render_bass

FAUST_WOBBLE_BASS = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 55, 20, 500, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'raw = os.sawtooth(freq) + os.sawtooth(freq * 1.01) * 0.6;\n'
    'lfo = 0.5 + 0.5 * os.osc(6);\n'
    'cut = 200 + 3000 * lfo;\n'
    'filt = fi.resonlp(cut, 8, 1, raw);\n'
    'env = gain * en.ar(0.01, 0.3, gate);\n'
    'process = filt * env * 0.35 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_bass("wobble_bass", FAUST_WOBBLE_BASS, voices=3)
