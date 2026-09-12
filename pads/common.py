"""Utilidades compartidas por los scripts de pads/.
Progresion de 4 patrones (acordes) a 100 BPM, repetida 2 veces (8 compases),
y una funcion de render generica: cada script solo aporta su Faust DSP string."""

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


def build_notas():
    notas = []
    for bar in range(COMPASES):
        for n in CHORDS[bar % len(CHORDS)]:
            notas.append((n, bar * 4, 4.0))
    return notas


def render_pad(nombre, dsp_string, voices=6, fx=None, reverb=None):
    """Renderiza el loop de 4 patrones con el DSP Faust dado a pads/output/<nombre>.wav

    fx: lista opcional [(nombre_fx, dsp_string_fx), ...] encadenada tras el pad.
    reverb: dict opcional para sobreescribir los parametros del reverb final.
    """
    import dawdreamer as daw
    from scipy.io import wavfile

    beats_tot = COMPASES * 4
    duracion = beats_tot * (60.0 / BPM)
    print(f"[{nombre}] BPM {BPM} | {COMPASES} compases | {duracion:.1f}s")

    engine = daw.RenderEngine(SR, BUFFER_SIZE)
    engine.set_bpm(float(BPM))

    proc = engine.make_faust_processor("pad")
    proc.set_dsp_string(dsp_string)
    proc.num_voices = voices
    for nota, start, dur in build_notas():
        proc.add_midi_note(int(nota), 90, float(start), float(dur), beats=True)

    grafo = [(proc, [])]
    prev = "pad"
    for fx_nombre, fx_dsp in (fx or []):
        fp = engine.make_faust_processor(fx_nombre)
        fp.set_dsp_string(fx_dsp)
        grafo.append((fp, [prev]))
        prev = fx_nombre

    rv = {"room_size": 0.5, "damping": 0.4, "wet_level": 0.28, "dry_level": 0.78, "width": 0.8}
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
