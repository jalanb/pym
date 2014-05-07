"""Set up the pym project"""


from setuptools import setup, find_packages


import pym


setup(
    name='pym',
    packages=find_packages(),
    version=pym.__version__,
    url='https://github.com/jalanb/pym',
    download_url=
        'https://github.com/jalanb/pym/tarball/v%s' % pym.__version__,
    license='MIT License',
    author='J Alan Brogan',
    author_email='pym@al-got-rhythm.net',
    description=pym.__doc__,
    platforms='any',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Development Status :: 1 - Planning',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Text Editors :: Text Processing',
        'Topic :: Software Development :: Code Generators',
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    extras_require={
        'testing': ['nose'],
    }
)
