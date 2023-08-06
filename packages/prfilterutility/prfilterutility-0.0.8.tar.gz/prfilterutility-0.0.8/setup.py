from setuptools import find_packages
from setuptools import setup

setup(
    name="prfilterutility",
    version="0.0.8",
    author="Mariam Jamal",
    author_email="mjamal@folio3.com",
    include_package_data=True,
    description="Package to provide utility tools for Github Pull Requests",
    long_description="Package to provide find pull requests for Github repos"
                     "with commit and file filters",
    long_description_content_type="text/markdown",
    url="https://github.com/oakbani/f3Github/gwrapper",
    packages=find_packages(
      exclude=['tests']
    ),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    test_suite='tests',
)
