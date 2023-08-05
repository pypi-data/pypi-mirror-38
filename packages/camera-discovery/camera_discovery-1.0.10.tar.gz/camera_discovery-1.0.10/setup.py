import setuptools

REQUIREMENTS = [line for line in open('requirements.txt').read().split('\n') if line != '']

VERSION = '1.0.10'
AUTHOR = 'Ricardo Barbosa Filho'
EMAIL = 'ricardob@dcc.ufmg.br'

setuptools.setup(
    name="camera_discovery",
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description="A package to discover all onvif cameras on your network",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ricardobf/camera_discovery",
    packages=setuptools.find_packages(),
    classifiers=[
        'Natural Language :: English',
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.6',
    install_requires=REQUIREMENTS,
)