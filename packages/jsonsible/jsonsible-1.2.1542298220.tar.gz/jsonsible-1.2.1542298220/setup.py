from setuptools import setup, find_packages

setup(
    description="Python Library to turn ansible playbook into a json",
    author="Thomas Yeomans",
    author_email="william.yeomans@ge.com",
    url="https://github.build.ge.com/Cloudpod/jsonsible",
    version="1.2.1542298220",
    long_description="Python Library for returning a json of information from an ansible playbook run.",
    name="jsonsible",
    packages=find_packages(exclude=["build", "build/*"])
)
