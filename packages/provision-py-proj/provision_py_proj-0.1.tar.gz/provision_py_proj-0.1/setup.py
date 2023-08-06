#!/usr/bin/python3
"""Setup module for provision_py_proj pkg."""
from setuptools import setup, find_packages
import os
import sys
import shutil
import stat
from setuptools.command.develop import develop
from setuptools.command.install import install
from abstract_requires import requires

pkg_name = "provision_py_proj"
parent_dir = os.path.dirname(os.path.realpath(__file__))
data_src_dir = pkg_name + "_data"
config_src_dir = pkg_name + "_config"
defaults_location = os.path.join(pkg_name, "defaults")

# Create scripts list
script_dir = os.path.join(parent_dir, "bin")
scripts = []
try:
    for f in os.listdir(script_dir):
        scripts.append(os.path.join(script_dir, str(f)))

except FileNotFoundError:
    pass

def copy_pkg_files():
    """Copy config and data files."""
    from appdirs import user_data_dir, user_config_dir

    pkg_dirs_to_copy = [
        (data_src_dir, user_data_dir()),
        (config_src_dir, user_config_dir())
    ]
    for d, t in pkg_dirs_to_copy:
        t = os.path.join(t, d)
        d = os.path.join(os.path.join(parent_dir, pkg_name), d)

        if os.path.exists(d):
            shutil.rmtree(t, ignore_errors=True)
            shutil.copytree(d, t)

            if "SUDO_USER" in os.environ:
                user = os.environ["SUDO_USER"]
            else:
                user = os.environ["USER"]

            for root, dirs, files in os.walk(t):
                shutil.chown(root, user=user, group=user)
                os.chmod(root, stat.S_IRWXU)

                for d in dirs:
                    d_path = os.path.join(root, d)
                    shutil.chown(d_path, user=user, group=user)
                    os.chmod(d_path, stat.S_IRWXU)

                for f in files:
                    f_path = os.path.join(root, f)
                    shutil.chown(f_path, user=user, group=user)
                    os.chmod(f_path, stat.S_IRUSR | stat.S_IWUSR)


def reset():
    """Remove build dirs."""
    dirnames_to_remove = [pkg_name + ".egg-info", "dist", "build"]
    for d in dirnames_to_remove:
        shutil.rmtree(d, ignore_errors=True)

with open("README.md", "r") as fh:
    long_description = fh.read()

def setuptools_setup():
    """Setup provisioner."""
    setup(
        name="provision_py_proj",
        version="0.1",
        description="Utility for the creation of python packages.",
        url="https://github.com/ku-wolf/provision_py_proj",
        author="Kevin Wolf",
        author_email="kevinuwolf@gmail.com",
        license="gplv3.txt",
        packages=find_packages(),
        scripts=scripts,
        install_requires=requires,
        setup_requires=requires,
        long_description=long_description,
        long_description_content_type="text/markdown",
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
        ]
    )


def main():
    """Main method."""
    os.chdir(parent_dir)

    if sys.argv[1] == "reset":
        reset()
    else:
        setuptools_setup()
        copy_pkg_files()

if __name__ == "__main__":
    main()
