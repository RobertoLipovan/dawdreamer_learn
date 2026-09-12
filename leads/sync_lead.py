"""Sync lead (aproximacion): en vez de un hard sync real (resetear la fase de
un oscilador esclavo con el maestro, dificil de expresar en Faust sin
primitivas de fase), se aproxima el barrido armonico caracteristico con un
segundo oscilador cuyo ratio de frecuencia cae desde 4x hasta 1x tras el
ataque -- el mismo efecto perceptivo de "barrido metalico" que da el sync."""

from common import render_lead

FAUST_SYNC_LEAD = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 440, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'ratio_env = 1 + 3 * en.adsr(0.02, 0.3, 0.5, 0.2, gate);\n'
    'osc2 = os.sawtooth(freq * ratio_env);\n'
    'raw = os.sawtooth(freq) * 0.4 + osc2;\n'
    'filt = fi.lowpass(2, 7000, raw);\n'
    'env = gain * en.adsr(0.005, 0.2, 0.75, 0.25, gate);\n'
    'process = filt * env * 0.3 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_lead("sync_lead", FAUST_SYNC_LEAD, voices=3)
