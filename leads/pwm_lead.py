"""PWM lead: onda cuadrada cuyo ancho de pulso se modula con un LFO lento
(derivada de una sierra 0..1 comparada con un duty variable) -- el movimiento
tímbrico "vivo" tipico de los leads PWM analogicos."""

from common import render_lead

FAUST_PWM_LEAD = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 440, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'saw01 = (os.sawtooth(freq) + 1) * 0.5;\n'
    'duty = 0.5 + 0.35 * os.osc(2.5);\n'
    'raw = (saw01 < duty) * 2 - 1;\n'
    'filt = fi.lowpass(2, 6000, raw);\n'
    'env = gain * en.adsr(0.02, 0.2, 0.75, 0.3, gate);\n'
    'process = filt * env * 0.3 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_lead("pwm_lead", FAUST_PWM_LEAD, voices=3)
