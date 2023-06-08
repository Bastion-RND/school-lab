import json
import re

from pathlib import Path


if __name__ == '__main__':
    result = dict()
    paths = sorted(Path('.').glob('*.json'))
    for path in paths:
        if re.match('^\w{8}\.spec\.json$', str(path)):
            with open(path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                result[config.get('description')] = path

    descriptions = list(result.keys())
    descriptions.sort()

    for key in descriptions:
        print(f'{result[key]} --> {key}')
