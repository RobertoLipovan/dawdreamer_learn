"""Utilidades compartidas por los scripts de bass/.
Mismo progresion que pads/ y pluck/ (Am-F-C-G a 100 BPM, 2 vueltas = 8
compases), pero aqui con la nota raiz de cada acorde una octava mas abajo
y un patron ritmico sincopado tipico de linea de bajo (no acorde sostenido)."""

import os

import numpy as np

SR = 44100
BUFFER_SIZE = 128
BPM = 100

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

# raiz de Am-F-C-G una octava abajo del pad (57,53,60,55 -> -12)
ROOTS = [45, 41, 48, 43]

VUELTAS = 2  # 4 patrones x 2 vueltas = 8 compases de loop
COMPASES = len(ROOTS) * VUELTAS

# patron ritmico sincopado por compas (start, dur), en tiempos
RITMO = [(0.0, 1.5), (1.5, 0.5), (2.0, 1.0), (3.0, 0.5), (3.5, 0.5)]


def build_notas():
    notas = []
    for bar in range(COMPASES):
        root = ROOTS[bar % len(ROOTS)]
        for start, dur in RITMO:
            notas.append((root, bar * 4 + start, dur * 0.9))
    return notas


def render_bass(nombre, dsp_string, voices=3, fx=None, reverb=None):
    """Renderiza la linea de bajo del loop de 4 patrones con el DSP Faust dado
    a bass/output/<nombre>.wav

    fx: lista opcional [(nombre_fx, dsp_string_fx), ...] encadenada tras el bajo.
    reverb: dict opcional para sobreescribir los parametros del reverb final
    (por defecto casi nulo: el bajo suele ir seco).
    """
    import dawdreamer as daw
    from scipy.io import wavfile

    beats_tot = COMPASES * 4
    duracion = beats_tot * (60.0 / BPM)
    print(f"[{nombre}] BPM {BPM} | {COMPASES} compases | {duracion:.1f}s")

    engine = daw.RenderEngine(SR, BUFFER_SIZE)
    engine.set_bpm(float(BPM))

    proc = engine.make_faust_processor("bass")
    proc.set_dsp_string(dsp_string)
    proc.num_voices = voices
    for nota, start, dur in build_notas():
        proc.add_midi_note(int(nota), 110, float(start), float(dur), beats=True)

    grafo = [(proc, [])]
    prev = "bass"
    for fx_nombre, fx_dsp in (fx or []):
        fp = engine.make_faust_processor(fx_nombre)
        fp.set_dsp_string(fx_dsp)
        grafo.append((fp, [prev]))
        prev = fx_nombre

    rv = {"room_size": 0.2, "damping": 0.6, "wet_level": 0.05, "dry_level": 0.97, "width": 0.4}
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
