"""Motor de síntesis y render para dawdreamer_learn.
Reutilizado por todos los scripts de canción que solo definen build_partitura()."""

import math
import os

import numpy as np

SAMPLE_RATE = 44100
SR = SAMPLE_RATE
BUFFER_SIZE = 128

MIDI_MIN, MIDI_MAX = 36, 84
GANANCIA_MAX = 0.5
BPM_MIN, BPM_MAX = 50, 140
COMPASES_MIN, COMPASES_MAX = 8, 64

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

# ─── SINTESIS FAUST ──────────────────────────────────────────────────

FAUST_PAD = (
    'import("stdfaust.lib");\n'
    "freq = nentry(\"freq\", 220, 20, 5000, 0.01);\n"
    "gain = nentry(\"gain\", 0.5, 0, 1, 0.01);\n"
    "gate = button(\"gate\");\n"
    "ratio = nentry(\"ratio\", 1.5, 0.5, 4, 0.01);\n"
    "mod_idx = nentry(\"mod_idx\", 0.5, 0.1, 3, 0.01);\n"
    "cut = hslider(\"cut\", 3000, 200, 10000, 1);\n"
    "lfo_rate = hslider(\"lfo\", 0.06, 0.01, 0.5, 0.01);\n"
    "carrier = os.osc(freq);\n"
    "modulator = os.osc(freq * ratio + 0.5 * os.osc(lfo_rate));\n"
    "fm = os.osc(freq + modulator * freq * ratio * mod_idx);\n"
    "det = os.osc(freq * 1.003 + modulator * freq * ratio * mod_idx * 0.6);\n"
    "raw = fm + det * 0.5 + 0.2 * os.osc(freq * 2.01);\n"
    "lfo_cut = cut + 2000 * os.osc(lfo_rate * 0.3);\n"
    "filt = fi.lowpass(4, max(100, lfo_cut), raw);\n"
    "env = gain * en.adsr(1.0, 0.5, 0.6, 1.8, gate);\n"
    "process = filt * env * 0.5 <: _, _;\n"
    "effect = _;\n"
)

FAUST_PLUCK = (
    'import("stdfaust.lib");\n'
    "freq = nentry(\"freq\", 440, 20, 5000, 0.01);\n"
    "gain = nentry(\"gain\", 0.5, 0, 1, 0.01);\n"
    "gate = button(\"gate\");\n"
    "d = 1.0 / freq;\n"
    "burst = no.noise * en.ar(0.001, 0.008, gate);\n"
    "ks1 = burst : (+ : de.delay(0.3, d, _)) ~ (0.92 * _);\n"
    "ks2 = burst : (+ : de.delay(0.3, d * 0.997, _)) ~ (0.85 * _);\n"
    "tone = os.osc(freq) * en.ar(0.003, 0.2, gate) * 0.3;\n"
    "process = (ks1 + ks2 * 0.6 + tone) * gain * 0.7 <: _, _;\n"
    "effect = _;\n"
)

FAUST_BASS = (
    'import("stdfaust.lib");\n'
    "freq = nentry(\"freq\", 55, 20, 500, 0.01);\n"
    "gain = nentry(\"gain\", 0.5, 0, 1, 0.01);\n"
    "gate = button(\"gate\");\n"
    "raw = os.square(freq) * 0.5 + os.osc(freq) * 0.4 + os.osc(freq * 0.5) * 0.6 + 0.3 * os.osc(freq * 2.01);\n"
    "sat = raw * 0.35 / (1 + abs(raw * 0.35));\n"
    "env = gain * en.ar(0.02, 0.4, gate);\n"
    "process = (raw * 0.6 + sat * 0.5) * env * 0.8 <: _, _;\n"
    "effect = _;\n"
)

FAUST_ARPEGIO = (
    'import("stdfaust.lib");\n'
    "freq = nentry(\"freq\", 440, 20, 5000, 0.01);\n"
    "gain = nentry(\"gain\", 0.5, 0, 1, 0.01);\n"
    "gate = button(\"gate\");\n"
    "mod = os.osc(freq * 1.5) * 0.6;\n"
    "carrier = os.osc(freq + mod);\n"
    "shimmer = os.osc(freq * 2.01) * 0.3 + os.osc(freq * 3.02) * 0.15 + os.osc(freq * 4.03) * 0.08;\n"
    "raw = carrier + shimmer;\n"
    "env = gain * en.ar(0.003, 0.15, gate);\n"
    "process = raw * env * 0.6 <: _, _;\n"
    "effect = _;\n"
)

FAUST_LEAD = (
    'import("stdfaust.lib");\n'
    "freq = nentry(\"freq\", 440, 20, 5000, 0.01);\n"
    "gain = nentry(\"gain\", 0.5, 0, 1, 0.01);\n"
    "gate = button(\"gate\");\n"
    "supersaw = os.square(freq) + os.square(freq * 1.004) + os.square(freq * 0.996) + os.osc(freq * 1.01) + os.osc(freq * 0.99);\n"
    "swell = gain * en.adsr(0.02, 0.3, 0.7, 0.5, gate);\n"
    "sweep = 500 + 7000 * (1 - en.adsr(0.05, 0.4, 0.5, 0.2, gate));\n"
    "filt = fi.lowpass(3, max(100, sweep), supersaw);\n"
    "process = filt * swell * 0.35 <: _, _;\n"
    "effect = _;\n"
)

SYNTH_MAP = {
    "pad": FAUST_PAD, "pluck": FAUST_PLUCK, "bass": FAUST_BASS,
    "arpegio": FAUST_ARPEGIO, "lead": FAUST_LEAD,
}

VOICES_MAP = {"pad": 6, "pluck": 6, "bass": 3, "arpegio": 6, "lead": 4}
DEFAULT_GAIN = {"pad": 0.25, "pluck": 0.18, "bass": 0.28, "arpegio": 0.20,
                "lead": 0.22, "drums": 0.34, "ambient": 0.28}

# ─── EFECTOS FAUST ───────────────────────────────────────────────────

FAUST_SATURATION = (
    'import("stdfaust.lib");\n'
    "gain = nentry(\"gain\", 0.5, 0, 1, 0.01);\n"
    "drive = nentry(\"drive\", 2.0, 0.5, 10, 0.1);\n"
    "process = (_ * drive) / (1 + abs(_ * drive)) * gain <: _, _;\n"
    "effect = _;\n"
)

FAUST_CHORUS = (
    'import("stdfaust.lib");\n'
    "gain = nentry(\"gain\", 0.5, 0, 1, 0.01);\n"
    "mix = nentry(\"mix\", 0.45, 0, 1, 0.01);\n"
    "wetL = _ : ef.echo(0.5, 0.015, 0.0) : _;\n"
    "wetR = _ : ef.echo(0.5, 0.023, 0.0) : _;\n"
    "wet = wetL + wetR;\n"
    "process = (_ * (1 - mix) + wet * mix) * gain <: _, _;\n"
    "effect = _;\n"
)

FAUST_DELAY_FB = (
    'import("stdfaust.lib");\n'
    "gain = nentry(\"gain\", 0.5, 0, 1, 0.01);\n"
    "fb = nentry(\"feedback\", 0.3, 0, 0.85, 0.01);\n"
    "mix = nentry(\"mix\", 0.4, 0, 1, 0.01);\n"
    "wet = _ : ef.echo(1.0, 0.25, fb) : _;\n"
    "process = (_ * (1 - mix) + wet * mix) * gain <: _, _;\n"
    "effect = _;\n"
)

FAUST_DELAY_RETURN = (
    'import("stdfaust.lib");\n'
    "fb = nentry(\"fb\", 0.3, 0, 0.85, 0.01);\n"
    "t = nentry(\"t\", 0.25, 0.05, 1.0, 0.01);\n"
    "wet = _ : ef.echo(1.0, t, fb) : _;\n"
    "process = wet , wet;\n"
    "effect = _;\n"
)

FAUST_AUTO_GAIN = (
    'import("stdfaust.lib");\n'
    "gain = nentry(\"gain\", 1.0, 0, 1, 0.01);\n"
    "process = _ * gain , _ * gain;\n"
    "effect = _;\n"
)

FAUST_AUTO_FILTER = (
    'import("stdfaust.lib");\n'
    "cut = nentry(\"cut\", 5000, 50, 12000, 1);\n"
    "process = fi.lowpass(3, cut, _) , fi.lowpass(3, cut, _);\n"
    "effect = _;\n"
)

FAUST_SIDECHAIN = (
    'import("stdfaust.lib");\n'
    "process(L, R, sc) = L * gain, R * gain\n"
    "with {\n"
    "  env = abs(sc) : fi.one_pole(0.003, 0.997);\n"
    "  threshold = 0.05;\n"
    "  red = max(0.0, env - threshold) * 3.0;\n"
    "  gain = 1.0 - min(1.0, red);\n"
    "};\n"
)

# ─── VALIDACION ──────────────────────────────────────────────────────

def validar_nota(nota):
    return max(MIDI_MIN, min(MIDI_MAX, int(round(nota))))

def validar_partitura(partitura):
    p = partitura
    p["bpm"] = max(BPM_MIN, min(BPM_MAX, int(p.get("bpm", 90))))
    p["compases"] = max(COMPASES_MIN, min(COMPASES_MAX, int(p.get("compases", 16))))
    max_beats = p["compases"] * 4.0

    validos = []
    for trk in p.get("tracks", []):
        tipo = trk.get("tipo", "")
        if tipo not in SYNTH_MAP and tipo not in ("drums", "ambient"):
            continue
        ganancia = max(0.0, min(GANANCIA_MAX, float(trk.get("ganancia", 0.25))))
        if tipo == "drums":
            patron = {}
            for key in ("kick", "snare", "hat", "clap", "rim"):
                pat = trk.get(key, [])
                patron[key] = [round(float(x), 2) for x in pat
                               if isinstance(x, (int, float)) and 0 <= x < 4]
            if not any(patron.values()):
                patron = {"kick": [0, 1, 2, 3], "snare": [1, 3],
                          "hat": [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]}
            track = {"tipo": "drums", "ganancia": ganancia,
                     "swing": float(trk.get("swing", 0.0)),
                     "velocity": float(trk.get("velocity", 0.8)),
                     **patron}
        elif tipo == "ambient":
            track = {"tipo": "ambient", "ganancia": ganancia,
                     "audios": trk.get("audios", [])}
        else:
            eventos = []
            for ev in trk.get("notas", []):
                if not isinstance(ev, (list, tuple)) or len(ev) < 3:
                    continue
                nota, start, dur = ev[0], ev[1], ev[2]
                start = max(0.0, float(start))
                dur = max(0.1, float(dur))
                if start >= max_beats:
                    continue
                if start + dur > max_beats:
                    dur = max_beats - start
                eventos.append([validar_nota(nota), round(start, 2), round(dur, 2)])
            if not eventos:
                continue
            track = {"tipo": tipo, "ganancia": ganancia, "notas": eventos}
            for opt in ("fx", "send", "automation"):
                if opt in trk and isinstance(trk[opt], (dict, list)):
                    track[opt] = trk[opt]
        validos.append(track)

    p["tracks"] = validos or [
        {"tipo": "pad", "ganancia": 0.25,
         "notas": [[69, 0, 8], [72, 0, 8], [76, 0, 8]]},
        {"tipo": "bass", "ganancia": 0.28,
         "notas": [[45, 0, 4], [48, 4, 4]]},
    ]
    return p

# ─── DRUMS ───────────────────────────────────────────────────────────

def synth_kick(sr, dur, f0=110.0, f1=45.0):
    n = int(sr * dur)
    t = np.linspace(0, dur, n, endpoint=False)
    freq = f1 + (f0 - f1) * np.exp(-t * 25)
    phase = 2 * np.pi * np.cumsum(freq) / sr
    env = np.exp(-t * 12)
    return (np.sin(phase) * env).astype("float32")

def synth_snare(sr, dur, rng):
    n = int(sr * dur)
    t = np.linspace(0, dur, n, endpoint=False)
    noise = rng.standard_normal(n) * np.exp(-t * 30)
    tone = np.sin(2 * np.pi * 180 * t) * np.exp(-t * 40)
    return (0.7 * noise + 0.3 * tone).astype("float32")

def synth_hat(sr, dur, rng):
    n = int(sr * dur)
    noise = rng.standard_normal(n)
    hp = np.diff(noise, prepend=0)
    env = np.exp(-np.linspace(0, dur, n) * 70)
    return (hp * env * 0.35).astype("float32")

def _aplicar_swing(puntos, swing):
    if swing <= 0:
        return puntos
    out = []
    for p in puntos:
        frac = p - int(p)
        if abs(frac - 0.5) < 0.001:
            out.append(p + swing * 0.5)
        else:
            out.append(p)
    return out

def renderizar_drums(patron, bpm, compases):
    beats_tot = compases * 4
    beat = 60.0 / bpm
    total = int(SR * (beat * beats_tot))
    rng = np.random.default_rng(42)
    swing = patron.get("swing", 0.0)
    velocity = patron.get("velocity", 0.8)

    HIT_CONFIGS = [
        ("kick", 0.35, 20, 45), ("snare", 0.25, 30, 180),
        ("hat", 0.06, 70, None), ("clap", 0.15, 50, 250),
        ("rim", 0.08, 60, None),
    ]

    layers = {}
    for patron_key in ("kick", "snare", "hat", "clap", "rim"):
        offsets = _aplicar_swing(patron.get(patron_key, []), swing)
        dur_s = next((c[1] for c in HIT_CONFIGS if c[0] == patron_key), 0.15)
        capa = np.zeros(total, dtype="float32")
        for comp in range(compases):
            for off in offsets:
                s0 = (comp * 4 + off) * beat * SR
                s = int(s0)
                e = s + int(dur_s * SR)
                if e > total: e = total
                if s >= total: continue
                vel = velocity * (0.85 + 0.15 * rng.random())
                if patron_key == "kick":
                    seg = synth_kick(SR, dur_s)
                elif patron_key == "snare":
                    seg = synth_snare(SR, dur_s, rng)
                elif patron_key == "hat":
                    seg = synth_hat(SR, dur_s, rng)
                elif patron_key == "clap":
                    seg = synth_snare(SR, dur_s, rng) * 0.5
                elif patron_key == "rim":
                    seg = synth_hat(SR, dur_s, rng) * 0.3
                else:
                    continue
                capa[s:e] += seg[:e - s] * vel
        layers[patron_key] = capa

    ghost_hats = []
    for comp in range(compases):
        for frac in [0.25, 0.75, 1.25, 1.75, 2.25, 2.75, 3.25, 3.75]:
            base = comp * 4 + frac
            existing = patron.get("hat", [])
            if not any(abs(e - frac) < 0.1 for e in existing):
                ghost_hats.append(base)
    for pos in ghost_hats:
        s = int(pos * beat * SR)
        e = s + int(0.04 * SR)
        if e >= total: continue
        vel = 0.08 + 0.06 * rng.random()
        seg = synth_hat(SR, 0.04, rng)
        layers["hat"][s:e] += seg[:e - s] * vel

    out = sum(layers.values())
    pico = float(np.abs(out).max())
    if pico > 0: out /= pico
    mixed = np.stack([out, out], axis=0)
    kick = np.stack([layers["kick"], layers["kick"]], axis=0)
    return mixed, kick

# ─── AMBIENT ─────────────────────────────────────────────────────────

def cargar_ambient(rutas, duracion):
    import librosa
    total = int(SR * duracion)
    out = np.zeros((2, total), dtype="float32")
    for ruta in rutas:
        if not os.path.isfile(ruta):
            print(f"  [WARN] Audio no encontrado: {ruta}")
            continue
        sig, _ = librosa.load(ruta, sr=SR, mono=True)
        if sig.size == 0: continue
        sig = sig.astype("float32")

        if sig.size > SR * 0.5:
            stretch = librosa.effects.time_stretch(sig, rate=0.77)
            winsize = int(0.5 * SR)
            total_frames = total
            acum = np.zeros(total_frames, dtype="float32")
            weight = np.zeros(total_frames, dtype="float32")
            pos = 0
            while pos < total_frames:
                chunk = stretch[pos % stretch.size: (pos % stretch.size) + winsize]
                if chunk.size < winsize:
                    chunk = np.pad(chunk, (0, winsize - chunk.size))
                window = np.hanning(winsize)
                end = min(pos + winsize, total_frames)
                chunk_len = end - pos
                acum[pos:end] += chunk[:chunk_len] * window[:chunk_len] * 0.6
                weight[pos:end] += window[:chunk_len] * 0.6 + 0.4
                pos += winsize // 2
            mask = weight > 0
            acum[mask] /= weight[mask]
            sig = acum
        else:
            rep = max(1, math.ceil(total / sig.size))
            sig = np.tile(sig, rep)[:total]

        delay = int(0.015 * SR)
        L = sig[:total]
        R = np.pad(sig[:-delay] if delay < sig.size else sig,
                   (delay if delay < sig.size else 0, 0))[:total]
        out[0, :len(L)] += L
        out[1, :len(R)] += R

    pico = float(np.abs(out).max())
    if pico > 0: out /= pico
    return out

# ─── AUTOMATION ──────────────────────────────────────────────────────

def build_automation(nframes, points):
    if len(points) < 2:
        return np.full(nframes, points[0][1] if points else 0.0)
    max_beat = float(points[-1][0])
    beats_per_frame = max_beat / max(nframes, 1)
    x = np.arange(nframes, dtype=float) * beats_per_frame
    beats = np.array([p[0] for p in points], dtype=float)
    vals = np.array([p[1] for p in points], dtype=float)
    return np.interp(x, beats, vals).astype(np.float32)

# ─── RENDER ─────────────────────────────────────────────────────────

AUTO_PROFILES = {
    "pad": [(FAUST_AUTO_FILTER, [("cut", [(0, 300), (16, 1200), (32, 5000), (48, 7000)])])],
    "bass": [(FAUST_AUTO_FILTER, [("cut", [(0, 150), (24, 600)])])],
    "arpegio": [(FAUST_AUTO_GAIN, [("gain", [(0, 0.3), (16, 0.5), (32, 0.7), (48, 0.5), (56, 0.3)])])],
}

FX_MAP = {
    "bass": [("sat", FAUST_SATURATION)],
    "pad": [("chorus", FAUST_CHORUS)],
    "lead": [("delay", FAUST_DELAY_FB)],
}

def render(partitura, output_path):
    import dawdreamer as daw
    from scipy.io import wavfile

    bpm = partitura["bpm"]
    compases = partitura["compases"]
    tracks = partitura["tracks"]
    beats_tot = compases * 4
    duracion = beats_tot * (60.0 / bpm)

    print(f"BPM: {bpm} | Compases: {compases} | Duracion: {duracion:.1f}s")
    print(f"Tracks: {[t['tipo'] for t in tracks]}")

    engine = daw.RenderEngine(SR, BUFFER_SIZE)
    engine.set_bpm(float(bpm))

    grafo = []
    mezcla = {}
    kick_proc_name = None
    rev_sends = []
    dly_sends = []
    nframes = int(SR * duracion / BUFFER_SIZE)
    cont = 0

    for trk in tracks:
        tipo = trk["tipo"]
        ganancia = trk.get("ganancia", DEFAULT_GAIN.get(tipo, 0.25))

        if tipo == "ambient":
            a = cargar_ambient(trk["audios"], duracion)
            dsp = engine.make_playback_processor(f"ambient_{cont}", a)
            grafo.append((dsp, []))
            mezcla[f"ambient_{cont}"] = ganancia
        elif tipo == "drums":
            patron = {k: trk.get(k, []) for k in ("kick", "snare", "hat", "clap", "rim")}
            patron["swing"] = trk.get("swing", 0.0)
            patron["velocity"] = trk.get("velocity", 0.8)
            d, kick = renderizar_drums(patron, bpm, compases)
            dsp = engine.make_playback_processor(f"drums_{cont}", d)
            kick_dsp = engine.make_playback_processor(f"kick_{cont}", kick)
            grafo.append((dsp, []))
            grafo.append((kick_dsp, []))
            mezcla[f"drums_{cont}"] = ganancia
            kick_proc_name = f"kick_{cont}"
        elif tipo in SYNTH_MAP:
            nombre = f"{tipo}_{cont}"
            dsp_str = SYNTH_MAP[tipo]
            nv = VOICES_MAP.get(tipo, 8)
            eventos = trk.get("notas", [])

            def _notas(p, evs=eventos):
                for nota, start, dur in evs:
                    p.add_midi_note(int(nota), 80, float(start), float(dur), beats=True)

            p = engine.make_faust_processor(nombre)
            p.set_dsp_string(dsp_str)
            p.num_voices = nv
            _notas(p)
            grafo.append((p, []))
            prev_name = nombre

            # Track-level automation override
            track_auto = trk.get("automation")
            if track_auto:
                for item in track_auto:
                    param = item.get("param", "")
                    points = item.get("points", [])
                    dsp = FAUST_AUTO_FILTER if param == "cutoff" else FAUST_AUTO_GAIN if param == "gain" else None
                    if not dsp: continue
                    fx_name = f"{nombre}_auto_{param}"
                    pp = engine.make_faust_processor(fx_name)
                    pp.set_dsp_string(dsp)
                    pts = [(float(a), float(b)) for a, b in points]
                    curve = build_automation(nframes, pts)
                    for d in pp.get_parameters_description():
                        pp.set_automation(d['name'], curve)
                        break
                    grafo.append((pp, [prev_name]))
                    prev_name = fx_name
            else:
                for fx_dsp, params_list in AUTO_PROFILES.get(tipo, []):
                    fx_name = f"{nombre}_auto"
                    pp = engine.make_faust_processor(fx_name)
                    pp.set_dsp_string(fx_dsp)
                    for param_name, points in params_list:
                        curve = build_automation(nframes, points)
                        for d in pp.get_parameters_description():
                            pp.set_automation(d['name'], curve)
                            break
                    grafo.append((pp, [prev_name]))
                    prev_name = fx_name

            # FX chain
            fx_config = trk.get("fx")
            if fx_config:
                for fx_type in ("compressor", "saturation", "chorus", "delay", "reverb"):
                    if fx_type in fx_config:
                        fx_name = f"{nombre}_{fx_type}"
                        fx_params = fx_config[fx_type] or {}
                        if fx_type == "compressor":
                            pp = engine.make_compressor_processor(fx_name)
                            pp.threshold = float(fx_params.get("threshold", -24))
                            pp.ratio = float(fx_params.get("ratio", 4))
                            pp.attack = float(fx_params.get("attack", 3))
                            pp.release = float(fx_params.get("release", 150))
                        elif fx_type == "chorus":
                            pp = engine.make_faust_processor(fx_name)
                            pp.set_dsp_string(FAUST_CHORUS)
                        elif fx_type == "saturation":
                            pp = engine.make_faust_processor(fx_name)
                            pp.set_dsp_string(FAUST_SATURATION)
                        elif fx_type == "delay":
                            pp = engine.make_faust_processor(fx_name)
                            pp.set_dsp_string(FAUST_DELAY_FB)
                        elif fx_type == "reverb":
                            pp = engine.make_reverb_processor(fx_name)
                            pp.room_size = float(fx_params.get("room", 0.3))
                            pp.damping = float(fx_params.get("damping", 0.5))
                            mix = float(fx_params.get("mix", 0.35))
                            pp.wet_level = mix
                            pp.dry_level = float(fx_params.get("dry", 1.0 - mix))
                            pp.width = float(fx_params.get("width", 0.7))
                        grafo.append((pp, [prev_name]))
                        prev_name = fx_name
            else:
                for fx_type, fx_dsp in FX_MAP.get(tipo, []):
                    fx_name = f"{nombre}_{fx_type}"
                    pp = engine.make_faust_processor(fx_name)
                    pp.set_dsp_string(fx_dsp)
                    grafo.append((pp, [prev_name]))
                    prev_name = fx_name
                if tipo == "pluck":
                    fx_name = f"{nombre}_verb"
                    pp = engine.make_reverb_processor(fx_name)
                    pp.room_size = 0.3; pp.damping = 0.5
                    pp.wet_level = 0.35; pp.dry_level = 0.65; pp.width = 0.7
                    grafo.append((pp, [prev_name]))
                    prev_name = fx_name

            # Sidechain
            prev_for_mixer = prev_name
            if kick_proc_name and tipo in ("bass", "pad"):
                sc_sum = engine.make_faust_processor(f"kick_sum_{tipo}_{cont}")
                sc_sum.set_dsp_string('import("stdfaust.lib"); process = _ + _;')
                grafo.append((sc_sum, [kick_proc_name]))
                sc = engine.make_faust_processor(f"sc_{prev_name}")
                sc.set_dsp_string(FAUST_SIDECHAIN)
                grafo.append((sc, [prev_name, f"kick_sum_{tipo}_{cont}"]))
                mezcla[f"sc_{prev_name}"] = ganancia
                prev_for_mixer = f"sc_{prev_name}"
            else:
                mezcla[prev_name] = ganancia

            # Send to buses
            sends = trk.get("send", {})
            if sends.get("reverb", 0) > 0:
                rev_sends.append((prev_for_mixer, sends["reverb"]))
            if sends.get("delay", 0) > 0:
                dly_sends.append((prev_for_mixer, sends["delay"]))
        cont += 1

    if not grafo:
        raise RuntimeError("No hay tracks para renderizar")

    graph_nodes = [(p, inputs or []) for p, inputs in grafo]

    # Reverb bus
    if rev_sends:
        rev_names = [n for n, _ in rev_sends]
        rev_weights = [w for _, w in rev_sends]
        rev_bus = engine.make_add_processor("rev_bus", rev_weights)
        rev_ret = engine.make_reverb_processor("rev_return")
        rev_ret.room_size = 0.6; rev_ret.damping = 0.4
        rev_ret.wet_level = 0.5; rev_ret.dry_level = 0.0; rev_ret.width = 1.0
        rev_mod = engine.make_faust_processor("rev_mod")
        rev_mod.set_dsp_string(FAUST_AUTO_GAIN)
        rev_curve = build_automation(nframes, [(0, 0.3), (24, 0.6), (48, 0.4)])
        for d in rev_mod.get_parameters_description():
            rev_mod.set_automation(d['name'], rev_curve)
            break
        graph_nodes += [(rev_bus, rev_names), (rev_ret, ["rev_bus"]), (rev_mod, ["rev_return"])]
        mezcla["rev_mod"] = 0.55

    # Delay bus
    if dly_sends:
        dly_names = [n for n, _ in dly_sends]
        dly_weights = [w for _, w in dly_sends]
        dly_bus = engine.make_add_processor("dly_bus", dly_weights)
        dly_ret = engine.make_faust_processor("dly_return")
        dly_ret.set_dsp_string(FAUST_DELAY_RETURN)
        graph_nodes += [(dly_bus, dly_names), (dly_ret, ["dly_bus"])]
        mezcla["dly_return"] = 0.4

    # Mixer and master
    keys = list(mezcla.keys())
    mixer = engine.make_add_processor("mixer", [mezcla[k] for k in keys])
    master_mod = engine.make_faust_processor("master_mod")
    master_mod.set_dsp_string(FAUST_AUTO_GAIN)
    master_curve = build_automation(nframes, [(0, 0.7), (16, 0.8), (40, 1.0), (56, 0.9)])
    for d in master_mod.get_parameters_description():
        master_mod.set_automation(d['name'], master_curve)
        break
    master_verb = engine.make_reverb_processor("master_verb")
    master_verb.room_size = 0.3; master_verb.damping = 0.5
    master_verb.wet_level = 0.12; master_verb.dry_level = 0.88; master_verb.width = 0.5

    engine.load_graph(
        graph_nodes +
        [(mixer, keys),
         (master_mod, ["mixer"]),
         (master_verb, ["master_mod"])]
    )

    print("Renderizando...")
    engine.render(beats_tot, beats=True)
    audio = engine.get_audio()

    pico = float(np.abs(audio).max())
    if pico > 0:
        audio = audio * (0.89 / pico)
        audio = np.clip(audio, -1.0, 1.0)

    wavfile.write(output_path, SR, (audio.T * 32767).astype(np.int16))
    print(f"[OK] {output_path}")


# ─── RUNNER ──────────────────────────────────────────────────────────

def run(build_partitura_fn):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    import glob
    existentes = sorted(
        (int(os.path.splitext(os.path.basename(f))[0])
         for f in glob.glob(os.path.join(OUTPUT_DIR, "[0-9]*.wav"))),
    )
    n = (existentes[-1] + 1) if existentes else 1
    output_path = os.path.join(OUTPUT_DIR, f"{n}.wav")
    partitura = build_partitura_fn()
    partitura = validar_partitura(partitura)
    render(partitura, output_path)
    return output_path