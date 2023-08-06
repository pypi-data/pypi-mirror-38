# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['pyartifact', 'pyartifact.deck_encoding', 'pyartifact.types']

package_data = \
{'': ['*']}

install_requires = \
['mypy_extensions>=0.4.1,<0.5.0', 'requests>=2.20,<3.0']

setup_kwargs = {
    'name': 'pyartifact',
    'version': '0.3.1',
    'description': "Pythonic wrapper around Valve's Artifact API",
    'long_description': '# pyArtifact\n\nPythonic wrapper around Valve\'s Artifact API, with object mapping, filtering and hopefully more\n\nCurrent phase: **prototype** -> very unstable API\n\n[![MIT License](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://opensource.org/licenses/MIT)\n[![pypi version](https://badge.fury.io/py/pyartifact.svg)](https://badge.fury.io/py/pyartifact)\n[![Documentation Status](https://readthedocs.org/projects/pyartifact/badge/?version=latest)](https://pyartifact.readthedocs.io/en/latest/?badge=latest)\n[![Build Status](https://travis-ci.org/iScrE4m/pyArtifact.svg?branch=master)](https://travis-ci.org/iScrE4m/pyArtifact)\n\n\n## Here\'s what we can do so far\n```python\n>>> from pyartifact import Cards\n>>> cards = Cards()\n>>> cards.load_all_sets()\n>>> repr(cards.get(\'Storm Spirit\').includes[0])\n<Artifact card: {\'id\': 10538, \'base_id\': 10538, \'name\': \'Ball Lightning\', \'type\': \'Spell\', \'text\': "Move an <span style=\'font-weight:bold;color:#736e80;\'>allied black hero</span> to an empty combat position in any lane.", \'mini_image\': \'https://steamcdn-a.akamaihd.net/apps/583950/icons/set01/10538.aeb7a6a47e1d8b1a26307ae25e329df3e3bb0843.png\', \'large_image\': \'https://steamcdn-a.akamaihd.net/apps/583950/icons/set01/10538_large_english.9b39d2d2bb4769b68fa3ac42abee35b1685a57de.png\', \'ingame_image\': None, \'_CardBase__references\': [], \'color\': \'black\', \'rarity\': None, \'item_def\': None, \'mana_cost\': 3, \'illustrator\': \'JiHun Lee\'}>\n\n>>> filtered = cards.filter.type(\'Spell\').mana_cost(gt=4).color(\'black\').rarity(\'Rare\')\n>>> len(filtered)\n1\n>>> for card in filtered:\n...     print(card)\n...\nThe Cover of Night\n\n# Deck encoding (wrapper not done)\n>>> from pyartifact import decode_deck_string\n>>> deck_contents = decode_deck_string(\'ADCJQUQI30zuwEYg2ABeF1Bu94BmWIBTEkLtAKlAZakAYmHh0JsdWUvUmVkIEV4YW1wbGU_\')\n>>> print(deck_contents[\'name\'])\nBlue/Red Example\n>>> print(deck_contents[\'heroes\'])\n[{\'id\': 4003, \'turn\': 1}, {\'id\': 10006, \'turn\': 1}, {\'id\': 10030, \'turn\': 1}, {\'id\': 10033, \'turn\': 3}, {\'id\': 10065, \'turn\': 2}]\n>>> from pyartifact import encode_deck\n>>> print(encode_deck(deck_contents))\nADCJQUQI30zuwEYg2ABeF1Bu94BmWIBTEkLtAKlAZakAYmHh0JsdWUvUmVkIEV4YW1wbGU_\n```\n\n## Plans\n\n* Provide text sanitizers (text atm. has html) - to markdown, strip, etc., use for deck encoding/decoding\n* Add more filtering options\n* Cleanup code structure (possible performance improvements)\n',
    'author': 'David Jetelina',
    'author_email': 'david@djetelina.cz',
    'url': 'https://github.com/iscre4m/pyartifact',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
