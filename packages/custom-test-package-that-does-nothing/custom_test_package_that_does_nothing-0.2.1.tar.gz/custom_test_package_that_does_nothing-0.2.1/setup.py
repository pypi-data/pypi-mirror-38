import setuptools

with open("README.md", "r") as fh:
      long_description = fh.read()

setuptools.setup(
      name="custom_test_package_that_does_nothing",
      version="0.2.1",
      author="Mak",
      author_email="38956972+makarandh@users.noreply.github.com",
      description="A python library that does nothing",
      long_description_content_type="text/markdown",
      url="https://github.com/makarandh/do-nothing",
      packages=setuptools.find_packages(),
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: OS Independent",
      ],
)
