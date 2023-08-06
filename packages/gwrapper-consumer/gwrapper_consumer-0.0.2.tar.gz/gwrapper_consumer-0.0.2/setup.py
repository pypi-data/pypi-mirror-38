from setuptools import find_packages
from setuptools import setup

setup(
    name="gwrapper_consumer",
    version="0.0.2",
    author="Mariam Jamal",
    author_email="mjamal@folio3.com",
    include_package_data=True,
    description="GWrapper package consumer",
    url="https://github.com/Mariamjamal32/gwrapper_consumer",
    packages=find_packages(),
    classifiers=[
        "Operating System :: OS Independent",
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    install_requires=['Flask']
)
