"""Square lead: onda cuadrada pura con un toque de sub-octava -- el timbre
"chiptune"/8-bit hueco y directo, sin filtro que lo suavice."""

from common import render_lead

FAUST_SQUARE_LEAD = (
    'import("stdfaust.lib");\n'
    'freq = nentry("freq", 440, 20, 5000, 0.01);\n'
    'gain = nentry("gain", 0.5, 0, 1, 0.01);\n'
    'gate = button("gate");\n'
    'raw = os.square(freq) + os.square(freq * 0.5) * 0.3;\n'
    'env = gain * en.adsr(0.002, 0.05, 0.85, 0.06, gate);\n'
    'process = raw * env * 0.28 <: _, _;\n'
    'effect = _;\n'
)

if __name__ == "__main__":
    render_lead(
        "square_lead", FAUST_SQUARE_LEAD, voices=3,
        reverb={"room_size": 0.15, "damping": 0.6, "wet_level": 0.08, "dry_level": 0.95, "width": 0.4},
    )
