"""Growl bass: saturacion agresiva sobre sierra+cuadrada subarmonica, con LFO
en el filtro -- el bajo "growl" de dubstep/riddim mas sucio que el wobble."""

from common import render_bass

FAUST_GROWL_BASS = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 55, 20, 500, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'raw = os.sawtooth(freq) + os.square(freq * 0.5) * 0.6;\n'
    'drive = 4;\n'
    'sat = (raw * drive) / (1 + abs(raw * drive));\n'
    'lfo = 0.5 + 0.5 * os.osc(9);\n'
    'cut = 300 + 2500 * lfo;\n'
    'filt = fi.resonlp(cut, 10, 1, sat);\n'
    'env = gain * en.ar(0.005, 0.25, gate);\n'
    'process = filt * env * 0.4 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_bass("growl_bass", FAUST_GROWL_BASS, voices=3)
