"""FM lead: portadora modulada por otra a ratio 2:1 con indice de modulacion
alto y sostenido -- timbre metalico/campana tipico de leads FM (DX7)."""

from common import render_lead

FAUST_FM_LEAD = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 440, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'ratio = 2.0;\n'
    'mod_env = en.adsr(0.02, 0.3, 0.6, 0.2, gate) * 3.0;\n'
    'modulator = os.osc(freq * ratio);\n'
    'carrier = os.osc(freq + modulator * freq * mod_env);\n'
    'env = gain * en.adsr(0.005, 0.15, 0.8, 0.2, gate);\n'
    'process = carrier * env * 0.35 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_lead("fm_lead", FAUST_FM_LEAD, voices=3)
