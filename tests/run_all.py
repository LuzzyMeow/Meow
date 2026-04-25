import subprocess
import sys
import os

tests_dir = os.path.join(os.path.dirname(__file__))
meow_files = sorted([f for f in os.listdir(tests_dir) if f.endswith('.meow')])

passed = 0
failed = 0
errors = []

for f in meow_files:
    path = os.path.join(tests_dir, f)
    result = subprocess.run(
        [sys.executable, '-m', 'bootstrap.main', path],
        capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(__file__)))
    if result.returncode == 0:
        print(f'  PASS  {f}')
        passed += 1
    else:
        print(f'  FAIL  {f}')
        print(f'        {result.stderr.strip().splitlines()[-1] if result.stderr else result.stdout.strip().splitlines()[-1]}')
        failed += 1
        errors.append(f)

print(f'\nResults: {passed} passed, {failed} failed, {passed + failed} total')
if errors:
    print(f'Failed: {", ".join(errors)}')
    sys.exit(1)
