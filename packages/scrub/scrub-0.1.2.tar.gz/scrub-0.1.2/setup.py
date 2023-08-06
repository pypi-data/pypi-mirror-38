# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['scrub']

package_data = \
{'': ['*']}

install_requires = \
['cytoolz>=0.9.0,<0.10.0', 'toolz>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'scrub',
    'version': '0.1.2',
    'description': 'Scrub sensitive fields for production and data that keeps changing for testing.',
    'long_description': '![](media/cover.png)\n\n# Scrub\n\nA Python library for cleaning sensitive data for production and normalizing data for testing.\n\n\n```py\n>>> from scrub import scrub_headers\n>>> sensitive_headers = {\n        "x-api-key": "--key--",\n        "x-date": "--filtered--",\n        "Set-Cookie": "--filtered--",\n    }\n>>> scrubber = scrub_headers(sensitive_headers)\n>>> scrubber({\n        "x-api-key": "3faf",\n        "x-date": "Oct 18 2001",\n        "Set-Cookie": "secret=3faf00",\n        "Accept": "application/json",\n    })\n{\n    \'Accept\': \'application/json\',\n    \'Set-Cookie\': \'--filtered--\',\n    \'x-api-key\': \'--key--\',\n    \'x-date\': \'--filtered--\'\n}\n>>>\n```\n\n## Quick Start\n\nInstall using pip/pipenv/etc. (we recommend [poetry](https://github.com/sdispater/poetry) for sane dependency management):\n\n```\n$ poetry add --dev scrub\n```\n\nImport a scrubber that you need:\n\n```py\nfrom scrub import scrub_headers scrub_body, scrub_request\n```\n\n### Available Scrubbers\n\n`scrub_headers`\n\nScrubs HTTP headers, or more generally a plain python dict. Initialize with a key replacements dict:\n\n```py\n{\n    "x-api-key": "--key--",\n    "x-date": "--filtered--",\n    "Set-Cookie": "--filtered--",\n}\n```\n\n\n`scrub_body`\n\nScrubs HTTP body, or more generally any piece of text. Initialize with content matching replacement dict:\n\n```py\n{\n    "<Secret>.*</Secret>": "<Secret>{}</Secret>".format(\n        base64.b64encode(b"--filtered--").decode()\n    ),\n    "{.*}": "{}",\n}\n```\n\n`scrub_request`\n\nScrubs a [requests](https://github.com/requests/requests) request. Give it headers and body scrubbers, or identity function if you don\'t want to replace anything there.\n\n```py\nfrom scrub import scrub_request\nscrubber = scrub_request(headerscrubber, lambda x: x)\n\nscrubber(req)\n```\n\n\n\n### Thanks:\n\nTo all [Contributors](https://github.com/jondot/scrub/graphs/contributors) - you make this happen, thanks!\n\n# Copyright\n\nCopyright (c) 2018 [@jondot](http://twitter.com/jondot). See [LICENSE](LICENSE.txt) for further details.',
    'author': 'Dotan Nahum',
    'author_email': 'jondotan@gmail.com',
    'url': 'https://github.com/jondot/scrub',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
