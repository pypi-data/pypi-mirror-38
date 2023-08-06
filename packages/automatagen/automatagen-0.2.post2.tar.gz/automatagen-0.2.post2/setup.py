import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='automatagen',
      version='0.2.post-2',
      description='Generate random terrain using cellular automata.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/PetarPeychev/automatagen',
      author='PetarPeychev',
      author_email='petarpeychev98@gmail.com',
      packages=setuptools.find_packages(),
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: Public Domain",
          "Operating System :: OS Independent",
       ],)
