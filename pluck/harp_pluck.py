"""Harp pluck: Karplus-Strong muy amortiguado y calido, ataque suave (sin pick
noise agudo) y decay largo -- cuerdas de arpa/kalimba de cuerpo grande."""

from common import render_pluck

FAUST_HARP_PLUCK = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 440, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'd = 1.0 / freq;\n'
    'burst_raw = no.noise * en.ar(0.002, 0.015, gate);\n'
    'burst = fi.lowpass(2, 3500, burst_raw);\n'
    'ks1 = burst : (+ : de.delay(0.3, d, _)) ~ (0.965 * _);\n'
    'ks2 = burst : (+ : de.delay(0.3, d * 1.003, _)) ~ (0.955 * _);\n'
    'filt = fi.lowpass(2, 2200, ks1 + ks2 * 0.8);\n'
    'process = filt * gain * 0.7 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_pluck(
        "harp_pluck", FAUST_HARP_PLUCK, voices=8,
        reverb={"room_size": 0.5, "damping": 0.4, "wet_level": 0.3, "dry_level": 0.75, "width": 0.9},
    )
