"""Vocal lead: filtros de formantes (bandpass) sobre una sierra con vibrato,
como el choir_pad pero mas protagonista/agresivo -- lead con caracter "vocal"."""

from common import render_lead

FAUST_VOCAL_LEAD = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 440, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'vibrato = 1 + 0.012 * os.osc(5.5);\n'
    'src = os.sawtooth(freq * vibrato) + os.sawtooth(freq * vibrato * 1.003) * 0.7;\n'
    'raw = (src : fi.resonbp(800, 8, 1)) + (src : fi.resonbp(1400, 8, 0.7)) + (src : fi.resonbp(2900, 8, 0.35));\n'
    'env = gain * en.adsr(0.02, 0.2, 0.75, 0.3, gate);\n'
    'process = raw * env * 0.32 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_lead("vocal_lead", FAUST_VOCAL_LEAD, voices=3)
