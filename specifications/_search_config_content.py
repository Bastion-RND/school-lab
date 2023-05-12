import json
import re

from pathlib import Path


if __name__ == '__main__':
    paths = sorted(Path('.').glob('*.json'))
    for path in paths:
        if re.match('^\w{8}\.spec\.json$', str(path)):
            with open(path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                print(f'{path} --> {config.get("description")}')
