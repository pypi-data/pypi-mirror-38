from __future__ import print_function

import fnmatch
import hashlib
import os
import shutil
import sys
import subprocess
import traceback
import tempfile
import zipfile
import distutils.sysconfig as dsc

from glob import glob
from setuptools import find_packages
from distutils.core import setup, Extension
from setuptools.command.install import install
from setuptools.command.build_ext import build_ext
from setuptools.command.egg_info import egg_info
from setuptools import setup, Distribution
from multiprocessing import Process


try:
    import pip._internal.pep425tags as pep425tags
    pep425tags.get_supported()
    raise Exception()
except Exception as e:
    import pep425tags

try:
    from urllib.request import urlretrieve
except BaseException:
    from urllib import urlretrieve


PACKAGE_NAME = 'supersqlite'
PACKAGE_SHORT_NAME = 'supersqlite'
DOWNLOAD_REQ_WHEELS = []


def copy_sqlite(src, dest, apsw=False):
    """ Copy the SQLite amalgamation """
    shutil.copy(
        os.path.join(src, 'sqlite3.c'), os.path.join(dest, 'sqlite3.c.pre.c'))
    shutil.copy(
        os.path.join(src, 'sqlite3.h'), os.path.join(dest, 'sqlite3.h'))
    shutil.copy(
        os.path.join(src, 'sqlite3ext.h'), os.path.join(dest, 'sqlite3ext.h'))
    shutil.copy(
        os.path.join(src, 'shell.c'), os.path.join(dest, 'shell.c'))
    if apsw:
        shutil.copy(
            os.path.join(src, 'apsw_shell.c'), os.path.join(dest, 'shell.c'))
    SQLITE_PRE = os.path.join(dest, 'sqlite3.c.pre.c')
    SQLITE_POST = os.path.join(dest, 'sqlite3.c')
    with open(SQLITE_POST, 'w+') as outfile:
        with open(SQLITE_PRE, 'r') as infile:
            for line in infile:
                outfile.write(line)
        outfile.write('''
        #ifndef PLASTICITY_SUPERSQLITE_SQLITE3_C_SHIM
            # define PLASTICITY_SUPERSQLITE_SQLITE3_C_SHIM 1
            #ifdef sqlite3_progress_handler
              #undef sqlite3_progress_handler
            #endif
            #ifdef sqlite3_column_decltype
              #undef sqlite3_column_decltype
            #endif
            #ifdef sqlite3_enable_shared_cache
              #undef sqlite3_enable_shared_cache
            #endif\n
        ''' + '\n')
        outfile.write(
            'void sqlite3_progress_handler(sqlite3* a, int b, int (*c)(void*), void* d){ }' +
            '\n')
        outfile.write('''
        const char *sqlite3_column_decltype(sqlite3_stmt* stmt, int col) {
            int datatype = sqlite3_column_type(stmt, col);
            if (datatype == SQLITE_INTEGER) {
                return "integer";
            } else if (datatype == SQLITE_FLOAT) {
                return "float";
            } else if (datatype == SQLITE_TEXT) {
                return "text";
            } else if (datatype == SQLITE_BLOB) {
                return "blob";
            } else if (datatype == SQLITE_NULL) {
                return "null";
            } else {
                return "other";
            }
        }''' + '\n')
        outfile.write('''
        int sqlite3_enable_shared_cache(int a) {
            return SQLITE_ERROR;
        }
        ''' + '\n')
        outfile.write('#endif\n')


def get_modules(THIRD_PARTY, INTERNAL, PROJ_PATH,
                SO_SUFFIX, source_for_module_with_pyinit):
    """ Get all modules this package needs compiled """
    PYSQLITE2 = INTERNAL + '/pysqlite2'
    APSW = INTERNAL + '/apsw'
    PYSQLITE = THIRD_PARTY + '/_pysqlite'
    APSW_TP = THIRD_PARTY + '/_apsw'
    SQLITE3 = THIRD_PARTY + '/sqlite3'
    ICU_UNIX = SQLITE3 + '/icu_unix'
    ICU_WIN32 = SQLITE3 + '/icu_win32'
    includes = [os.path.relpath(SQLITE3, PROJ_PATH)]
    libraries = [os.path.relpath(SQLITE3, PROJ_PATH)]
    link_args = ["-flto"]
    if sys.platform == 'win32':
        libraries.append(ICU_WIN32)
        includes.append(ICU_WIN32)
        link_args.append('-L' + ICU_WIN32)
    else:
        libraries.append(ICU_UNIX)
        includes.append(ICU_UNIX)
        link_args.append('-L' + ICU_UNIX)

    SQLITE_PRE = os.path.relpath(
        os.path.join(SQLITE3, 'sqlite3.c.pre.c'), PROJ_PATH)
    SQLITE_POST = os.path.relpath(
        os.path.join(SQLITE3, 'sqlite3.c'), PROJ_PATH)
    SQLITE_EXT = os.path.relpath(
        os.path.join(SQLITE3, 'ext'), PROJ_PATH)

    with open(SQLITE_POST, 'w+') as outfile:
        outfile.write('#define SQLITE_ENABLE_DBPAGE_VTAB 1' + '\n')
        outfile.write('#define SQLITE_ENABLE_DBSTAT_VTAB 1' + '\n')
        outfile.write('#define SQLITE_ENABLE_FTS3 1' + '\n')
        outfile.write('#define SQLITE_ENABLE_FTS3_PARENTHESIS 1' + '\n')
        outfile.write('#define SQLITE_ENABLE_FTS4 1' + '\n')
        outfile.write('#define SQLITE_ENABLE_FTS5 1' + '\n')
        outfile.write('#define SQLITE_ENABLE_GEOPOLY 1' + '\n')
        outfile.write('#define SQLITE_ENABLE_IOTRACE 1' + '\n')
        outfile.write('#define SQLITE_ENABLE_JSON1 1' + '\n')
        outfile.write('#define SQLITE_ENABLE_RBU 1' + '\n')
        outfile.write('#define SQLITE_ENABLE_RTREE 1' + '\n')
        outfile.write('#define SQLITE_ENABLE_SESSION 1' + '\n')
        outfile.write('#define SQLITE_ENABLE_SNAPSHOT 1' + '\n')
        outfile.write('#define SQLITE_ENABLE_STMTVTAB 1' + '\n')
        outfile.write('#define SQLITE_ENABLE_STAT2 1' + '\n')
        outfile.write('#define SQLITE_ENABLE_STAT3 1' + '\n')
        outfile.write('#define SQLITE_ENABLE_STAT4 1' + '\n')
        outfile.write('#define SQLITE_INTROSPECTION_PRAGMAS 1' + '\n')
        outfile.write('#define SQLITE_SOUNDEX 1' + '\n')
        # outfile.write('#define SQLITE_THREADSAFE 0' + '\n')
        outfile.write('#define SQLITE_DEFAULT_MEMSTATUS 0' + '\n')
        outfile.write('#define SQLITE_DEFAULT_WAL_SYNCHRONOUS 1' + '\n')
        outfile.write('#define SQLITE_LIKE_DOESNT_MATCH_BLOBS 1' + '\n')
        outfile.write('#define SQLITE_MAX_EXPR_DEPTH 0' + '\n')
        outfile.write('#define SQLITE_OMIT_DECLTYPE 1' + '\n')
        outfile.write('#define SQLITE_OMIT_PROGRESS_CALLBACK 1' + '\n')
        outfile.write('#define SQLITE_OMIT_SHARED_CACHE 1' + '\n')
        outfile.write('#define SQLITE_USE_ALLOCA 1' + '\n')
        outfile.write('#define SQLITE_ALLOW_COVERING_INDEX_SCAN 1' + '\n')
        outfile.write('#define SQLITE_DISABLE_DIRSYNC 1' + '\n')
        outfile.write('#define SQLITE_ENABLE_UPDATE_DELETE_LIMIT 1' + '\n')
        outfile.write('#define SQLITE_STMTJRNL_SPILL -1' + '\n')
        outfile.write('#define SQLITE_TEMP_STORE 1' + '\n')
        outfile.write('#define SQLITE_USE_URI 1' + '\n')
        outfile.write('#define SQLITE_ENABLE_EXPLAIN_COMMENTS 1' + '\n')
        outfile.write('#define SQLITE_DEFAULT_FOREIGN_KEYS 1' + '\n')
        outfile.write('#define SQLITE_MAX_LENGTH 2147483647' + '\n')
        outfile.write('#define SQLITE_MAX_COLUMN 32767' + '\n')
        outfile.write('#define SQLITE_MAX_SQL_LENGTH 2147483647' + '\n')
        outfile.write('#define SQLITE_MAX_FUNCTION_ARG 127' + '\n')
        outfile.write('#define SQLITE_MAX_COMPOUND_SELECT 65536' + '\n')
        outfile.write(
            '#define SQLITE_MAX_LIKE_PATTERN_LENGTH 2147483647' +
            '\n')
        outfile.write('#define SQLITE_MAX_VARIABLE_NUMBER 1000000000' + '\n')
        outfile.write('#define SQLITE_MAX_TRIGGER_DEPTH 2147483647' + '\n')
        outfile.write('#define SQLITE_MAX_ATTACHED 125' + '\n')
        outfile.write('#define SQLITE_MAX_PAGE_COUNT 2147483646' + '\n')
        outfile.write('\n\n\n')
        with open(SQLITE_PRE, 'r') as infile:
            for line in infile:
                outfile.write(line)
    module = 'sqlite3'
    pyinit_source = source_for_module_with_pyinit(module)
    sqlite3 = Extension('sqlite3' + SO_SUFFIX,
                        sources=[SQLITE_POST] + [pyinit_source],
                        include_dirs=includes,
                        library_dirs=libraries,
                        extra_compile_args=["-O4"],
                        extra_link_args=link_args)

    def sqlite_extension(ext, skip=[], module=None):
        module = module or ext
        pyinit_source = source_for_module_with_pyinit(module)
        return Extension(
            module + SO_SUFFIX,
            sources=([
                g for g in glob(
                    os.path.join(
                        SQLITE_EXT,
                        ext,
                        '*.c')) if os.path.basename(g) not in skip] +
                     [pyinit_source]),
            include_dirs=includes,
            library_dirs=libraries,
            extra_compile_args=["-O4"],
            extra_link_args=link_args)

    def sqlite_misc_extensions(skip=[]):
        miscs = []
        for source in glob(os.path.join(SQLITE_EXT, 'misc', '*.c')):
            if os.path.basename(source) in skip:
                continue
            module = os.path.basename(source)[:-2]
            pyinit_source = source_for_module_with_pyinit(module)
            miscs.append(
                Extension(module + SO_SUFFIX,
                          sources=[source] + [pyinit_source],
                          include_dirs=includes,
                          library_dirs=libraries,
                          extra_compile_args=["-O4"],
                          extra_link_args=link_args))
        return miscs

    async_m = sqlite_extension('async')
    expert = sqlite_extension('expert')
    # fts1 = sqlite_extension('fts1') deprecated
    # fts2 = sqlite_extension('fts2') deprecated
    fts3 = sqlite_extension('fts3', skip=['fts3_test.c'])
    fts5 = sqlite_extension('fts5built', module='fts5')
    icu = sqlite_extension('icu')
    lsm1 = sqlite_extension('lsm1')
    rbu = sqlite_extension('rbu')
    rtree = sqlite_extension('rtree', skip=['geopoly.c'])
    session = sqlite_extension('session', skip=['changeset.c',
                                                'session_speed_test.c'])
    userauth = sqlite_extension('userauth')

    return ([sqlite3, async_m, expert, fts3,
             fts5, icu, lsm1, rbu, rtree, session, userauth] +
            sqlite_misc_extensions())


def install_custom_sqlite3(THIRD_PARTY, INTERNAL):
    """ Begin install custom SQLite
    Can be safely ignored even if it fails, however, system SQLite
    imitations may prevent large database files with many columns
    from working."""
    if built_local():
        return

    PYSQLITE2 = INTERNAL + '/pysqlite2'
    APSW = INTERNAL + '/apsw'
    PYSQLITE = THIRD_PARTY + '/_pysqlite'
    APSW_TP = THIRD_PARTY + '/_apsw'
    SQLITE3 = THIRD_PARTY + '/sqlite3'

    print("Installing custom SQLite 3 (pysqlite) ....")
    install_env = os.environ.copy()
    install_env["PYTHONPATH"] = INTERNAL + \
        (':' + install_env["PYTHONPATH"] if "PYTHONPATH" in install_env else "")
    copy_sqlite(SQLITE3, PYSQLITE)
    copy_sqlite(SQLITE3, os.path.join(APSW_TP, 'src'), apsw=True)
    rc = subprocess.Popen([
        sys.executable,
        PYSQLITE + '/setup.py',
        'install',
        '--install-lib=' + INTERNAL,
    ], cwd=PYSQLITE, env=install_env).wait()
    if rc:
        print("")
        print("============================================================")
        print("=========================WARNING============================")
        print("============================================================")
        print("It seems like building a custom version of SQLite on your")
        print("machine has failed. This is fine, SuperSQLite will likely work")
        print("just fine with the sytem version of SQLite for most use cases.")
        print("However, if you are trying to load extremely high dimensional")
        print("models > 999 dimensions, you may run in to SQLite limitations")
        print("that can only be resolved by using the custom version of SQLite.")
        print("To troubleshoot make sure you have appropriate build tools on")
        print("your machine for building C programs like GCC and the standard")
        print("library. Also make sure you have the python-dev development")
        print("libraries and headers for building Python C extensions.")
        print("If you need more help with this, please reach out to ")
        print("opensource@plasticity.ai.")
        print("============================================================")
        print("============================================================")
        print("")
    else:
        print("")
        print("============================================================")
        print("=========================SUCCESS============================")
        print("============================================================")
        print("Building a custom version of SQLite on your machine has")
        print("succeeded.")
        print("Listing internal...")
        print(try_list_dir(INTERNAL))
        print("Listing internal/pysqlite2...")
        print(try_list_dir(PYSQLITE2))
        print("============================================================")
        print("============================================================")
        print("")
    print("Installing custom SQLite 3 (apsw) ....")
    rc = subprocess.Popen([
        sys.executable,
        APSW_TP + '/setup.py',
        'install',
        '--install-lib=' + INTERNAL,
    ], cwd=APSW_TP, env=install_env).wait()
    if rc:
        print("")
        print("============================================================")
        print("=========================WARNING============================")
        print("============================================================")
        print("It seems like building a custom version of SQLite on your")
        print("machine has failed. This is fine, SuperSQLite will likely work")
        print("just fine with the sytem version of SQLite for most use cases.")
        print("However, if you are trying to stream a remote model that")
        print("can only be resolved by using the custom version of SQLite.")
        print("To troubleshoot make sure you have appropriate build tools on")
        print("your machine for building C programs like GCC and the standard")
        print("library. Also make sure you have the python-dev development")
        print("libraries and headers for building Python C extensions.")
        print("If you need more help with this, please reach out to ")
        print("opensource@plasticity.ai.")
        print("============================================================")
        print("============================================================")
        print("")
    else:
        print("")
        print("============================================================")
        print("=========================SUCCESS============================")
        print("============================================================")
        print("Building a custom version of SQLite on your machine has")
        print("succeeded.")
        print("Listing internal...")
        print(try_list_dir(INTERNAL))
        print("Listing internal/apsw...")
        print(try_list_dir(APSW))
        print("============================================================")
        print("============================================================")
        print("")
        if not(os.path.exists(APSW)):
            print("Install-lib did not install APSW, installing from egg...")
            for egg in glob(INTERNAL + "/apsw-*.egg"):
                if (os.path.isfile(egg)):
                    print("Found an egg file, extracting...")
                    try:
                        zip_ref = zipfile.ZipFile(egg, 'r')
                    except BaseException:
                        print("Egg extraction error")
                        continue
                    zip_ref.extractall(APSW)
                else:
                    print("Found an egg folder, renaming...")
                    os.rename(egg, APSW)
                print("Renaming apsw.py to __init__.py")
                os.rename(
                    os.path.join(
                        APSW, 'apsw.py'), os.path.join(
                        APSW, '__init__.py'))


def custom_compile(THIRD_PARTY, INTERNAL):
    """ Compile resources this package needs """
    install_custom_sqlite3(THIRD_PARTY, INTERNAL)


# Redirect output to a file
tee = open(
    os.path.join(
        tempfile.gettempdir(),
        PACKAGE_SHORT_NAME +
        '.install'),
    'a+')


class TeeUnbuffered:
    def __init__(self, stream):
        self.stream = stream
        self.errors = ""

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
        tee.write(data)
        tee.flush()

    def flush(self):
        self.stream.flush()
        tee.flush()


sys.stdout = TeeUnbuffered(sys.stdout)
sys.stderr = TeeUnbuffered(sys.stderr)

# Setup path constants
PROJ_PATH = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
THIRD_PARTY = PROJ_PATH + '/' + PACKAGE_NAME + '/third_party'
BUILD_PATH = PROJ_PATH + '/build'
BUILD_THIRD_PARTY = BUILD_PATH + '/lib/' + PACKAGE_NAME + '/third_party'
INTERNAL = THIRD_PARTY + '/internal'
SO_SUFFIX = '00000' + ''.join(format(ord(x), 'b') for x in PACKAGE_NAME)
BINARY_EXTENSIONS = ('.so', '.pyd', '.dll', '.o', '.obj', '.lib')

# Get the package version
__version__ = None
with open(os.path.join(PROJ_PATH, 'version.py')) as f:
    exec(f.read())

# Setup remote wheel configurations
RM_WHEELHOUSE = 'https://s3.amazonaws.com/' + \
    PACKAGE_SHORT_NAME + '.plasticity.ai/wheelhouse/'
TRIED_DOWNLOADING_WHEEL = os.path.join(
    tempfile.gettempdir(),
    PACKAGE_NAME +
    '-' +
    __version__ +
    '-' +
    hashlib.md5(PROJ_PATH.encode('utf-8')).hexdigest() +
    '.whldownload'
)
INSTALLED_FROM_WHEEL = os.path.join(
    tempfile.gettempdir(),
    PACKAGE_NAME +
    '-' +
    __version__ +
    '-' +
    hashlib.md5(PROJ_PATH.encode('utf-8')).hexdigest() +
    '.whlinstall'
)
BUILT_LOCAL = os.path.join(
    tempfile.gettempdir(),
    PACKAGE_NAME +
    '-' +
    __version__ +
    '-' +
    hashlib.md5(PROJ_PATH.encode('utf-8')).hexdigest() +
    '.buildlocal'
)
BUILT_EXT = os.path.join(
    tempfile.gettempdir(),
    PACKAGE_NAME +
    '-' +
    __version__ +
    '-' +
    hashlib.md5(PROJ_PATH.encode('utf-8')).hexdigest() +
    '.buildext'
)


def try_list_dir(d):
    """ Return a list of files in a directory """
    try:
        return os.listdir(d)
    except BaseException:
        return []


def get_supported_wheels(package_name=PACKAGE_NAME, version=__version__):
    """Get supported wheel strings"""
    def tuple_invalid(t):
        return (
            t[1] == 'none' or
            'fat32' in t[2] or
            'fat64' in t[2] or
            '_universal' in t[2]
        )
    return ['-'.join((package_name, version) + t) + '.whl'
            for t in pep425tags.get_supported() if not(tuple_invalid(t))]


def install_wheel(whl):
    """Installs a wheel file"""
    whl_args = [
        sys.executable,
        '-m',
        'pip',
        'install',
        '--ignore-installed',
    ]
    rc = subprocess.Popen(whl_args + [whl]).wait()
    if rc != 0:
        try:
            import site
            if hasattr(site, 'getusersitepackages'):
                site_packages = site.getusersitepackages()
                print("Installing to user site packages...", site_packages)
                rc = subprocess.Popen(whl_args + ["--user"] + [whl]).wait()
        except ImportError:
            pass
    return rc


def skip_wheel():
    """ Checks if a wheel install should be skipped """
    return "SKIP_" + PACKAGE_SHORT_NAME.upper() + "_WHEEL" in os.environ


def installed_wheel():
    """Checks if a pre-compiled remote wheel was installed"""
    return os.path.exists(INSTALLED_FROM_WHEEL)


def tried_downloading_wheel():
    """Checks if already tried downloading a wheel"""
    return os.path.exists(TRIED_DOWNLOADING_WHEEL)


def built_local():
    """Checks if built out the project locally"""
    return os.path.exists(BUILT_LOCAL)


def built_ext():
    """Checks if built out the extensions"""
    return os.path.exists(BUILT_EXT)


def download_and_install_wheel():
    """Downloads and installs pre-compiled remote wheels"""
    if skip_wheel():
        return False
    if installed_wheel():
        return True
    if tried_downloading_wheel():
        return False
    print("Downloading and installing wheel (if it exists)...")
    tmpwhl_dir = tempfile.gettempdir()
    for whl in get_supported_wheels():
        exitcodes = []
        whl_url = RM_WHEELHOUSE + whl
        dl_path = os.path.join(tmpwhl_dir, whl)
        try:
            print("Trying...", whl_url)
            urlretrieve(whl_url, dl_path)
        except BaseException:
            print("FAILED")
            continue
        extract_dir = os.path.join(
            tempfile.gettempdir(), whl.replace(
                '.whl', ''))
        extract_dir = os.path.join(
            tempfile.gettempdir(), whl.replace(
                '.whl', ''))
        try:
            zip_ref = zipfile.ZipFile(dl_path, 'r')
        except BaseException:
            print("FAILED")
            continue
        zip_ref.extractall(extract_dir)
        for ewhl in glob(extract_dir + "/*/req_wheels/*.whl"):
            print("Installing requirement wheel: ", ewhl)
            package_name = os.path.basename(ewhl).split('-')[0]
            version = os.path.basename(ewhl).split('-')[1]
            requirement = package_name + ">=" + version
            print("Checking if requirement is met: ", requirement)
            req_rc = subprocess.Popen([
                sys.executable,
                '-c',
                "import importlib;"
                "import pkg_resources;"
                "pkg_resources.require('" + requirement + "');"
                "importlib.import_module('" + package_name + "');"
            ]).wait()
            if req_rc == 0:
                print("Requirement met...skipping install of: ", package_name)
            else:
                print("Requirement not met...installing: ", package_name)
                exitcodes.append(install_wheel(ewhl))
        print("Installing wheel: ", dl_path)
        exitcodes.append(install_wheel(dl_path))
        zip_ref.extractall(PROJ_PATH)
        zip_ref.close()
        if len(exitcodes) > 0 and max(exitcodes) == 0 and min(exitcodes) == 0:
            open(TRIED_DOWNLOADING_WHEEL, 'w+').close()
            print("Done downloading and installing wheel")
            return True
    open(TRIED_DOWNLOADING_WHEEL, 'w+').close()
    print("Done trying to download and install wheel (it didn't exist)")
    return False


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


def build_req_wheels():
    """Builds requirement wheels"""
    if built_local():
        return
    print("Building requirements wheels...")

    # Get wheels from PyPI
    rc = subprocess.Popen([
        sys.executable,
        '-m',
        'pip',
        'wheel',
        '-r',
        'requirements.txt',
        '--wheel-dir=' + PACKAGE_NAME + '/req_wheels'
    ], cwd=PROJ_PATH).wait()

    # Download wheels
    for wheelhouse, package, versions in DOWNLOAD_REQ_WHEELS:
        req_dl_success = False
        for version in versions:
            for whl in get_supported_wheels(package, version):
                exitcodes = []
                whl_url = wheelhouse + whl
                sys.stdout.write("Trying to download... '" + whl_url + "'")
                dl_path = os.path.join(PACKAGE_NAME + '/req_wheels', whl)
                try:
                    urlretrieve(whl_url, dl_path)
                    zip_ref = zipfile.ZipFile(dl_path, 'r')
                    req_dl_success = True
                    sys.stdout.write(" ...SUCCESS\n")
                except BaseException:
                    if os.path.exists(dl_path):
                        os.remove(dl_path)
                    sys.stdout.write(" ...FAIL\n")
                    continue
                sys.stdout.flush()
        # Try to get it from PyPI as last resort
        if not req_dl_success:
            rc2 = subprocess.Popen([
                sys.executable,
                '-m',
                'pip',
                'wheel',
                package,
                '--wheel-dir=' + PACKAGE_NAME + '/req_wheels'
            ], cwd=PROJ_PATH).wait()

    if rc:
        print("Failed to build requirements wheels!")
        pass


def install_req_wheels():
    """Installs requirement wheels"""
    print("Installing requirements wheels...")
    for whl in glob(PACKAGE_NAME + '/req_wheels/*.whl'):
        rc = install_wheel(whl)
    print("Done installing requirements wheels")


def install_requirements():
    """Installs requirements.txt"""
    print("Installing requirements...")
    rc = subprocess.Popen([
        sys.executable,
        '-m',
        'pip',
        'install',
        '-r',
        'requirements.txt'
    ], cwd=PROJ_PATH).wait()
    if rc:
        print("Failed to install some requirements!")
    print("Done installing requirements")


def get_site_packages():
    """ Gets all site_packages paths """
    try:
        import site
        if hasattr(site, 'getsitepackages'):
            site_packages = site.getsitepackages()
        else:
            from distutils.sysconfig import get_python_lib
            site_packages = [get_python_lib()]
        if hasattr(site, 'getusersitepackages'):
            site_packages = site_packages + [site.getusersitepackages()]
        return site_packages
    except BaseException:
        return []


def source_for_module_with_pyinit(module):
    """ Create PyInit symbols for shared objects compiled with Python's
        Extension()"""
    source_file = os.path.join(tempfile.mkdtemp(), module + '.c')
    with open(source_file, 'w+') as outfile:
        outfile.write('''
            void init''' + (module + SO_SUFFIX) + '''() {} //Python 2.7
            void PyInit_''' + (module + SO_SUFFIX) + '''() {} //Python 3.5
        ''')
    return os.path.relpath(source_file, PROJ_PATH)


def delete_shared_objects():
    """ Deletes shared object files made with build_ext from site_packages """
    site_packages = get_site_packages()
    for site_pack in site_packages:
        print("Deleting shared objects...", os.path.abspath(site_pack))
        for root, dirnames, filenames in list(os.walk(site_pack)):
            for filename in filenames:
                if filename.lower().endswith(BINARY_EXTENSIONS):
                    so = os.path.join(root, filename)
                    so_base = os.path.basename(so)
                    if SO_SUFFIX in so_base:
                        print("Deleting", so)
                        os.remove(so)


def get_shared_object_ext():
    """ Return the extension of shared objects on the current system """
    if sys.platform == 'win32':
        return '.dll'
    else:
        return '.so'


def copy_shared_objects():
    """ Copies shared object files made with build_ext to /third_party/ """
    print("Copying shared objects...", os.path.abspath(BUILD_PATH))
    for root, dirnames, filenames in list(os.walk(BUILD_PATH)):
        for filename in filenames:
            if filename.lower().endswith(BINARY_EXTENSIONS):
                so = os.path.join(root, filename)
                so_base = os.path.basename(so)
                if SO_SUFFIX in so_base:
                    p_ext = '.' + PACKAGE_NAME
                    ext = get_shared_object_ext()
                    so_base_new = so_base.replace(SO_SUFFIX, p_ext)
                    so_base_new = '.'.join(so_base_new.split('.')[:-2])
                    if not so_base_new.endswith(p_ext):
                        so_base_new += p_ext
                    so_base_new = so_base_new + ext
                    dest_1 = os.path.join(BUILD_THIRD_PARTY, so_base_new)
                    dest_2 = os.path.join(THIRD_PARTY, so_base_new)
                    try:
                        os.makedirs(os.path.dirname(dest_1))
                    except BaseException:
                        pass
                    try:
                        os.makedirs(os.path.dirname(dest_2))
                    except BaseException:
                        pass
                    print("Copying from", so, "-->", dest_1)
                    shutil.copyfile(so, dest_1)
                    print("Copying from", so, "-->", dest_2)
                    shutil.copyfile(so, dest_2)
                    print("Deleting", so)
                    os.remove(so)
    delete_shared_objects()


def early_build_shared_objects():
    print("Early building of shared objects...")
    rc = subprocess.Popen([
        sys.executable,
        os.path.abspath(__file__),
        'build_ext'
    ]).wait()


def copy_custom_compile():
    """Copy the third party folders into site-packages under
    PACKAGE_NAME/third_party/ and
    ./build/lib/PACKAGE_NAME/third_party/
    for good measure"""

    # Copy locally installed libraries
    from distutils.dir_util import copy_tree
    try:
        site_packages = get_site_packages()
        cp_from = THIRD_PARTY + '/'
        for site_pack in site_packages:
            for globbed in glob(site_pack + '/' + PACKAGE_NAME + '*/'):
                try:
                    cp_to = (globbed + '/' + PACKAGE_NAME +
                             '/third_party/')
                except IndexError as e:
                    print(
                        "Site Package: '" +
                        site_pack +
                        "' did not have " + PACKAGE_NAME)
                    continue
                print("Copying from: ", cp_from, " --> to: ", cp_to)
                copy_tree(cp_from, cp_to)
    except Exception as e:
        print("Error copying internal pysqlite folder to site packages:")
        traceback.print_exc(e)
    try:
        cp_from = THIRD_PARTY + '/'
        cp_to = BUILD_THIRD_PARTY + '/'
        print("Copying from: ", cp_from, " --> to: ", cp_to)
        copy_tree(cp_from, cp_to)
    except Exception as e:
        print("Error copying internal pysqlite folder to build folder:")
        traceback.print_exc(e)


def delete_pip_files():
    """Delete random pip files"""
    try:
        from pip.utils.appdirs import user_cache_dir
    except BaseException:
        try:
            from pip._internal.utils.appdirs import user_cache_dir
        except BaseException:
            return
    for root, dirnames, filenames in os.walk(user_cache_dir('pip/wheels')):
        for filename in fnmatch.filter(filenames, PACKAGE_NAME + '-*.whl'):
            try:
                whl = os.path.join(root, filename)
                print("Deleting...", whl)
                os.remove(whl)
            except BaseException:
                pass
    try:
        site_packages = get_site_packages()
        for site_pack in site_packages:
            for globbed in glob(site_pack + '/' + PACKAGE_NAME + '*/'):
                try:
                    if globbed.endswith('.dist-info/'):
                        shutil.rmtree(globbed)
                except BaseException:
                    pass
    except BaseException:
        pass


cmdclass = {}

try:
    from wheel.bdist_wheel import bdist_wheel as bdist_wheel_

    class CustomBdistWheelCommand(bdist_wheel_):
        def run(self):
            if not(download_and_install_wheel()):
                custom_compile(THIRD_PARTY, INTERNAL)
                early_build_shared_objects()
                copy_shared_objects()
                build_req_wheels()
                open(BUILT_LOCAL, 'w+').close()
            print("Running wheel...")
            bdist_wheel_.run(self)
            print("Done running wheel")
            copy_custom_compile()

    cmdclass['bdist_wheel'] = CustomBdistWheelCommand

except ImportError as e:
    pass


class CustomInstallCommand(install):
    def run(self):
        if not(download_and_install_wheel()):
            custom_compile(THIRD_PARTY, INTERNAL)
            early_build_shared_objects()
            copy_shared_objects()
            install_req_wheels()
            open(BUILT_LOCAL, 'w+').close()
        print("Running install...")
        p = Process(target=install.run, args=(self,))
        p.start()
        p.join()
        print("Done running install")
        if not(download_and_install_wheel()):
            print("Running egg_install...")
            p = Process(target=install.do_egg_install, args=(self,))
            p.start()
            p.join()
            install_requirements()
            print("Done running egg_install")
        else:
            print("Skipping egg_install")
        copy_custom_compile()

    def finalize_options(self):
        install.finalize_options(self)
        if self.distribution.has_ext_modules():
            self.install_lib = self.install_platlib


class CustomBuildExtCommand(build_ext):
    def run(self):
        if not built_ext():
            build_ext.run(self)
            copy_shared_objects()
        else:
            print("Skipping build_ext, already built")
        open(BUILT_EXT, 'w+').close()


cmdclass['install'] = CustomInstallCommand
cmdclass['build_ext'] = CustomBuildExtCommand


class BinaryDistribution(Distribution):
    def has_ext_modules(foo):
        return True


MODULES = get_modules(THIRD_PARTY, INTERNAL, PROJ_PATH,
                      SO_SUFFIX, source_for_module_with_pyinit)

if __name__ == '__main__':

    # Attempt to install from a remote pre-compiled wheel
    if any([a in sys.argv for a in ['egg_info', 'install']]):
        if download_and_install_wheel():
            open(INSTALLED_FROM_WHEEL, 'w+').close()

    # Only create requirements if not installing from a wheel
    if any([a in sys.argv for a in ['bdist_wheel', 'sdist', 'egg_info']]):
        # The wheel shouldn't have any reqs
        # since it gets packaged with all of its req wheels
        reqs = []
    elif not any([a in sys.argv for a in ['-V']]):
        reqs = parse_requirements('requirements.txt')
        for wheelhouse, package, versions in DOWNLOAD_REQ_WHEELS:
            if package not in reqs:
                reqs.append(package)
        print("Adding requirements: ", reqs)
    else:
        reqs = []

    # Delete pip files
    delete_pip_files()

    setup(
        name=PACKAGE_NAME,
        packages=find_packages(
            exclude=[
                'tests',
                'tests.*']),
        version=__version__,
        description='A supercharged SQLite library for Python.',
        long_description="""
    About
    -----
    A feature-packed Python package and for utilizing SQLite in Python by `Plasticity <https://www.plasticity.ai/>`_. It is intended to be a drop-in replacement to Python's built-in `SQLite API <https://docs.python.org/3/library/sqlite3.html>`_, but without any limitations. It offers unique features like remote streaming over HTTP and bundling of extensions like JSON, R-Trees (geospatial indexing), and Full Text Search.

    Documentation
    -------------
    You can see the full documentation and README at the `GitLab repository <https://gitlab.com/Plasticity/supersqlite>`_ or the `GitHub repository <https://github.com/plasticityai/supersqlite>`_.
        """,
        author='Plasticity',
        author_email='opensource@plasticity.ai',
        url='https://gitlab.com/Plasticity/supersqlite',
        keywords=[
                    'supersqlite',
                    'sqlite',
                    'sqlite3',
                    'apsw',
                    'pysqlite',
                    'sql',
                    'embedded',
                    'database',
                    'db',
                    'http',
                    'remote',
                    'stream',
                    'full',
                    'text',
                    'fulltext',
                    'full-text',
                    'json',
                    'lsm',
                    'blob',
                    'vfs',
                    'fts4',
                    'fts5'],
        license='MIT',
        include_package_data=True,
        install_requires=reqs,
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            'Intended Audience :: Developers',
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Operating System :: OS Independent",
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.0',
            'Programming Language :: Python :: 3.7'],
        cmdclass=cmdclass,
        distclass=BinaryDistribution,
        ext_modules=MODULES
    )

    # Delete pip files
    delete_pip_files()
