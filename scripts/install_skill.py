"""Copy a self-contained skill without dependencies, private films or symlinks."""
import argparse, shutil
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--agent',choices=['codex','claude','custom'],default='codex')
    p.add_argument('--dest',type=Path)
    a=p.parse_args()
    base=a.dest
    if a.agent=='custom' and base is None: p.error('--dest is required for custom')
    if base is None: base=Path.home()/('.agents/skills' if a.agent=='codex' else '.claude/skills')
    target=base.expanduser().resolve()/'remake-epic-motion-graphics'
    source=Path(__file__).resolve().parents[1]
    if target.exists(): p.error(f'Refusing to overwrite {target}')
    if source==target or source in target.parents: p.error('Destination cannot be inside the source repository')
    shutil.copytree(source,target,ignore=shutil.ignore_patterns('.git','.venv','node_modules','films','__pycache__','*.pyc','.DS_Store','*.zip'))
    print(target)

if __name__=='__main__': main()
