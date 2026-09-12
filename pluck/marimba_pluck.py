"""Marimba pluck: modelo de percusion de barra de madera -- fundamental mas
un par de parciales inarmonicos tipicos de barras (~3.9x y ~9.2x) con envolvente
de golpe rapida (attack casi instantaneo, decay corto)."""

from common import render_pluck

FAUST_MARIMBA_PLUCK = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 440, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'golpe = en.ar(0.001, 0.35, gate);\n'
    'raw = os.osc(freq) + os.osc(freq * 3.93) * 0.35 + os.osc(freq * 9.2) * 0.15;\n'
    'process = raw * golpe * gain * 0.6 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_pluck("marimba_pluck", FAUST_MARIMBA_PLUCK, voices=6)
