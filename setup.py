# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt

from setuptools import setup, find_packages

name = "gocept.cxoracle"

classifiers = []

setup(
    name = name,
    version = "dev",
    author = "Christian Zagrodnick",
    author_email = "cz@gocept.com",
    description = \
    "zc.buildout recipe for installing cx_Oracle",
    long_description = (
        open("README.txt").read() + '\n\n' +
        open(os.path.join('src', 'gocept', 'cxoracle', 'README.txt')).read()),
    license = "ZPL 2.1",
    classifiers = classifiers,
    url = "http://svn.gocept.com/repos/gocept/" + name,
    download_url = \
    "https://svn.gocept.com/repos/gocept/"
    "%(name)s/trunk#egg=%(name)s-dev" % {"name": name},
    packages = find_packages("src"),
    include_package_data = True,
    package_dir = {"": "src"},
    namespace_packages = ["gocept"],
    install_requires = ["zc.buildout", "setuptools"],
    extras_require = {"test": ["zope.testing"]},
    entry_points = {"zc.buildout": ["default = %s.recipe:CxOracle" % name,],},
    )

