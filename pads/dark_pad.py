"""Dark/evolving pad: timbre oscuro con un LFO lento moviendo el filtro,
tipico de score de terror/sci-fi. Fundamental grave, pocos armonicos altos."""

from common import render_pad

FAUST_DARK_PAD = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 220, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'raw = os.osc(freq * 0.5) * 0.6 + os.square(freq) * 0.3 + os.osc(freq * 1.997) * 0.2;\n'
    'lfo_cut = 400 + 500 * (0.5 + 0.5 * os.osc(0.08));\n'
    'filt = fi.lowpass(4, lfo_cut, raw);\n'
    'env = gain * en.adsr(2.0, 0.8, 0.6, 3.0, gate);\n'
    'process = filt * env * 0.45 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_pad("dark_pad", FAUST_DARK_PAD, voices=6)
