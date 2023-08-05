# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['sqlalchemy_lazy_way']

package_data = \
{'': ['*']}

install_requires = \
['sqlalchemy>=1.2,<2.0']

setup_kwargs = {
    'name': 'sqlalchemy-lazy-way',
    'version': '0.0.1',
    'description': 'sqlalchemy-lazy-way ',
    'long_description': '# sqlalchemy-lazy-way\n\n![pyversions](https://img.shields.io/badge/python%20-3.7%2B-blue.svg)\n![celery](https://img.shields.io/badge/celery-4.2.0-4BC51D.svg)\n![pypi](https://img.shields.io/pypi/v/nine.svg)\n[![contributions welcome](https://img.shields.io/badge/contributions-welcome-ff69b4.svg)](https://github.com/twocucao/YaDjangoWeb/issues)\n\n## 目的\n\n使用 sqlalchemy 之后，很多查询写起来特别啰嗦。为了在提高效率的基础上能挽留点头发 , 于是开了这个项目。\n\n1. Django Like Query\n2. Common Utils\n\n## Get Started\n\n```bash\nbrew install python3\n```\n\n## 技术栈\n\n - Python 3.7.0\n\n## 许可\n\nmit\n\n## Credits\n\n- smart_query ported from https://github.com/mitsuhiko/sqlalchemy-django-query/blob/master/tests.py\n\n',
    'author': 'twocucao',
    'author_email': 'twocucao@gmail.com',
    'url': 'https://github.com/twocucao/sqlalchemy-lazy-way',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
