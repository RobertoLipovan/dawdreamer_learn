"""Pluck bass: envolvente de pitch descendente sobre el propio oscilador (el
"pop" tipico del bajo tipo 808/synth-bass corto) mas ataque y decay rapidos."""

from common import render_bass

FAUST_PLUCK_BASS = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 55, 20, 500, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'pitch_env = 1 + 3 * en.ar(0.001, 0.05, gate);\n'
    'raw = os.osc(freq * pitch_env) + os.square(freq) * 0.3;\n'
    'env = gain * en.ar(0.001, 0.15, gate);\n'
    'process = raw * env * 0.5 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_bass("pluck_bass", FAUST_PLUCK_BASS, voices=3)
