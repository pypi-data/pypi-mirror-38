import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
   name="dmete",
   version="1.0.1",
   author="Linhong Xiao",
   author_email="xiaoforest@lzb.ac.cn",
   description="download mete data",
   long_description=long_description,
   long_description_content_type="text/markdown",
   url="http://10.110.18.201:3000/Course/dump_mete",

   package_data = {
        'dmete': ['*.txt',],
   },

   packages=setuptools.find_packages(),

   classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
   ],
)
