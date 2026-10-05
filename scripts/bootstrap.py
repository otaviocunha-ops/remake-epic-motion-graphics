"""Install project-local dependencies; never modify system package managers."""
from pathlib import Path
import subprocess, sys, shutil, venv

def main():
    root = Path(__file__).resolve().parents[1]
    npm = shutil.which('npm.cmd' if sys.platform == 'win32' else 'npm')
    node = shutil.which('node')
    if not npm or not node:
        raise SystemExit('Install Node.js 20+ (including npm) first.')
    if not (3,10) <= sys.version_info[:2] <= (3,14):
        raise SystemExit('Python 3.10–3.14 required.')
    venv.EnvBuilder(with_pip=True).create(root/'.venv')
    py = root/'.venv'/('Scripts/python.exe' if sys.platform == 'win32' else 'bin/python')
    subprocess.run([str(py),'-m','pip','install','--only-binary=:all:','-r',str(root/'requirements.txt')],check=True)
    # npm is a .cmd file on Windows; cmd.exe must interpret that wrapper.
    command=[npm,'ci']
    if sys.platform=='win32': command=['cmd.exe','/d','/s','/c',subprocess.list2cmdline(command)]
    subprocess.run(command,cwd=root,check=True)
    subprocess.run([node,str(root/'node_modules/playwright/cli.js'),'install','chromium'],cwd=root,check=True)
    print('Ready. Run:',str(py),'scripts/remake.py doctor')

if __name__=='__main__': main()
