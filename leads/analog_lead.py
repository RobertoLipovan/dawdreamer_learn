"""Analog lead: sierra + triangulo con filtro paso-bajo subtractivo clasico y
envolvente de filtro moderada -- el lead "Juno/Moog" calido y monofonico."""

from common import render_lead

FAUST_ANALOG_LEAD = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 440, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'raw = os.sawtooth(freq) + os.sawtooth(freq * 1.003) * 0.6 + os.triangle(freq * 0.5) * 0.3;\n'
    'fenv = en.adsr(0.03, 0.3, 0.55, 0.25, gate);\n'
    'cut = 500 + 3500 * fenv;\n'
    'filt = fi.lowpass(3, cut, raw);\n'
    'env = gain * en.adsr(0.015, 0.2, 0.75, 0.3, gate);\n'
    'process = filt * env * 0.35 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_lead("analog_lead", FAUST_ANALOG_LEAD, voices=3)
