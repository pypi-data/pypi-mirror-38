from setuptools import setup, find_packages

__version__ = '0.8'

setup(
    name='z3c.jbot',
    version=__version__,
    description="Drop-in template overrides.",
    long_description=(open('README.rst').read() + "\n" +
                      open('CHANGES.rst').read()),
    classifiers=[
        'Framework :: Zope',
        'Framework :: Zope2',
        'Framework :: Zope :: 2',
        'Framework :: Zope3',
        'Framework :: Zope :: 3',
        'Framework :: Zope :: 4',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='page template override',
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.org',
    url='https://pypi.org/project/z3c.jbot',
    license='ZPL 2.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['z3c'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'six',
        'zope.pagetemplate',
        'zope.component',
        'zope.configuration',
        'zope.security',
        'zope.publisher',
    ],
    extras_require={
        'test': ['Zope2'],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
