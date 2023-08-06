import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
      name='qlib',
      version='0.0.2dev19',
      author="Q Engineering Dev Team",
      author_email="david@q.engineering",
      description="A Q Library for Data Scientist",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/Q-Engineering/qlib",
      packages=setuptools.find_packages(),
      install_requires=[
          'requests',
      ],
      classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
      ],
      project_urls={  # Optional
         'Bug Reports': 'https://someurl',
         'Funding': 'https://someurl',
         'Subscriptions': 'http://someurl',
         'Source': 'https://someurl',
    },
)