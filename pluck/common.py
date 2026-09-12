"""Utilidades compartidas por los scripts de pluck/.
Mismo patron que pads/common.py: progresion de 4 acordes (Am-F-C-G) a 100 BPM,
repetida 2 veces (8 compases), pero aqui arpegiada en corcheas para que cada
pluck se oiga con su propio ataque/decay en vez de sostenido."""

import os

import numpy as np

SR = 44100
BUFFER_SIZE = 128
BPM = 100

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

# vi-IV-I-V en Do mayor (Am-F-C-G), un acorde por compas
CHORDS = [
    [57, 60, 64],  # Am
    [53, 57, 60],  # F
    [60, 64, 67],  # C
    [55, 59, 62],  # G
]

VUELTAS = 2  # 4 patrones x 2 vueltas = 8 compases de loop
COMPASES = len(CHORDS) * VUELTAS

# patron ritmico en corcheas sobre el acorde subido una octava: 1-3-5-3 x2
IDX_SEQ = [0, 1, 2, 1, 0, 1, 2, 1]


def build_notas():
    notas = []
    for bar in range(COMPASES):
        tonos = [n + 12 for n in CHORDS[bar % len(CHORDS)]]
        for i, idx in enumerate(IDX_SEQ):
            start = bar * 4 + i * 0.5
            notas.append((tonos[idx], start, 0.45))
    return notas


def render_pluck(nombre, dsp_string, voices=6, fx=None, reverb=None):
    """Renderiza el loop de 4 patrones arpegiado con el DSP Faust dado
    a pluck/output/<nombre>.wav

    fx: lista opcional [(nombre_fx, dsp_string_fx), ...] encadenada tras el pluck.
    reverb: dict opcional para sobreescribir los parametros del reverb final.
    """
    import dawdreamer as daw
    from scipy.io import wavfile

    beats_tot = COMPASES * 4
    duracion = beats_tot * (60.0 / BPM)
    print(f"[{nombre}] BPM {BPM} | {COMPASES} compases | {duracion:.1f}s")

    engine = daw.RenderEngine(SR, BUFFER_SIZE)
    engine.set_bpm(float(BPM))

    proc = engine.make_faust_processor("pluck")
    proc.set_dsp_string(dsp_string)
    proc.num_voices = voices
    for nota, start, dur in build_notas():
        proc.add_midi_note(int(nota), 100, float(start), float(dur), beats=True)

    grafo = [(proc, [])]
    prev = "pluck"
    for fx_nombre, fx_dsp in (fx or []):
        fp = engine.make_faust_processor(fx_nombre)
        fp.set_dsp_string(fx_dsp)
        grafo.append((fp, [prev]))
        prev = fx_nombre

    rv = {"room_size": 0.3, "damping": 0.5, "wet_level": 0.2, "dry_level": 0.85, "width": 0.7}
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
