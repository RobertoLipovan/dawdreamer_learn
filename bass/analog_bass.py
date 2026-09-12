"""Analog bass: sierra + sub-octava calida, filtro paso-bajo de 4 polos con
envolvente propia -- el bajo "Moog" subtractivo clasico."""

from common import render_bass

FAUST_ANALOG_BASS = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 55, 20, 500, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'raw = os.sawtooth(freq) + os.sawtooth(freq * 1.005) * 0.5 + os.osc(freq * 0.5) * 0.5;\n'
    'fenv = en.ar(0.005, 0.2, gate);\n'
    'cut = 400 + 2500 * fenv;\n'
    'filt = fi.lowpass(4, cut, raw);\n'
    'env = gain * en.ar(0.01, 0.35, gate);\n'
    'process = filt * env * 0.45 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_bass("analog_bass", FAUST_ANALOG_BASS, voices=3)
