<p align="center"><img src="docs/cover.svg" alt="Remake Epic Motion Graphics — a frame-driven editing timeline" width="920"></p>

# Remake Epic Motion Graphics

An agent skill and portable toolkit for rebuilding motion graphics from a reference video, with measured timing, brand swaps and synchronized visual comparisons.

[Leia em português](README.pt-BR.md) · [Skill instructions](SKILL.md) · [Quality guide](references/quality.md) · [Inputs](references/inputs.example.json)

This is a reconstruction workflow, **not a one-click video cloning model**. An agent measures the reference, implements scenes in HTML/SVG and checks the rendered poses. It includes the engine, templates, specification example, installer, analysis CLI and an original runnable demo. There is no dependency on the owner's local toolkit folder.

## Install and run

```sh
git clone https://github.com/psiotavio/remake-epic-motion-graphics.git
cd remake-epic-motion-graphics
```



Download/clone this repository. Use Python 3.10–3.14, Node.js 20+ and FFmpeg (including ffprobe). Install FFmpeg with your OS package manager; details are in [runtime](references/runtime.md).

```sh
python scripts/bootstrap.py
```

On macOS/Linux, use `python3` if `python` is unavailable. Then use `.venv/bin/python`; on Windows use `.venv\Scripts\python.exe`. The commands below assume that virtual environment is activated, or that you replace `python` with its full interpreter path.

```sh
python scripts/remake.py doctor
python scripts/remake.py demo --output "films/demo"
python scripts/remake.py analyze "films/demo"
python scripts/remake.py render "films/demo" --frames 0,12,24,36,48,59
python scripts/remake.py render "films/demo" --full
python scripts/remake.py verify "films/demo"
python scripts/remake.py encode "films/demo"
python scripts/remake.py sync "films/demo"
```

The demo creates its own reference video from procedural graphics and a synthesized tone. `films/demo/demo.mp4` and `films/demo/out/side-by-side.mp4` are the final outputs. Single-sample rendering is included; true multi-sample shutter blur is documented as a film extension, not silently claimed as included.

## Install as a skill

```sh
python scripts/install_skill.py --agent codex
python scripts/install_skill.py --agent claude
python scripts/install_skill.py --agent custom --dest "/path/to/agent/skills"
```

The installer copies the whole package, excluding dependencies/generated files, into a canonical `remake-epic-motion-graphics` folder. It refuses to overwrite an existing installation. Codex uses ~/.agents/skills; Claude uses ~/.claude/skills. Custom accepts any skills directory. For other agents, consult their current skill-discovery mechanism; any tool-capable agent can read SKILL.md manually. Run bootstrap inside the installed copy when its runtime is needed. Chat-only assistants cannot execute the workflow by themselves.

## Recreate your video

> Use remake-epic-motion-graphics with my reference video. Keep cuts, motion and layout, replace the brand/logo/palette/UI with my supplied assets, and show the measured shot table before building.

```sh
python scripts/remake.py init --reference "/path/to/reference.mp4" --output "films/my-film" --name "My Brand"
python scripts/remake.py analyze "films/my-film"
```

Complete film.json, SPEC.md and the measurements. Implement shots using engine/core.js and the [quality rules](references/quality.md). Supply local fonts and media; the scaffold does not generate your product UI. `analyze` rejects variable-frame-rate and rotated references until you explicitly normalize them. No TTS, transcription or commercial music account is bundled. First-time setup downloads dependencies; local rendering then works offline.

## Repository

```text
SKILL.md                  Model-neutral agent workflow
agents/                   Optional agent display metadata
scripts/                  Bootstrap, installer, portable CLI
engine/                   Core, renderer, utilities and upstream snapshot
prompts/                  Nine original brief/script/remake templates
playbook/                 Original craft and pipeline guides
examples/                 GOJI specification and source examples
references/               Measurement, quality, runtime, input contract
docs/                     Cover and publication guide
tests/                    Unit and end-to-end smoke checks
.github/workflows/        macOS/Linux/Windows CI
Dockerfile                Optional Linux rendering environment
```

## Acceptance and limitations

The goal in strict mode is zero-frame cut/typing/cursor offsets and geometry error ≤1% per frame dimension. These are measured acceptance criteria, not an automatic guarantee. Structural verification does not certify visual similarity; inspect side-by-side images and record remaining differences. Native SVG motion is sought by frame, text shares stable baselines, holds stay sharp and UI components have measured final positions. Adaptations are listed explicitly.

The runtime is designed for macOS, Linux and Windows. CI is provided for all three; see [validation](docs/VALIDATION.md) for what was actually run. Cross-OS font rasterization can differ. Bundled toolkit material has no stated upstream license; [notices](THIRD_PARTY_NOTICES.md) separate it from the MIT-licensed original additions. No private Nola assets or reference media are included.

See [Contributing](CONTRIBUTING.md) and [GitHub publication](docs/PUBLISHING.md).
