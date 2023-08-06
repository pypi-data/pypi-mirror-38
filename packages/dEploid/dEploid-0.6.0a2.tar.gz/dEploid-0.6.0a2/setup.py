## import subprocess
# import platform
#from __future__ import division
#from __future__ import print_function

import zlib
import datetime
#import subprocess
import platform
import os
import os.path
#from warnings import warn

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as _build_ext

#from distutils.core import setup
#from distutils.extension import Extension


class get_pybind_include(object):
    """Helper class to determine the pybind11 include path
    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)


now = datetime.datetime.now()
ZLIB_PREFIX = os.getenv("ZLIB_PREFIX", None)
IS_WINDOWS = platform.system() == "Windows"

class PathConfigurator(object):
    """
    A class to attempt configuration of the compile search paths
    on various platforms.
    """
    def __init__(self):
        self.include_dirs = []
        self.library_dirs = []
        #try:
            #self._configure_gsl()
        #except OSError as e:
            #warn("Error occured getting GSL path config: {}".format(e))
        ## If the conda prefix is defined, then we are compiling in a conda
        ## context. All include and lib paths should come from within this prefix.
        if ZLIB_PREFIX is not None:
            prefix = ZLIB_PREFIX
            if IS_WINDOWS:
                prefix = prefix
                #prefix = os.path.join(prefix, "Library")
            self.library_dirs.append(os.path.join(prefix, "lib"))
            self.include_dirs.append(os.path.join(prefix, "include"))


libdir = "lib/src/"
includes = [libdir]

#if IS_WINDOWS:
    #includes = [libdir, "C:/projects/deploid-py/lib/src/", "C:/projects/deploid-py/lib/src/lasso/", "C:/projects/deploid-py/lib/src/random/",
                #"C:/projects/deploid-py/lib/src/gzstream/", "C:/projects/deploid-py/lib/src/codeCogs/", "C:/projects/deploid-py/lib/src/debug/",
                #"C:/projects/deploid-py/lib/src/export/"]


lasso_dir = "lasso/src/"
random_dir = "random/"
gzstream_dir = "gzstream/"
codeCogs_dir = "codeCogs/"
dbg_dir = "debug/"
export_dir = "export/"

configurator = PathConfigurator()
print(configurator.include_dirs)
source_files = [
    "dEploidIO.cpp", "panel.cpp", "variantIndex.cpp", "txtReader.cpp",
    "vcfReader.cpp", "ibd.cpp", "updateHap.cpp", "mcmc.cpp", "utility.cpp",
    os.path.join(lasso_dir, "dEploidLasso.cpp"),
    os.path.join(lasso_dir, "lasso.cpp"),
    os.path.join(lasso_dir, "lassoDBG.cpp"),
    os.path.join(random_dir, "fastfunc.cpp"),
    os.path.join(random_dir, "mersenne_twister.cpp"),
    os.path.join(random_dir, "random_generator.cpp"),
    os.path.join(gzstream_dir, "gzstream.cpp"),
    os.path.join(dbg_dir, "mcmcDebug.cpp"),
    os.path.join(dbg_dir, "vcfReaderDebug.cpp"),
    os.path.join(export_dir, "dEploidIOExport.cpp"),
    os.path.join(export_dir, "dEploidIOExportPosteriorProb.cpp"),
    os.path.join(export_dir, "writeMcmcRelated.cpp")
]

compileData = str("\"") + now.strftime("%Y-%m-%d") + str("\"")


def get_v(obj_dir):
    cwd = os.getcwd()
    os.chdir(obj_dir)
    ret = str("\"") + os.popen(
        "git show HEAD | head -1 | sed -e \"s/commit //g\" | cat").read(
        ).strip("\n") + str("\"")
    os.chdir(cwd)
    return ret


#dEploid_v = get_v("lib/")
#lasso_v = get_v("lib/DEploid-Lasso-lib")
vv = "\"python\""
dEploid_v = "\"dEploid-cpp\""
lasso_v = "\"lasso-cpp\""

if IS_WINDOWS:
    vv = "\\\"python\\\""
    dEploid_v = "\\\"dEploid-cpp\\\""
    lasso_v = "\\\"lasso-cpp\\\""

cpp11option = ['-std=c++11']
#if IS_WINDOWS:
    #cpp11option = ['-std:c++11']

_dEploid_module = Extension(
    '_dEploid',
    sources=["dEploid-py.cpp"] + [
        os.path.join(libdir, f) for f in source_files],
    extra_compile_args=cpp11option,
    extra_link_args=['-lz'],
    #libraries=['z'],
    #undef_macros=["NDEBUG"],
    define_macros=[("VERSION", vv), ("DEPLOIDVERSION", dEploid_v),
                   ("LASSOVERSION", lasso_v), ("COMPILEDATE", compileData)],
    include_dirs=[get_pybind_include(),
            get_pybind_include(user=True)] + ["lib/"] + includes + [
        os.path.join(libdir, lasso_dir)] + [
        os.path.join(libdir, random_dir)] + [
        os.path.join(libdir, gzstream_dir)] + [
        os.path.join(libdir, codeCogs_dir)] + [
        os.path.join(libdir, dbg_dir)] + [
        os.path.join(libdir, export_dir)] + configurator.include_dirs,
    library_dirs=configurator.library_dirs,
)

with open("README.rst") as f:
    long_description = f.read()

setup(
    name="dEploid",
    packages=['dEploid'],
    description="dEploid CPP module",
    long_description=long_description,
    author="Joe Zhu",
    version="0.6.0a2",
    author_email="joe.zhu@bdi.ox.ac.uk",
    url="https://github.com/DEploid-dev/DEploid-py",
    ext_modules=[_dEploid_module],
    keywords=["deconvolution", "mixed infection"],
    license="GNU GPLv3+",
    platforms=["POSIX"],
    classifiers=[
        "Programming Language :: C++",
        "Programming Language :: C",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
)
