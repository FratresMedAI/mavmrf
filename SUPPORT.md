# Support

MAVMRF is a **portfolio / research prototype**. There is no commercial support SLA.

## Where to get help

| Need | Where |
|------|--------|
| Bug report | [GitHub Issues](https://github.com/FratresMedAI/mavmrf/issues) (bug template) |
| Feature idea | [GitHub Issues](https://github.com/FratresMedAI/mavmrf/issues) (feature template) |
| How to run / contribute | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Architecture | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Security vulnerability | [SECURITY.md](SECURITY.md) — report privately |

Before opening an issue, check existing issues and try a fresh clone with:

```bash
cd marmf
pip install -r requirements.txt -r requirements-dev.txt
pip install -e .
pytest tests -q
python main.py --mode monitor --no-trained --duration 2
```
