"""Distortion lead: sierras dobles saturadas -- el lead "rock/guitarra"
agresivo, con el filtro abriendose un poco tras el ataque para dar mordiente."""

from common import render_lead

FAUST_DISTORTION_LEAD = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 440, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'raw = os.sawtooth(freq) + os.sawtooth(freq * 1.006) * 0.8;\n'
    'drive = 6;\n'
    'sat = (raw * drive) / (1 + abs(raw * drive));\n'
    'fenv = en.adsr(0.01, 0.2, 0.7, 0.2, gate);\n'
    'cut = 1500 + 4000 * fenv;\n'
    'filt = fi.lowpass(2, cut, sat);\n'
    'env = gain * en.adsr(0.005, 0.15, 0.85, 0.2, gate);\n'
    'process = filt * env * 0.3 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_lead("distortion_lead", FAUST_DISTORTION_LEAD, voices=3)
