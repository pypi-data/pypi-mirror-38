import setuptools

setuptools.setup(
        name='sifca-utils',
        version='0.1',
        description='SIFCA analysis utils',
        author='Jordi Duarte-Campderros',
        author_email='Jordi.Duarte.Campderros@cern.ch',
        url='https://gitlab.cern.ch/sifca/sifca-utils',
        # See https://docs.python.org/2/distutils/setupscript.html#listing-whole-packages
        # for changes in the package distribution
        package_dir={'sifca_utils':'python'},
        packages = ['sifca_utils'],
        scripts=[],
        classifiers=[
            "Programming Language :: Python :: 2.7",
            "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
            "Operating System :: OS Independent",
            "Development Status :: 4 - Beta",
            ],
        )
