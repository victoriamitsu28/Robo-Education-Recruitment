"""Run before class to check the interpreter and installed course dependencies."""
import importlib
from importlib.metadata import PackageNotFoundError, version
import json
import platform
import sys


def main():
    report = {'python': platform.python_version(), 'python_minimum': '3.11'}
    problems = []
    if sys.version_info < (3, 11):
        problems.append('Use Python 3.11 or later; Python 3.12 is recommended.')
    for package, module, expected in [
        ('numpy', 'numpy', '2.3.5'),
        ('opencv-python-headless', 'cv2', '5.0.0.93'),
    ]:
        try:
            installed = version(package)
            loaded = importlib.import_module(module)
            report[package] = {'package_version': installed, 'module_version': loaded.__version__}
            if installed != expected:
                problems.append(f'{package}: expected {expected}, found {installed}. Reinstall requirements.txt.')
        except (PackageNotFoundError, ImportError) as exc:
            report[package] = {'error': str(exc)}
            problems.append(f'{package} is missing or cannot be imported. Install requirements.txt in this interpreter.')
    report['ready'] = not problems
    report['problems'] = problems
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not problems else 1


if __name__ == '__main__':
    raise SystemExit(main())
