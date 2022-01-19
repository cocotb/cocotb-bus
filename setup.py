# Copyright cocotb contributors
# Licensed under the Revised BSD License, see LICENSE for details.
# SPDX-License-Identifier: BSD-3-Clause
import pathlib

from setuptools import setup, find_packages


def get_version(version_file):
    locls = {}
    exec(open(version_file).read(), {}, locls)
    return locls["__version__"]


root = pathlib.Path(__file__).parent.resolve()
readme_file = root / "README.md"
version_file = root / "src" / "cocotb_bus" / "_version.py"


if __name__ == "__main__":
    setup(
        name="cocotb-bus",
        version=get_version(version_file),
        author="cocotb maintainers",
        author_email="cocotb@lists.librecores.org",
        description="",
        long_description=readme_file.read_text(encoding="utf-8"),
        long_description_content_type="text/markdown",
        url="https://github.com/cocotb/cocotb-bus",
        packages=find_packages("src"),
        package_dir={"": "src"},
        install_requires=[
            "cocotb>=1.5.0.dev,<2.0"
        ],
        python_requires='>=3.5'
    )
