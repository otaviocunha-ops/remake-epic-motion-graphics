# Contributing

Keep scene state a deterministic function of the frame. Preserve the upstream snapshot and its checksums. Add film-specific behavior to shared helpers, not core.js. Keep subprocess arguments as lists, avoid shell=True and respect paths with spaces. Never commit personal paths, API keys, source footage, installed dependencies or rendered film frames.

Run `python -m unittest discover -s tests -v`, then the bootstrap and demo smoke sequence from README in a fresh temporary directory with spaces. Test failure cases as well as happy paths. Report the platforms actually tested; a CI configuration is not a passing CI run. Documentation changes must keep Portuguese and English commands consistent.
