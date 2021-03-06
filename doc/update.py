#!/usr/bin/env python
# -*- coding: utf-8 -*-

#**********************************************************************************************************************#
#                                        PYTOOLBOX - TOOLBOX FOR PYTHON SCRIPTS
#
#  Main Developer : David Fischer (david.fischer.ch@gmail.com)
#  Copyright      : Copyright (c) 2012-2013 David Fischer. All rights reserved.
#
#**********************************************************************************************************************#
#
# This file is part of David Fischer's pytoolbox Project.
#
# This project is free software: you can redistribute it and/or modify it under the terms of the EUPL v. 1.1 as provided
# by the European Commission. This project is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See the European Union Public License for more details.
#
# You should have received a copy of the EUPL General Public License along with this project.
# If not, see he EUPL licence v1.1 is available in 22 languages:
#     22-07-2013, <https://joinup.ec.europa.eu/software/page/eupl/licence-eupl>
#
# Retrieved from https://github.com/davidfischer-ch/pytoolbox.git

from __future__ import absolute_import, division, print_function, unicode_literals

import shutil, sys
from pytoolbox.encoding import configure_unicode
from pytoolbox.subprocess import cmd
from pytoolbox.filesystem import from_template

configure_unicode()

# Detect modules, thanks to find !
modules = sorted(m.replace(u'.py', u'').replace(u'./', u'').replace(u'/', u'.')
                 for m in cmd(u'find . -type f -name "*.py"', cwd=u'../pytoolbox', shell=True)[u'stdout'].split()
                 if m.endswith(u'.py') and not u'__init__' in m)

print(u'Detected modules are: {0}'.format(modules))

api_toc = u''
for module in modules:
    if u'django' in module or u'crypto' in module:
        continue  # FIXME temporary hack, see issue #6
    module = u'pytoolbox.{0}'.format(module)
    title = module.replace(u'.', u' > ')
    api_toc += u'    {0}\n'.format(module)
    from_template(u'templates/module.rst.template', u'source/{0}.rst'.format(module),
                  {u'module': module, u'title': title, u'equals': u'='*len(title)})

from_template(u'templates/api.rst.template', u'source/api.rst', {u'api_toc': api_toc})
shutil.rmtree(u'build/html', ignore_errors=True)
result = cmd(u'make html', fail=False)

print(u'\nOutputs\n=======\n')
print(result[u'stdout'])
print(u'\nErrors\n======\n')
print(result[u'stderr'])

sys.exit(0 if not result[u'stderr'] else 1)
