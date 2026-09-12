"""String pad: imita una seccion de cuerdas sintetizadas (ensemble de sierras
detuneadas), ataque medio y filtro algo mas brillante que el warm pad."""

from common import render_pad

FAUST_STRING_PAD = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 220, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'raw = os.sawtooth(freq) + os.sawtooth(freq * 1.004) + os.sawtooth(freq * 0.996)\n'
    '    + os.sawtooth(freq * 1.008) * 0.5 + os.sawtooth(freq * 0.992) * 0.5;\n'
    'filt = fi.lowpass(3, 3200, raw);\n'
    'env = gain * en.adsr(0.6, 0.3, 0.8, 1.4, gate);\n'
    'process = filt * env * 0.28 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_pad("string_pad", FAUST_STRING_PAD, voices=6)
