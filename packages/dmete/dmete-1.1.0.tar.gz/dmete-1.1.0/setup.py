''' python库安装脚本 '''

import setuptools
with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="dmete",
    version="1.1.0",
    author="Linhong Xiao",
    author_email="xiaoforest@lzb.ac.cn",
    description="download mete data",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="http://10.110.18.201:3000/Course/dump_mete",

    package_data={'dmete': ['*.txt',],},

    entry_points={
        "console_scripts": ["dmete=dmete.dump:main",],
    },

    packages=setuptools.find_packages(),

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
