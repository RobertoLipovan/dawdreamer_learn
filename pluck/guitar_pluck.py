"""Guitar pluck: Karplus-Strong con feedback mas alto (decay mas largo) y un
extra de "pick noise" en el ataque -- mas brillante que el pluck generico."""

from common import render_pluck

FAUST_GUITAR_PLUCK = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 440, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'd = 1.0 / freq;\n'
    'pick_raw = no.noise * en.ar(0.0003, 0.004, gate) * 0.6;\n'
    'burst_raw = no.noise * en.ar(0.001, 0.006, gate) + pick_raw;\n'
    'burst = fi.lowpass(2, 7500, burst_raw);\n'
    'ks1 = burst : (+ : de.delay(0.3, d, _)) ~ (0.96 * _);\n'
    'ks2 = burst : (+ : de.delay(0.3, d * 0.998, _)) ~ (0.94 * _);\n'
    'filt = fi.lowpass(2, 4800, ks1 + ks2 * 0.7);\n'
    'process = filt * gain * 0.75 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_pluck("guitar_pluck", FAUST_GUITAR_PLUCK, voices=6)
