#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import os.path
import setuptools
import setuptools.command.build_py
import shutil
import subprocess
import tempfile


def runCustomCommand(originalCommand):
    """
        A decorator for classes subclassing a setuptools/distutils
        command.
        Compiles the webis Java classes during build
    """

    originalRun = originalCommand.run

    def modifiedRun(self):
        # This function contains additional steps carried out
        # during the `build` command of setuptools

        import git

        # 1. update ECIR-2015-and-SEMEVAL-2015 submodule
        with git.Repo(".") as repo:
            for submodule in repo.submodules:
                submodule.update(init=True)

        # 2. download jazzy dictionaries (mandatory for but omitted
        #    by ECIR-2015-and-SEMEVAL-2015
        spellCheckerDir = os.path.join(
            ".",
            "webis",
            "ECIR-2015-and-SEMEVAL-2015",
            "resources",
            "lexi",
            "SpellChecker"
        )
        if not os.path.exists(spellCheckerDir):
            with tempfile.TemporaryDirectory() as jazzyRepoDir:
                git.Repo.clone_from(
                    "https://github.com/reckart/jazzy",
                    jazzyRepoDir
                )
                shutil.copytree(
                    os.path.join(jazzyRepoDir, "dict"),
                    spellCheckerDir
                )

        # 3. compile java classes
        subprocess.run(
            [
                os.path.join(
                    os.path.abspath(
                        os.path.dirname(__file__)
                    ),
                    "webis",
                    "tools",
                    "compile-java.sh"
                )
            ],
            capture_output=True
        )

        # 4. run original `build` command
        originalRun(self)

    originalCommand.run = modifiedRun
    return originalCommand


@runCustomCommand
class CustomBuildPyCommand(setuptools.command.build_py.build_py):
    pass


with open("README.md") as f:
    longDescription = f.read()

with open("requirements.txt") as f:
    requirements = f.read()

# try to derive version from git tag,
# otherwise read from file VERSION
try:
    import git

    try:
        with git.Repo(".") as repo:
            version = repo.git.describe()
            with open("VERSION", "w") as f:
                f.write("{}\n".format(version))

    except git.exc.InvalidGitRepositoryError:
        raise RuntimeError("Not in git repository")

except (ImportError, RuntimeError, git.exc.GitCommandError):
    with open("VERSION") as f:
        version = f.read()
        # strip trailing newline
        version = version[:-1]

# strip initial "v"
version = version[1:]

# extra files to include
packageName = setuptools.find_packages()[0]
os.chdir(packageName)
packageData = \
    glob.glob(
        os.path.join("ECIR-2015-and-SEMEVAL-2015", "**", "*.*"),
        recursive=True
    )
os.chdir("..")

# discard two of the arff files to submit a dev release to pypi
# in order to receive a higher file size quota
packageData = [p for p in packageData if not("TeamX.arff" in p or "NRC.arff" in p)]
for p in packageData:
    print(p)


setuptools.setup(
    name=packageName,
    version=version,
    author="Christoph Fink",
    author_email="christoph.fink@helsinki.fi",
    description="Python wrapper for the webis " +
    "Twitter sentiment identification tool",
    long_description=longDescription,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/christoph.fink/python-webis",
    packages=[packageName],
    package_data={
        packageName: packageData
    },
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent"
    ],
    license="GPLv2",
    cmdclass={
        "build_py": CustomBuildPyCommand
    }
)
