# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['tmn', 'tmn.elements']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'clint>=0.5.1,<0.6.0',
 'docker==3.5.0',
 'eth-hash[pycryptodome]>=0.2.0,<0.3.0',
 'eth-keys>=0.2.0b3,<0.3.0',
 'pastel>=0.1.0,<0.2.0',
 'python-slugify>=1.2,<2.0']

entry_points = \
{'console_scripts': ['tmn = tmn.tmn:main']}

setup_kwargs = {
    'name': 'tmn',
    'version': '0.3.2',
    'description': 'Quickstart your masternode',
    'long_description': '# tmn <a href="https://gitter.im/tomochain/tmn"><img align="right" src="https://badges.gitter.im/gitterHQ/gitter.png"></a>\n\n| Branch  | Status | Coverage |\n| --- | --- | --- |\n| Master | [![Build Status](https://travis-ci.org/tomochain/tmn.svg?branch=master)](https://travis-ci.org/tomochain/tmn) | [![Coverage Status](https://coveralls.io/repos/github/tomochain/tmn/badge.svg?branch=master)](https://coveralls.io/github/tomochain/tmn?branch=master) |\n| Develop | [![Build Status](https://travis-ci.org/tomochain/tmn.svg?branch=develop)](https://travis-ci.org/tomochain/tmn) | [![Coverage Status](https://coveralls.io/repos/github/tomochain/tmn/badge.svg?branch=develop)](https://coveralls.io/github/tomochain/tmn?branch=develop) |\n\nTomo MasterNode (tmn) is a cli tool to help you run a TomoChain masternode\n\n## Running and applying a masternode\n\nIf you are consulting this repo, it\'s probably because you want to run a masternode.\nFor complete guidelines on running a full node and applying it as a masternode, please refer to the [documentation](https://docs.tomochain.com/get-started/run-node/).\n\n## Requirements\n\n- Python >= 3.5\n- Docker\n\n## Installation\n\n```\npip3 install --user tmn\n```\n\nIf you are using macOS, make sure that the user python3 path is in your `$PATH`.\n\nThey are in `~/Library/Python/[python version number]/bin`.\n\nFor example, with python `3.6` and `bash`, add `PATH=$PATH:$HOME/Library/Python/3.6/bin` to your `$HOME/.bashrc`.\n\n## Update\n\nTo update `tmn, use pip3 directly.\n\n```\npip3 install -U tmn\n```\n\nIf you want to update the version of the TomoChain masternode run by tmn, directly use `tmn update`.\nWe communicate about updates on our [Gitter channel](https://gitter.im/tomochain/tmn).\n\n## Usage\n\n```\nUsage: tmn [OPTIONS] COMMAND [ARGS]...\n\n  Tomo MasterNode (tmn) is a cli tool to help you run a TomoChain masternode\n\nOptions:\n  --debug       Enable debug mode\n  --docker URL  Url to the docker server\n  --version     Show the version and exit.\n  --help        Show this message and exit.\n\nCommands:\n  docs     Display TomoChain documentation link\n  inspect  Show details about your TomoChain masternode\n  remove   Remove your TomoChain masternode\n  start    Start your TomoChain masternode\n  status   Show the status of your TomoChain masternode\n  stop     Stop your TomoChain masternode\n  update   Update your masternode\n```\n\n### First start\n\nOn the first run you will need to provide some options to the start command.\nIt will let you configure your node.\n\n```\nname = tomochain-orion  # A name that represents you.\n                        # It will be the public name available on tomomaster\n                        # and on the network stat page.\n\nnet = testnet           # The network you want to connect to.\n                        # Should be testnet or mainnet.\n\npkey = a25...5f5        # The private key of the account you want your\n                        # masternode to use.\n                        # It will be used to receive transactions fees\n                        # Please use a separate new account for security reasons\n\ntmn start --name $name --net $net --pkey $pkey\n```\n\n### After the first start\n\nOnce your node has been configured, you can use the start, stop and\nstatus command to interact with your node without any options.\n\n```\ntmn stop\n\ntmn start\n\ntmn status\n\ntmn inspect\n\ntmn update\n```\n\n### Removing\n\nIf you want to completely remove your node, you can use the `remove` command.\nBe aware that it will delete all data and lose your unique identity.\n\n```\ntmn remove\n```\n\n## Applying your node\n\nWith a running node, you can now apply it as a masternode on TomoMaster.\nYou can get the details of your node required to apply directly from `tmn`.\n\n```\ntmn inspect\n```\n',
    'author': 'Etienne Napoleone',
    'author_email': 'etienne@tomochain.com',
    'url': 'https://tomochain.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5.3,<4.0.0',
}


setup(**setup_kwargs)
