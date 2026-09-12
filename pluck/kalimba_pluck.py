"""Kalimba pluck: lengueta metalica -- fundamental con parciales inarmonicos
mas altos que la marimba (~2.76x y ~5.4x, tipicos de tines metalicas) y decay
un poco mas largo con "zumbido" caracteristico."""

from common import render_pluck

FAUST_KALIMBA_PLUCK = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 440, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'golpe = en.ar(0.0008, 0.6, gate);\n'
    'raw = os.osc(freq) + os.osc(freq * 2.76) * 0.4 + os.osc(freq * 5.4) * 0.2;\n'
    'zumbido = no.noise * en.ar(0.0005, 0.02, gate) * 0.1;\n'
    'process = (raw + zumbido) * golpe * gain * 0.55 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_pluck("kalimba_pluck", FAUST_KALIMBA_PLUCK, voices=6)
