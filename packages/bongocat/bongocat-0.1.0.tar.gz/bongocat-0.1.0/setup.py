import setuptools

with open('README.md') as file:

    readme = file.read()

name = 'bongocat'

module = __import__(name)

version = module.__version__

author = 'Exahilosys'

url = f'https://github.com/{author}/{name}'

download_url = f'{url}/archive/v{version}.tar.gz'

setuptools.setup(
    name = name,
    version = version,
    author = author,
    url = url,
    download_url = download_url,
    packages = setuptools.find_packages(),
    license = 'MIT',
    description = 'Bongo Cat overlay.',
    long_description = readme,
    long_description_content_type = 'text/markdown',
    include_package_data = True,
    install_requires = ['docopt', 'keyboard', 'pillow'],
    py_modules = [name],
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    entry_points = {
        'console_scripts': [
            f'{name} = {name}:start',
        ],
    },
)
