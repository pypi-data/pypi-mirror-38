from setuptools import setup, find_packages
from os import path


def long_description():
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        README = f.read()

    with open(path.join(here, 'HISTORY.md'), encoding='utf-8') as f:
        HISTORY = f.read()

    return '\n# ——————\n'.join([README, HISTORY])

setup(
    name='writeas-anon',
    version='0.1.0',
    description='Post anonymously to write.as',
    long_description_content_type="text/markdown",
    long_description=long_description(),
    license='MIT',
    packages=find_packages(),
    author='Grzegorz Chilczuk',
    author_email='chgrzegorz@pm.me',
    classifiers=[  # Optional
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='writeas anonymous',
    url='https://gitlab.com/chgrzegorz/writeas-anon',
    install_requires = [
        'requests>=2.20.1,<3.0.0',
    ]
)
