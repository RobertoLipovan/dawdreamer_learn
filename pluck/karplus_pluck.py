"""Karplus-Strong pluck: el algoritmo clasico de sintesis por modelado fisico
para cuerda pulsada -- una rafaga de ruido corta circulando por dos lineas de
retardo con feedback (que definen tono y decay), mas un toque de tono puro."""

from common import render_pluck

FAUST_KARPLUS_PLUCK = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 440, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'd = 1.0 / freq;\n'
    'burst_raw = no.noise * en.ar(0.001, 0.008, gate);\n'
    'burst = fi.lowpass(2, 6500, burst_raw);\n'
    'ks1 = burst : (+ : de.delay(0.3, d, _)) ~ (0.92 * _);\n'
    'ks2 = burst : (+ : de.delay(0.3, d * 0.997, _)) ~ (0.85 * _);\n'
    'tone = os.osc(freq) * en.ar(0.003, 0.2, gate) * 0.3;\n'
    'raw = ks1 + ks2 * 0.6 + tone;\n'
    'filt = fi.lowpass(2, 3200, raw);\n'
    'process = filt * gain * 0.7 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_pluck("karplus_pluck", FAUST_KARPLUS_PLUCK, voices=6)
