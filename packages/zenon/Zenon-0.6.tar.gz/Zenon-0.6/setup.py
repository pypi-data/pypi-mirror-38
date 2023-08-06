from distutils.core import setup
from setuptools import find_packages

setup(
    name="Zenon",
    version="0.6",
    packages=find_packages(),
    author="Zenaker",
    description="a discord userbot or selfbot framework to interact with users instead of normal bots",
    url="https://github.com/Zenaker/Zenon",
    keywords = ['discord', 'selfbot', 'userbot', 'bot'],
    install_requires=['requests'],
    download_url='https://github.com/Zenaker/Zenon/archive/v_06.tar.gz'
)