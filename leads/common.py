"""Utilidades compartidas por los scripts de leads/.
Misma progresion Am-F-C-G a 100 BPM, 2 vueltas (8 compases), pero aqui con
una melodia diatonica en negras (un lead es monofonico/protagonista, no un
acorde ni una linea de bajo) que se mueve sobre cada acorde."""

import os

import numpy as np

SR = 44100
BUFFER_SIZE = 128
BPM = 100

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

# motivo de 4 negras por compas sobre Am-F-C-G (todo diatonico en Do mayor/La menor)
MELODY = [
    [69, 72, 74, 72],  # sobre Am
    [65, 69, 72, 69],  # sobre F
    [67, 71, 72, 71],  # sobre C
    [67, 71, 74, 71],  # sobre G (tension que resuelve de vuelta a Am)
]

VUELTAS = 2  # 4 patrones x 2 vueltas = 8 compases de loop
COMPASES = len(MELODY) * VUELTAS


def build_notas():
    notas = []
    for bar in range(COMPASES):
        for i, nota in enumerate(MELODY[bar % len(MELODY)]):
            notas.append((nota, bar * 4 + i * 1.0, 0.9))
    return notas


def render_lead(nombre, dsp_string, voices=3, fx=None, reverb=None):
    """Renderiza la melodia del loop de 4 patrones con el DSP Faust dado
    a leads/output/<nombre>.wav

    fx: lista opcional [(nombre_fx, dsp_string_fx), ...] encadenada tras el lead.
    reverb: dict opcional para sobreescribir los parametros del reverb final.
    """
    import dawdreamer as daw
    from scipy.io import wavfile

    beats_tot = COMPASES * 4
    duracion = beats_tot * (60.0 / BPM)
    print(f"[{nombre}] BPM {BPM} | {COMPASES} compases | {duracion:.1f}s")

    engine = daw.RenderEngine(SR, BUFFER_SIZE)
    engine.set_bpm(float(BPM))

    proc = engine.make_faust_processor("lead")
    proc.set_dsp_string(dsp_string)
    proc.num_voices = voices
    for nota, start, dur in build_notas():
        proc.add_midi_note(int(nota), 105, float(start), float(dur), beats=True)

    grafo = [(proc, [])]
    prev = "lead"
    for fx_nombre, fx_dsp in (fx or []):
        fp = engine.make_faust_processor(fx_nombre)
        fp.set_dsp_string(fx_dsp)
        grafo.append((fp, [prev]))
        prev = fx_nombre

    rv = {"room_size": 0.35, "damping": 0.45, "wet_level": 0.2, "dry_level": 0.85, "width": 0.7}
    rv.update(reverb or {})
    verb = engine.make_reverb_processor("verb")
    verb.room_size = rv["room_size"]
    verb.damping = rv["damping"]
    verb.wet_level = rv["wet_level"]
    verb.dry_level = rv["dry_level"]
    verb.width = rv["width"]
    grafo.append((verb, [prev]))

    engine.load_graph(grafo)
    engine.render(beats_tot, beats=True)
    audio = engine.get_audio()

    pico = float(np.abs(audio).max())
    if pico > 0:
        audio = audio * (0.85 / pico)
        audio = np.clip(audio, -1.0, 1.0)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, f"{nombre}.wav")
    wavfile.write(output_path, SR, (audio.T * 32767).astype(np.int16))
    print(f"[OK] {output_path}")
    return output_path
