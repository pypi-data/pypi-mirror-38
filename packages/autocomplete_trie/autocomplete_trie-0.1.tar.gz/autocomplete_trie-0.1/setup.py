# a setup file
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name="autocomplete_trie",
                 version="0.1",
                 description="A database that supports fast autocomplete. Implemented using a trie.",
                 url="https://github.com/36-750/assignments-Timothy-Barry/tree/master/autocomplete-me",
                 author="Tim Barry",
                 author_email="timothybarry@cmu.edu",
                 packages=setuptools.find_packages(),
                 classifiers=["Programming Language :: Python :: 3",
                              "License :: OSI Approved :: MIT License",
                              "Operating System :: OS Independent",
                              ],
                 )
