# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-07-19

### Added

- Simulation-first detection policy (YOLO opt-in via train / `--pretrained` / `--weights`)
- IoU matching for optical detections and track ID attachment (`utils/bbox.py`)
- Synthetic YOLO dataset generator (`scripts/generate_dataset.py`)
- Pytest suite, ruff lint, GitHub Actions CI (`.github/workflows/tests.yml`)
- Editable install via `marmf/pyproject.toml` (`pip install -e marmf`)
- Demo scripts (`scripts/demo.ps1`, `scripts/demo.sh`) — local clone-and-run path
- README demo GIF + `scripts/make_demo_gif.py`
- Seeded benchmark gates (`scripts/benchmark.py`, `docs/benchmarks/`)
- Architecture docs, optical replay fixture with sidecar JPG
- Open-source community kit: SECURITY, Code of Conduct, SUPPORT, issue/PR templates, Dependabot, CITATION.cff
- Design tradeoffs / next-steps narrative aligned with Fratres X AI

### Changed

- Default monitor duration reduced for demos
- Reports include `detection_source` on every frame
- Root README and CONTRIBUTING updated for cross-platform setup
- CI actions bumped to `checkout@v5` / `setup-python@v6` (Node 20 deprecation)
- README: release badge, Related Fratres X threads, clone-and-run posture line


## [0.1.0] - 2026-05-26

### Added

- Initial public portfolio release of MAVMRF
- Multi-sensor simulation (sonar, acoustic, optical, magnetic)
- SORT-style tracking, weighted fusion, operator JSON reports
- MIT license and baseline documentation

[0.2.0]: https://github.com/Fratres-X-AI/mavmrf/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/Fratres-X-AI/mavmrf/releases/tag/v0.1.0
