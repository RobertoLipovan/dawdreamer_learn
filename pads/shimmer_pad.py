"""Shimmer/airy pad: capas agudas por encima de la fundamental (shimmer) para
dar sensacion de brillo y aire, con ataque lento y mucho reverb (via common)."""

from common import render_pad

FAUST_SHIMMER_PAD = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 220, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'base = os.osc(freq) + os.osc(freq * 1.003) * 0.5;\n'
    'shimmer = os.osc(freq * 4.01) * 0.25 + os.osc(freq * 6.02) * 0.12 + os.osc(freq * 8.03) * 0.06;\n'
    'raw = base + shimmer;\n'
    'filt = fi.highpass(1, 300, raw);\n'
    'env = gain * en.adsr(1.6, 0.6, 0.7, 2.5, gate);\n'
    'process = filt * env * 0.4 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_pad(
        "shimmer_pad", FAUST_SHIMMER_PAD, voices=6,
        reverb={"room_size": 0.8, "damping": 0.2, "wet_level": 0.45, "dry_level": 0.65, "width": 1.0},
    )
