# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['epicbox']

package_data = \
{'': ['*']}

install_requires = \
['docker>=2',
 'python-dateutil>=2.4,<3.0',
 'requests>=2.14.2,<3.0.0',
 'structlog>=15.3']

setup_kwargs = {
    'name': 'epicbox',
    'version': '1.0.0',
    'description': 'Run untrusted code in secure Docker based sandboxes',
    'long_description': '# epicbox\n[![Build Status](https://travis-ci.org/StepicOrg/epicbox.svg?branch=master)](https://travis-ci.org/StepicOrg/epicbox)\n\nA Python library to run untrusted code in secure, isolated [Docker](https://www.docker.com/)\nbased sandboxes. It is used to automatically grade programming assignments\non [Stepik.org](https://stepik.org/).\n\nIt allows to spawn a process inside one-time Docker container, send data\nto stdin, and obtain its exit code and stdout/stderr output.  It\'s very similar\nto what the [`subprocess`](https://docs.python.org/3/library/subprocess.html#module-subprocess)\nmodule does but additionally you can specify a custom environment for the process\n(a Docker [image](https://docs.docker.com/v17.09/engine/userguide/storagedriver/imagesandcontainers/))\nand limit the CPU, memory, disk, and network usage for the running process.\n\n## Usage\nRun a simple Python script in a one-time Docker container using the\n[`python:3.6.5-alpine`](https://hub.docker.com/_/python/) image:\n```python\nimport epicbox\n\nepicbox.configure(\n    profiles=[\n        epicbox.Profile(\'python\', \'python:3.6.5-alpine\')\n    ]\n)\nfiles = [{\'name\': \'main.py\', \'content\': b\'print(42)\'}]\nlimits = {\'cputime\': 1, \'memory\': 64}\nresult = epicbox.run(\'python\', \'python3 main.py\', files=files, limits=limits)\n\n```\nThe `result` value is:\n```python\n{\'exit_code\': 0,\n \'stdout\': b\'42\\n\',\n \'stderr\': b\'\',\n \'duration\': 0.143358,\n \'timeout\': False,\n \'oom_killed\': False}\n```\n\n### Advanced usage\nA more advanced usage example of `epicbox` is to compile a C++ program and then\nrun it multiple times on different input data.  In this example `epicbox` will\nrun containers on a dedicated [Docker Swarm](https://docs.docker.com/swarm/overview/)\ncluster instead of locally installed Docker engine:\n```python\nimport epicbox\n\nPROFILES = {\n    \'gcc_compile\': {\n        \'docker_image\': \'stepik/epicbox-gcc:6.3.0\',\n        \'user\': \'root\',\n    },\n    \'gcc_run\': {\n        \'docker_image\': \'stepik/epicbox-gcc:6.3.0\',\n        # It\'s safer to run untrusted code as a non-root user (even in a container)\n        \'user\': \'sandbox\',\n        \'read_only\': True,\n        \'network_disabled\': False,\n    },\n}\nepicbox.configure(profiles=PROFILES, docker_url=\'tcp://1.2.3.4:2375\')\n\nuntrusted_code = b"""\n// C++ program\n#include <iostream>\n\nint main() {\n    int a, b;\n    std::cin >> a >> b;\n    std::cout << a + b << std::endl;\n}\n"""\n# A working directory allows to preserve files created in a one-time container\n# and access them from another one. Internally it is a temporary Docker volume.\nwith epicbox.working_directory() as workdir:\n    epicbox.run(\'gcc_compile\', \'g++ -pipe -O2 -static -o main main.cpp\',\n                files=[{\'name\': \'main.cpp\', \'content\': untrusted_code}],\n                workdir=workdir)\n    epicbox.run(\'gcc_run\', \'./main\', stdin=\'2 2\',\n                limits={\'cputime\': 1, \'memory\': 64},\n                workdir=workdir)\n    # {\'exit_code\': 0, \'stdout\': b\'4\\n\', \'stderr\': b\'\', \'duration\': 0.095318, \'timeout\': False, \'oom_killed\': False}\n    epicbox.run(\'gcc_run\', \'./main\', stdin=\'14 5\',\n                limits={\'cputime\': 1, \'memory\': 64},\n                workdir=workdir)\n    # {\'exit_code\': 0, \'stdout\': b\'19\\n\', \'stderr\': b\'\', \'duration\': 0.10285, \'timeout\': False, \'oom_killed\': False}\n```\n\n## Installation\n`epicbox` can be installed by running `pip install epicbox`. It\'s tested on Python 3.4+ and\nDocker 1.12+.\n\nYou can also check the [epicbox-images](https://github.com/StepicOrg/epicbox-images)\nrepository that contains Docker images used to automatically grade programming\nassignments on [Stepik.org](https://stepik.org/).\n\n## Contributing\nContributions are welcome, and they are greatly appreciated!\nMore details can be found in [CONTRIBUTING](CONTRIBUTING.rst).\n',
    'author': 'Pavel Sviderski',
    'author_email': 'ps@stepik.org',
    'url': 'https://github.com/StepicOrg/epicbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
