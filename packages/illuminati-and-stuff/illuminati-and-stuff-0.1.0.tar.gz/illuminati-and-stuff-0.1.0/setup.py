"""setup.py"""
import setuptools

with open('README.md', 'r') as readme:
    README_TEXT = readme.read()

setuptools.setup(
    name='illuminati-and-stuff',
    version='0.1.0',
    license='MIT',
    author='yiwen song',
    author_email='songzgy@gmail.com',
    url='https://github.com/yiwensong/illuminati_and_stuff',
    description=(
        'a pyramid tween that returns the traceback to the client '
        'for 500 responses'
    ),
    long_description=README_TEXT,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(exclude=['tests*']),
    install_requires=[
        'pyramid',
    ],
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords=[
        'pyramid',
    ],
    entry_points={
    },
)
