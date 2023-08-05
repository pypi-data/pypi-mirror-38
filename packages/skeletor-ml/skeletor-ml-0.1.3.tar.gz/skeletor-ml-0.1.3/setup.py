"""setup.py for skeletor """
import setuptools

install_requires = [
    'pyyaml>=3.12',
    'ray>=0.4.0',
    'track-ml>=0.1',
    'torchvision',
    'awscli',
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name="skeletor-ml",
                 version="0.1.3",
                 author="Noah Golmant",
                 author_email="noah.golmant@gmail.com",
                 description="A lightweight module for research experiment reproducibility and analysis",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/noahgolmant/skeletor",
                 license='MIT License',
                 packages=setuptools.find_packages(),
                 install_requires=install_requires)
