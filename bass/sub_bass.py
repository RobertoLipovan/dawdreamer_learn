"""Sub bass: seno limpio con un toque de segundo armonico (para que se oiga
en altavoces pequenos), sin filtro ni distorsion -- el "808 sub" de referencia."""

from common import render_bass

FAUST_SUB_BASS = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 55, 20, 500, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'raw = os.osc(freq) + os.osc(freq * 2) * 0.15;\n'
    'env = gain * en.ar(0.005, 0.3, gate);\n'
    'process = raw * env * 0.6 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_bass("sub_bass", FAUST_SUB_BASS, voices=3)
