import setuptools
import subprocess

with open("README.md", "r") as fh:
    long_description = fh.read()

version = subprocess.run(['git', 'rev-list', '--all', '--count'], stdout=subprocess.PIPE)
version = version.stdout.decode('utf-8').replace('\n', '').replace('\r', '')

setuptools.setup(
    name="connectivity",
    version=version,
    author="nevolution.developers",
    author_email="basti.neubert@gmail.com",
    description="Library containing Server and Client for transferring messages and files via TCP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/nevolution.developers/libs/connectivity",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)