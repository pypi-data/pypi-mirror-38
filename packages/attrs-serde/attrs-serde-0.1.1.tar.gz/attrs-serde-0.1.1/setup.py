# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['attrs_serde']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=18.2,<19.0', 'cytoolz>=0.9.0,<0.10.0', 'toolz>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'attrs-serde',
    'version': '0.1.1',
    'description': 'A serialization addon for attrs',
    'long_description': '![](media/cover.png)\n\n# attrs-serde\n\nA serialization addon for [attrs](https://attrs.org).\n\n\n```py\nperson_dict = {"contact": {"personal": {"name": "John"}, "phone": "555-112233"}}\n\nname_path = ["contact", "personal", "name"]\nphone_path = ["contact", "phone"]\n\n@serde\n@attrs\nclass Person(object):\n    name = attrib(metadata={"to": name_path, "from": name_path})\n    phone = attrib(metadata={"to": phone_path, "from": phone_path})\n\n>>> p = Person.from_dict(person_dict)\nPerson(name=John phone=555-112233)\n\n>>> p.to_dict\n{"contact": {"personal": {"name": "John"}, "phone": "555-112233"}}\n```\n\n\n## Quick Start\n\nInstall using pip/pipenv/etc. (we recommend [poetry](https://github.com/sdispater/poetry) for sane dependency management):\n\n```\n$ poetry add attrs_serde\n```\n\nDecorate with `serde` for automatic `to_dict` and `from_dict`. Provide paths in `metadata`:\n\n1. `from` - path to fetch field value from\n2. `to` - path to serialize value into (creates nested dictionaries as needed)\n\nExample:\n\n```py\n@serde\n@attrs\nclass Person(object):\n    name = attrib(metadata={"to": name_path, "from": name_path})\n    phone = attrib(metadata={"to": phone_path, "from": phone_path})\n```\n\n\n## Performance\n\n`attrs-serde` works with `cytoolz` (mostly C implementation) and so presents very low overhead over what `attrs` already does.\n\n\nAgainst manual object construction:\n\n```\n------------------------------------------------------------------------------------- benchmark \'deserialization\': 2 tests ------------------------------------------------------------------------------------\nName (time in ns)              Min                    Max                  Mean                StdDev                Median                 IQR            Outliers  OPS (Kops/s)            Rounds  Iterations\n---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\ntest_deser_baseline       583.2500 (1.0)       5,037.3500 (1.0)        641.4743 (1.0)        161.4237 (1.0)        603.8500 (1.0)       33.7500 (1.0)     2315;3276    1,558.9089 (1.0)       77828          20\ntest_deser_serde        1,976.0000 (3.39)     88,504.0000 (17.57)    2,226.3774 (3.47)     1,195.7336 (7.41)     2,127.0000 (3.52)     110.0000 (3.26)     484;1576      449.1601 (0.29)      86806           1\n---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n```\n\nSerialization against attr\'s `asdict`:\n\n```\n-------------------------------------------------------------------------- benchmark \'serialization\': 2 tests --------------------------------------------------------------------------\nName (time in us)        Min                 Max              Mean            StdDev            Median               IQR            Outliers  OPS (Kops/s)            Rounds  Iterations\n----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\ntest_ser_baseline     2.6600 (1.0)      130.4550 (1.33)     2.9098 (1.0)      1.3230 (1.0)      2.7940 (1.0)      0.1320 (1.0)       302;882      343.6625 (1.0)       46642           1\ntest_ser_serde        5.0390 (1.89)      98.4540 (1.0)      5.6411 (1.94)     2.2398 (1.69)     5.4465 (1.95)     0.2890 (2.19)      491;912      177.2706 (0.52)      32936           1\n----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n```\n\n### Thanks:\n\nTo all [Contributors](https://github.com/jondot/attrs-serde/graphs/contributors) - you make this happen, thanks!\n\n# Copyright\n\nCopyright (c) 2018 [@jondot](http://twitter.com/jondot). See [LICENSE](LICENSE.txt) for further details.',
    'author': 'Dotan Nahum',
    'author_email': 'jondotan@gmail.com',
    'url': 'https://github.com/jondot/attrs-serde',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
