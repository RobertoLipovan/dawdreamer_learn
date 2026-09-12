"""Analog/vintage pad: osciladores detuneados con "drift" de afinacion lento
(simulando la inestabilidad de un VCO analogico) y saturacion suave."""

from common import render_pad

FAUST_ANALOG_PAD = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 220, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'drift1 = 1 + 0.004 * os.osc(0.13);\n'
    'drift2 = 1 + 0.004 * os.osc(0.09 + 0.02);\n'
    'raw = os.sawtooth(freq * drift1) + os.sawtooth(freq * 0.997 * drift2) * 0.8 + os.triangle(freq * 2.0) * 0.15;\n'
    'sat = raw * 0.5 / (1 + abs(raw * 0.5));\n'
    'filt = fi.lowpass(2, 2200, sat);\n'
    'env = gain * en.adsr(0.9, 0.4, 0.75, 1.8, gate);\n'
    'process = filt * env * 0.4 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_pad("analog_pad", FAUST_ANALOG_PAD, voices=6)
