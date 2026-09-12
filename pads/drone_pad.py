"""Drone: pariente estatico del pad, sin apenas ataque/decay marcados. Se usa
como fondo continuo; aqui se deja sonar sin envolvente perceptible por nota."""

from common import render_pad

FAUST_DRONE_PAD = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 220, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'raw = os.osc(freq) + os.osc(freq * 1.001) * 0.7 + os.osc(freq * 0.5) * 0.5 + os.osc(freq * 2.003) * 0.2;\n'
    'filt = fi.lowpass(2, 1500, raw);\n'
    'env = gain * en.adsr(3.0, 0.1, 1.0, 4.0, gate);\n'
    'process = filt * env * 0.4 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_pad("drone_pad", FAUST_DRONE_PAD, voices=6)
