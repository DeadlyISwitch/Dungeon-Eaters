# Dungeon Eaters

Proyecto Python + pygame-ce inspirado en survivor-likes con arquitectura ECS-lite, estados de juego, contenido JSON data-driven, gráficos 100% procedurales y sistema robusto de guardado con hash + backup + migraciones.

## Requisitos
- Python 3.11+
- Windows 10 (también funciona en Linux/macOS)

## Instalación
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución
```bash
python -m game
# o
python main.py
```

## Controles
- WASD: movimiento
- ESC: salir/volver
- F3: overlay debug FPS
- F11: fullscreen (en Settings)
- Menú nivel-up: teclas 1..4
- BuildLab: R auto-fill, S guarda preset, E exporta, I importa

## Cómo añadir contenido JSON
1. Abre `game/data/items/weapons.json`.
2. Agrega un objeto con `id`, `name`, `tags`, `base_stats`, `scaling`, `pattern_type`, `evolution`, `icon_spec`.
3. Mantén IDs únicos y referencias válidas (por ejemplo `needs_passive` existente).
4. Repite para pasivas/enemigos en sus respectivos JSON.
5. Reinicia el juego (carga en startup con validación ligera de esquema).

## Save version y migraciones
- El perfil se guarda en `saves/profile.json` con estructura:
  - `payload`: datos versionados (`save_version`)
  - `hash`: SHA-256 del payload serializado
- Si falla hash o se corrompe, se intenta recuperar `saves/profile.bak`.
- Si ambos fallan, usa defaults (`game/save/defaults.py`).
- Migraciones se aplican en `game/save/migrations.py` (ejemplo v1 -> v2).

## BuildLab
- Editor de build (personaje/meta objetivo + slots).
- Analyzer: calcula sinergias por tags y estado de evoluciones.
- Recommender: genera 3 builds (standard/offense/safe).
- Comparador y export/import compactado (base64+zlib) en módulos dedicados.
- Presets persistidos en el perfil.

## Estructura
Ver carpetas bajo `game/`:
- `core/`: app loop, fixed timestep, input, machine de estados.
- `ecs/`: world + systems (movimiento, IA, spawns, combate, loot, render UI).
- `procedural/`: shapes, sprites, iconos, partículas, fondo, paletas.
- `data/`: loader + schema + JSON de contenido.
- `meta/`: progresión, unlocks, cosméticos.
- `buildlab/`: analyzer, recommender, compare, export/import, UI.
- `save/`: defaults, migraciones, manager robusto.

