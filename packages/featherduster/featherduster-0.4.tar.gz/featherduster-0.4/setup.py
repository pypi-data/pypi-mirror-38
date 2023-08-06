import setuptools

with open("README.md", "r") as fh:
      long_description = fh.read()

setuptools.setup(name='featherduster',
      version='0.4',
      description='An automated, modular cryptanalysis framework (i.e. a Weapon of Math Destruction)',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/unicornsasfuel/featherduster',
      author='Daniel "unicornfurnace" Crowley',
      license='BSD 3-clause',
      packages=setuptools.find_packages(exclude=['examples','tests']),
      install_requires=[
          'pycryptodome',
          'ishell'
      ],
      entry_points = {
         'console_scripts': ['featherduster=featherduster.featherduster:main'],
      },
      classifiers=[
            "Development Status :: 4 - Beta",
            "Programming Language :: Python :: 2 :: Only",
            "Operating System :: OS Independent",
            "Environment :: Console :: Curses",
            "License :: OSI Approved :: BSD License",
            "Topic :: Security :: Cryptography"
      ],
      zip_safe=False)
