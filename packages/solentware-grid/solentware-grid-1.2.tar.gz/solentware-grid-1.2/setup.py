# setup.py
# Copyright 2011 Roger Marsh
# Licence: See LICENCE (BSD licence)

from setuptools import setup

if __name__ == '__main__':

    long_description = open('README').read()

    setup(
        name='solentware-grid',
        version='1.2',
        description='Database display classes',
        author='Roger Marsh',
        author_email='roger.marsh@solentware.co.uk',
        url='http://www.solentware.co.uk',
        package_dir={'solentware_grid':''},
        packages=[
            'solentware_grid',
            'solentware_grid.core', 'solentware_grid.gui',
            'solentware_grid.gui.minorbases',
            'solentware_grid.db', 'solentware_grid.dpt',
            'solentware_grid.sqlite', 'solentware_grid.apsw',
            'solentware_grid.about',
            ],
        package_data={
            'solentware_grid.about': ['LICENCE', 'CONTACT'],
            },
        long_description=long_description,
        license='BSD',
        classifiers=[
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Operating System :: OS Independent',
            'Topic :: Software Development',
            'Topic :: Database :: Front-Ends',
            'Intended Audience :: Developers',
            'Development Status :: 4 - Beta',
            ],
        )
