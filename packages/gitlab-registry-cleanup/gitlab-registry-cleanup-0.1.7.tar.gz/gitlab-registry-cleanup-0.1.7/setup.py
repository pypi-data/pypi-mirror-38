import os
import runpy
import subprocess
from setuptools import setup, find_packages


def get_version_from_pyfile(version_file="gitlab_registry_cleanup/_version.py"):
    file_globals = runpy.run_path(version_file)
    return file_globals["__version__"]


def get_install_requires_from_requirements(requirements_filename="requirements.txt"):
    try:
        with open(requirements_filename, "r", encoding="utf-8") as requirements_file:
            requirements = requirements_file.readlines()
    except OSError:
        import logging

        logging.warning("Could not read the requirements file.")
    return requirements


def get_long_description_from_readme(readme_filename="README.md"):
    rst_filename = "{}.rst".format(os.path.splitext(os.path.basename(readme_filename))[0])
    created_tmp_rst = False
    if not os.path.isfile(rst_filename):
        try:
            subprocess.check_call(["pandoc", readme_filename, "-t", "rst", "-o", rst_filename])
            created_tmp_rst = True
        except (OSError, subprocess.CalledProcessError):
            import logging

            logging.warning("Could not convert the readme file to rst.")
    long_description = None
    if os.path.isfile(rst_filename):
        with open(rst_filename, "r", encoding="utf-8") as readme_file:
            long_description = readme_file.read()
    if created_tmp_rst:
        os.remove(rst_filename)
    return long_description


version = get_version_from_pyfile()
long_description = get_long_description_from_readme()
install_requires = get_install_requires_from_requirements()

setup(
    name="gitlab-registry-cleanup",
    version=version,
    packages=find_packages(),
    python_requires="~=3.3",
    install_requires=install_requires,
    entry_points={"console_scripts": ["gitlab-registry-cleanup = gitlab_registry_cleanup.cli:main"]},
    author="Ingo Heimbach",
    author_email="i.heimbach@fz-juelich.de",
    description="A tool to clean up untagged GitLab registry images.",
    long_description=long_description,
    license="MIT",
    url="https://github.com/sciapp/gitlab-registry-cleanup",
    keywords=["Git", "GitLab", "Docker", "Registry", "Cleanup"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: System :: Systems Administration",
    ],
)
