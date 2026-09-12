"""FM pluck: portadora modulada en frecuencia por otra, con el indice de
modulacion cayendo rapido tras el ataque -- el clasico "electric piano/bell
pluck" de sintesis FM (tipo DX7)."""

from common import render_pluck

FAUST_FM_PLUCK = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 440, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'ratio = 3.0;\n'
    'mod_env = en.ar(0.001, 0.25, gate) * 3.5;\n'
    'modulator = os.osc(freq * ratio);\n'
    'carrier = os.osc(freq + modulator * freq * mod_env);\n'
    'amp_env = en.ar(0.002, 0.35, gate);\n'
    'process = carrier * amp_env * gain * 0.55 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_pluck("fm_pluck", FAUST_FM_PLUCK, voices=6)
