import setuptools
import os

pkg_vars = {}
pkg_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(pkg_dir, "README.md"), "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="beatbot",
    version='0.1.0',
    author="FrozenFOXX",
    author_email="frozenfoxx@cultoffoxx.net",
    description="Creates a beatmatched bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/frozenfoxx/beatbot",
    download_url = 'https://github.com/frozenfoxx/beatbot/archive/refs/tags/0.1.0.tar.gz',
    packages=["beatbot"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'vizdoom'
    ],
    entry_points = {
        "console_scripts": ["beatbot=beatbot.beatbot:main"],
    },
    data_files=[
        ('/etc/beatbot', ['conf/beatbot.yml'])
    ],
)

