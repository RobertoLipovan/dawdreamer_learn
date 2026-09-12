"""Warm pad: subtractivo clasico, ondas triangulares apiladas + sub-octava,
filtro paso-bajo suave y ataque/release lentos. El "pad calido" de referencia."""

from common import render_pad

FAUST_WARM_PAD = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 220, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'raw = os.triangle(freq) + os.triangle(freq * 1.005) * 0.6 + os.osc(freq * 0.5) * 0.35;\n'
    'filt = fi.lowpass(2, 1800, raw);\n'
    'env = gain * en.adsr(1.2, 0.5, 0.75, 2.0, gate);\n'
    'process = filt * env * 0.5 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_pad("warm_pad", FAUST_WARM_PAD, voices=6)
