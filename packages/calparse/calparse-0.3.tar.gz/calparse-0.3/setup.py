import setuptools

with open('README.md', 'r') as readme:
    long_description = readme.read()

setuptools.setup(
    name='calparse',
    version='0.3',
    author='Filip Weidemann',
    author_email='filip.weidemann@outlook.de',
    description='A lightweigh CalDAV parser',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/filipweidemann/calpy',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent'
    ]
)
