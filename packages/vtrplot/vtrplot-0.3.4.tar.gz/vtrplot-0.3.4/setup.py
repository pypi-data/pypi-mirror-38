from setuptools import setup
from vtrplot import __version__ as vtrplot_version

setup(
    name='vtrplot',
    version=vtrplot_version,
    author='Tim Lin (S-Cube)',
    author_email='tlin@s-cube.com',
    description='Python utilities for Fullwave3D VTR model files',
    license='3-clause BSD',
    keywords='fullwave3d vtr',
    url='http://not-yet',
    py_modules=['vtrplot.vtr_image', 'vtrplot.sliced_models', 'vtrplot.interp', 'vtrplot.color_mappings'],
    long_description=open('README.md').read(),
    install_requires=[
        'numpy>=1.9',
        'purepng>=0.2',
        'vtrtool>=0.5',
        'segyio>=1.6',
        'defusedxml>=0.5'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
    ]
)
