# AGENTS.md

Proyecto de aprendizaje de sintesis y render de audio con [DAWdreamer](https://github.com/DBraun/DAWdreamer),
usando DSP en Faust embebido como strings de Python. No hay tests ni build: cada
script se ejecuta directamente y genera un `.wav`.

## Estructura

- `engine.py` — motor generico compartido por los scripts de cancion de nivel raiz
  (`1_simple_synth.py`, `2_techno.py`, `3_marea_baja.py`, `4_lush_pad_ambient.py`).
  Cada uno de esos scripts solo define `build_partitura()` (o su propia logica en
  `3_marea_baja.py`/`4_lush_pad_ambient.py`) y llama a `run()`/renderiza con `engine.py`.
- `pads/`, `bass/`, `leads/`, `pluck/` — librerias de presets Faust por categoria de
  timbre. Cada carpeta tiene su propio `common.py` con:
  - la misma progresion armonica base (vi-IV-I-V en Do mayor: Am-F-C-G) a 100 BPM,
    adaptada al rol de la carpeta (pad = acorde sostenido, bass = patron sincopado
    con la raiz una octava abajo, leads = melodia diatonica monofonica, pluck =
    arpegio en corcheas).
  - una funcion `render_<categoria>(nombre, dsp_string, ...)` generica que cada
    preset invoca pasandole solo su string de DSP Faust.
  Cada preset (`<nombre>.py`) define su propio `FAUST_*` string y, en
  `if __name__ == "__main__":`, llama a la funcion de render de `common.py`.
- `*/output/` — WAVs generados (ignorados por git, ver `.gitignore`).
- `samples/` — `loops/` y `one-shots/` para muestras de audio (si se usan).
- `download_vital.md` — enlace temporal con token personal, ignorado por git; no
  editarlo ni subirlo nunca a git ni a ningun servicio externo.

## Convenciones

- Los comentarios, docstrings y mensajes de commit de este repo estan en
  **castellano**. Sigue ese idioma al tocar este codigo.
- Los rangos de MIDI, BPM y compases estan acotados por constantes en
  `engine.py` (`MIDI_MIN`/`MIDI_MAX`, `BPM_MIN`/`BPM_MAX`,
  `COMPASES_MIN`/`COMPASES_MAX`) — respetalos al generar nuevas piezas.
- Al anadir un preset nuevo en `pads/`, `bass/`, `leads/` o `pluck/`: crear
  `<carpeta>/<nombre>.py` que importe la funcion de render de `common.py` de esa
  carpeta y solo aporte el string Faust (`FAUST_...`) y la llamada final en
  `if __name__ == "__main__":`. No dupliques la logica de render ni la
  progresion armonica: esas viven en `common.py`.
- Los presets basados en Karplus-Strong para pluck fueron eliminados por sonar
  "clicky" (ver commit `0015fa7`) — no reintroducir ese enfoque sin resolver
  antes el artefacto de sonido.

## Como ejecutar

No hay entorno virtual ni `requirements.txt` en el repo; se asume que
`dawdreamer`, `numpy` y `scipy` ya estan instalados en el Python activo.

```bash
python 3_marea_baja.py          # renderiza output/3.wav
python pads/dark_pad.py         # renderiza pads/output/dark_pad.wav
```

No hay suite de tests. Para verificar un cambio, ejecuta el script afectado y
escucha (o inspecciona con una libreria de audio) el `.wav` resultante en la
carpeta `output/` correspondiente.
