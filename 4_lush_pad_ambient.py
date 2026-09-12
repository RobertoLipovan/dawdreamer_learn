"""4_lush_pad_ambient.py - pieza ambient de 1 minuto exacto usando el
dark_pad de pads/dark_pad.py (no el "pad" generico de engine.py).

BPM 80, 20 compases: 5 compases (20 tiempos = 15s) por cada uno de los 4
acordes Am-F-C-G -> 20 compases * 4 tiempos = 80 tiempos = 60.0s exactos.
Cada acorde se dobla con la sub-octava de la raiz para dar peso ("lush"),
con delay + reverb grande y un fade-in/fade-out suave en los extremos.
"""

import glob
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "pads"))
from dark_pad import FAUST_DARK_PAD  # noqa: E402

import engine

SR = engine.SR
BUFFER_SIZE = engine.BUFFER_SIZE
BPM = 80

CHORDS = [
    [57, 60, 64],  # Am
    [53, 57, 60],  # F
    [60, 64, 67],  # C
    [55, 59, 62],  # G
]
COMPASES_POR_ACORDE = 5
COMPASES = COMPASES_POR_ACORDE * len(CHORDS)  # 20 compases = 80 tiempos = 60s a 80 BPM


def build_notas():
    notas = []
    for i, chord in enumerate(CHORDS):
        start = i * COMPASES_POR_ACORDE * 4
        dur = COMPASES_POR_ACORDE * 4.0
        for n in chord:
            notas.append((n, start, dur))
        notas.append((chord[0] - 12, start, dur))  # sub-octava del root, peso extra
    return notas


def render():
    import dawdreamer as daw
    from scipy.io import wavfile

    beats_tot = COMPASES * 4
    duracion = beats_tot * (60.0 / BPM)
    print(f"4_lush_pad_ambient | BPM {BPM} | {COMPASES} compases | {duracion:.1f}s")

    render_engine = daw.RenderEngine(SR, BUFFER_SIZE)
    render_engine.set_bpm(float(BPM))

    proc = render_engine.make_faust_processor("dark_pad")
    proc.set_dsp_string(FAUST_DARK_PAD)
    proc.num_voices = 8
    for nota, start, dur in build_notas():
        proc.add_midi_note(int(nota), 85, float(start), float(dur), beats=True)

    grafo = [(proc, [])]

    dly = render_engine.make_faust_processor("delay")
    dly.set_dsp_string(engine.FAUST_DELAY_RETURN)
    grafo.append((dly, ["dark_pad"]))

    mix = render_engine.make_add_processor("mix", [1.0, 0.3])
    grafo.append((mix, ["dark_pad", "delay"]))

    verb = render_engine.make_reverb_processor("verb")
    verb.room_size = 0.85
    verb.damping = 0.25
    verb.wet_level = 0.4
    verb.dry_level = 0.75
    verb.width = 1.0
    grafo.append((verb, ["mix"]))

    # set_automation espera un valor por muestra de audio, no por bloque de
    # buffer -- con nframes en bloques la curva se agota casi al instante y
    # el gain se queda clavado en su ultimo valor (aqui, 0.0 = silencio).
    nframes = int(SR * duracion)
    master_mod = render_engine.make_faust_processor("master_mod")
    master_mod.set_dsp_string(engine.FAUST_AUTO_GAIN)
    curve = engine.build_automation(
        nframes, [(0, 0.0), (4, 1.0), (beats_tot - 8, 1.0), (beats_tot, 0.0)]
    )
    for d in master_mod.get_parameters_description():
        master_mod.set_automation(d["name"], curve)
        break
    grafo.append((master_mod, ["verb"]))

    render_engine.load_graph(grafo)
    render_engine.render(beats_tot, beats=True)
    audio = render_engine.get_audio()

    pico = float(np.abs(audio).max())
    if pico > 0:
        audio = audio * (0.85 / pico)
        audio = np.clip(audio, -1.0, 1.0)

    output_dir = engine.OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)
    existentes = sorted(
        int(os.path.splitext(os.path.basename(f))[0])
        for f in glob.glob(os.path.join(output_dir, "[0-9]*.wav"))
    )
    n = (existentes[-1] + 1) if existentes else 1
    output_path = os.path.join(output_dir, f"{n}.wav")
    wavfile.write(output_path, SR, (audio.T * 32767).astype(np.int16))
    print(f"[OK] {output_path}")
    return output_path


if __name__ == "__main__":
    render()
