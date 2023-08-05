# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['thea',
 'thea.comm_handlers',
 'thea.environment',
 'thea.environment.updaters',
 'thea.thing_updaters']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0,<1', 'paho-mqtt>=1,<2', 'pvlib>=0,<1']

extras_require = \
{'docs': ['mkdocs>=1,<2', 'mkdocs-material>=3,<4', 'pygments>=2,<3']}

entry_points = \
{'console_scripts': ['my-script = thea:__main__']}

setup_kwargs = {
    'name': 'thea',
    'version': '0.0.1',
    'description': 'Thea is used to control the lighting of model(-train) layouts based on simulations and real world data.',
    'long_description': '# Thea\n\n***"Titaness of (...) the shining light of the clear blue sky"**\nfrom [Wikipedia](https://en.wikipedia.org/wiki/Thea) retrieved 1 November 2018.*\n\n---\n\n[![Python version](https://img.shields.io/badge/python-3.6%20%7C%203.7-blue.svg)](https://www.python.org/downloads/)\n[![Linux status](https://img.shields.io/travis/com/mikevansighem/thea/master.svg?label=linux)](https://travis-ci.com/mikevansighem/thea)\n[![Windows status](https://img.shields.io/appveyor/ci/mikevansighem/thea/master.svg?label=windows)](https://ci.appveyor.com/project/mikevansighem/thea/branch/master)\n[![Docs](https://img.shields.io/website-up-down-green-red/http/shields.io.svg?label=docs)](https://mikevansighem.github.io/thea/)\n[![Codacy Badge](https://img.shields.io/codacy/grade/bb3d838b073c489b89232463f0c2cf66.svg)](https://www.codacy.com/app/mikevansighem/thea?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=mikevansighem/thea&amp;utm_campaign=Badge_Grade)\n[![Codacy Badge](https://img.shields.io/codacy/coverage/bb3d838b073c489b89232463f0c2cf66.svg)](https://www.codacy.com/app/mikevansighem/thea?utm_source=github.com&utm_medium=referral&utm_content=mikevansighem/thea&utm_campaign=Badge_Coverage)\n[![Updates](https://pyup.io/repos/github/mikevansighem/thea/shield.svg)](https://pyup.io/repos/github/mikevansighem/thea/)\n[![License: LGPL 3](https://img.shields.io/badge/license-LGPL%203-blue.svg)](LICENSE.md)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n---\n\nThea is used to control the environment of model (train) layouts based\non real-world data and simulation models. Current development is focused\naround lighting ðŸŒ„ but we plan to expand the functionalities to include\nsound ðŸ”‰ and actuator control.\n\n---\n\n![](docs/images/header.png)\n\n---\n\n## ðŸŒ± Origin\n\nThis project was started in order to control lighting of model-train\nlayouts in more interesting ways. Most solutions only offer manual\nand rule based control resulting in very predictive behavior. Thea\nbreaks with this by controlling the model environment based on real-word\ndata and simulation models that introduce an element of randomness.\n\n## âœ… Principles\n\n-   Science based environment simulation;\n-   Simple to start but complex if you want to;\n-   Modern user interface;\n-   Support for common hardware;\n\n## âœ¨ Features\n\nCurrently Thea is in early development so the list of available features\nis a bit short. However we have a lot planned:\n\n-   [x] Accelerated model time\n-   [ ] Day and night cycle ðŸŒ“\n-   [ ] Hardware control over MQTT\n-   [ ] Household lighting\n-   [ ] Weather patterns ðŸŒ€\n-   [ ] Traffic ðŸš—\n-   [ ] Opening-hours ðŸ•“\n-   [ ] Graphical user interface\n-   [ ] Moon and stars ðŸŒ›âœ¨\n-   [ ] DCC train control ðŸš‚\n-   [ ] Weather sounds ðŸ”‰\n\n## ðŸ¤” Getting started\n\nCurrently there is not much use in this project as an end user. However\nif you would like to contribute head over to the\n[contributing](https://mikevansighem.github.io/thea/contibuting) section\nof our documentation. We are happy to receive pull-requests.\n\n## ðŸ“š Documentation\n\nAll our documentation including on how to get started can be found\n[here](https://mikevansighem.github.io/thea).\n\n## ðŸ“ƒ License\n\nThea is created by Mike van Sighem and licensed under LGPL version 3.\nRefer to the\n[license](https://github.com/mikevansighem/thea/blob/master/docs/LICENSE.md)\nfor more details.\n\n## ðŸ’› Contributing \n\nWe are happy to see contributors on the project. Head over to the\n[contributing](https://mikevansighem.github.io/thea/contibuting) section\nof our documentation and submit your first pull-requests.\n',
    'author': 'Mike van Sighem',
    'author_email': 'mikevansighem@gmail.com',
    'url': 'https://mikevansighem.github.io/thea/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
