import PyInstaller.__main__
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'college_planner.py',
    '--name=SmartCollegePlanner',
    '--onefile',
    '--windowed',
    '--add-data=README.md;.',
    '--icon=NONE',
    '--clean',
    '--noconfirm',
    f'--distpath={os.path.join(current_dir, "dist")}',
    f'--workpath={os.path.join(current_dir, "build")}',
    f'--specpath={current_dir}',
]) 