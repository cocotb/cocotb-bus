# Copyright cocotb contributors
# Licensed under the Revised BSD License, see LICENSE for details.
# SPDX-License-Identifier: BSD-3-Clause

from setuptools import setup, find_packages


with open("README.md") as file:
    long_description = file.read()


if __name__ == "__main__":
    setup(
        name="cocotb-bus",
        use_scm_version=dict(
            write_to='src/cocotb_bus/_version.py',
            version_scheme='release-branch-semver'
        ),
        author="cocotb maintainers",
        author_email="cocotb@lists.librecores.org",
        description="",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/cocotb/cocotb-bus",
        packages=find_packages("src"),
        package_dir={"": "src"},
        install_requires=[
            "cocotb>=1.5.0.dev,<2.0"
        ],
        python_requires='>=3.5'
    )
