"""Analog pluck: el "trance/house pluck" clasico -- sierra subtractiva con
envolvente de filtro rapida (brillante al golpe, se oscurece enseguida) y
resonancia, sin modelado de cuerda."""

from common import render_pluck

FAUST_ANALOG_PLUCK = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 440, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'raw = os.sawtooth(freq) + os.sawtooth(freq * 1.005) * 0.7;\n'
    'filt_env = en.ar(0.001, 0.18, gate);\n'
    'cut = 200 + 6000 * filt_env;\n'
    'filt = fi.resonlp(cut, 3, 1, raw);\n'
    'amp_env = en.ar(0.001, 0.3, gate);\n'
    'process = filt * amp_env * gain * 0.4 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_pluck("analog_pluck", FAUST_ANALOG_PLUCK, voices=6)
