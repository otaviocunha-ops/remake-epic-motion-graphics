"""Find ffmpeg: env FFMPEG (path to the binary) wins, else `ffmpeg` on PATH."""
import os
import shutil


def ffmpeg_bin():
    ff = os.environ.get('FFMPEG') or shutil.which('ffmpeg')
    if not ff or not os.path.exists(ff):
        raise SystemExit('ffmpeg not found: install it (brew install ffmpeg / apt install ffmpeg) or set FFMPEG=/path/to/ffmpeg')
    return os.path.abspath(ff)


def ffmpeg_cwd():
    """Some portable ffmpeg builds load their libraries relative to their own folder, so ffmpeg runs from there.
    Every path passed to ffmpeg is absolute, so this has no effect on a normal install."""
    return os.path.dirname(ffmpeg_bin())
