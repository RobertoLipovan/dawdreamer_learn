"""Pizzicato pluck: Karplus-Strong con decay muy corto (cuerda apagada con el
dedo) mas una resonancia de "cuerpo" en banda media, como una cuerda orquestal
tocada pizzicato."""

from common import render_pluck

FAUST_PIZZICATO_PLUCK = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 440, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'd = 1.0 / freq;\n'
    'burst_raw = no.noise * en.ar(0.001, 0.004, gate);\n'
    'burst = fi.lowpass(2, 5500, burst_raw);\n'
    'ks1 = burst : (+ : de.delay(0.3, d, _)) ~ (0.80 * _);\n'
    'ks2 = burst : (+ : de.delay(0.3, d * 0.996, _)) ~ (0.72 * _);\n'
    'cuerpo = (ks1 + ks2) : fi.resonbp(350, 6, 1);\n'
    'raw = ks1 + ks2 * 0.5 + cuerpo * 0.5;\n'
    'filt = fi.lowpass(2, 3800, raw);\n'
    'process = filt * gain * 0.75 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_pluck("pizzicato_pluck", FAUST_PIZZICATO_PLUCK, voices=6)
