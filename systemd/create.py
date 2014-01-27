"""
Create systemd files from .in templates.
"""

import os
import glob
import coils

# Do the work in systemd/ subdirectory.
os.chdir('systemd')

# For each *.service.in template, create a real .service 
# file with text replacement as per the configuration.
config = coils.Config('hello.conf')
for fname in glob.glob('*.service.in'):
    with open(fname) as inf:
        outf = config['PREFIX'] + fname[:-3]
        outf = open(outf, 'w')
        for line in inf.readlines():
            for key, val in config.items():
                line = line.replace('@{}@'.format(key), val)
            outf.write(line)
        outf.close()
