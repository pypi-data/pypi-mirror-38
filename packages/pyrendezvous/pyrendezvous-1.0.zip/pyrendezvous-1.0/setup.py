from distutils.core import setup, Extension
import argparse
import sys
import os
import shutil
import glob
import tempfile

SUPPORTED_PLATFORMS = ['linux', 'linux2']

SDIST_PARAMETER = 'sdist'
DEPENDENCY_PREFIX = 'dependency_'
PKG_INFO_FILE = 'PKG-INFO'
INIT_FILE = '__init__.py'
VERSION_ATTRIBUTE = 'Version:'
SUBPACKAGE_SEPARATOR = '.'

PACKAGES = ['framework',
            'framework.transports',
            'framework.transports.ipv4']
DEPENDENCIES = {'framework': ['*.pyi'],
                'framework.transports': ['*.pyi'],
                'framework.transports.ipv4': ['*.pyi']}


def is_subpackage(package):
    return SUBPACKAGE_SEPARATOR in package


def import_packages(path, packages):
    current = os.path.abspath(os.path.curdir)

    # copy files
    for package in packages:
        if not is_subpackage(package):
            package_dir = os.path.join(current, package)
            shutil.copytree(os.path.join(path, package), package_dir)

    return packages


def import_dependencies(paths):
    current = os.path.abspath(os.path.curdir)

    dependencies = {}
    dependency_index = 0
    for path in paths:
        dependency_index += 1
        name = 'dependency_{}'.format(dependency_index)

        # copy files
        dependency_dir = os.path.join(current, name)
        shutil.copytree(path, dependency_dir)

        dependencies[name] = [os.path.relpath(filename, dependency_dir)
                              for filename in glob.iglob(dependency_dir + '/**/*', recursive=True)]

    return dependencies


def import_extensions(path, dependencies):
    cpp_files = [os.path.relpath(filename, path)
                 for filename in glob.iglob(os.path.abspath(path) + '/**/*.cpp', recursive=True)]

    extensions = []
    for cpp_file in cpp_files:
        _, filename = os.path.split(cpp_file)
        name, _ = os.path.splitext(filename)

        extension = Extension(name=name,
                              sources=[cpp_file],
                              include_dirs=['/usr/local/include'] +
                                           [dependency_name for dependency_name in dependencies.keys()],
                              libraries=[],
                              library_dirs=['/usr/local/lib'],
                              extra_compile_args=['-O3', '-std=c++14'],
                              language='C++')
        extensions.append(extension)

    return extensions


def detect_dependencies():
    current = os.path.abspath(os.path.curdir)
    return [subpath for subpath in os.listdir(current)
            if os.path.isdir(os.path.join(current, subpath)) and subpath.startswith(DEPENDENCY_PREFIX)]


def detect_extensions(packages, dependencies):
    current = os.path.abspath(os.path.curdir)

    extensions = []
    for package in packages:
        package_dir = os.path.join(current, package.replace(SUBPACKAGE_SEPARATOR, os.path.sep))

        cpp_files = [os.path.relpath(filename, current)
                     for filename in glob.iglob(os.path.abspath(package_dir) + '/*.cpp', recursive=False)]

        for cpp_file in cpp_files:
            _, filename = os.path.split(cpp_file)
            name, _ = os.path.splitext(filename)

            extension = Extension(name=name,
                                  sources=[cpp_file],
                                  include_dirs=dependencies,
                                  libraries=['rt', 'stdc++'],
                                  extra_compile_args=['-std=c++14'],
                                  language='C++')
            extensions.append(extension)

    return extensions


def detected_version():
    current = os.path.abspath(os.path.curdir)

    with open(PKG_INFO_FILE, 'r') as pkg_info:
        for line in pkg_info.readlines():
            if line.startswith(VERSION_ATTRIBUTE):
                return line.replace(VERSION_ATTRIBUTE, '').strip(' ')

    return 'unknown'


def append_version(packages, version):
    current = os.path.abspath(os.path.curdir)

    for package in packages:
        if not is_subpackage(package):
            package_dir = os.path.join(current, package)
            init_file = os.path.join(package_dir, INIT_FILE)
            with open(init_file, 'a') as f:
                f.writelines(['\n', '\n', '__version__ = "{}"'.format(version), '\n'])


if __name__ == '__main__':
    if sys.platform not in SUPPORTED_PLATFORMS:
        raise RuntimeError('{} is currently unsupported!'.format(sys.platform))

    if sys.version_info < (3,):
        raise RuntimeError('Python 2.x is not supported as for now!')

    if SDIST_PARAMETER in sys.argv:
        parser = argparse.ArgumentParser()
        parser.add_argument('--src-dir', required=True,
                            help="Source directory from which packages should be loaded")
        parser.add_argument('--deps-dirs', nargs='+',
                            help="A list of directories with dependent header based libraries.")
        parser.add_argument('--version', default='unknown',
                            help="Version to build the package with")

        args, unknown_args = parser.parse_known_args()

        with tempfile.TemporaryDirectory() as tmpdirname:
            os.chdir(tmpdirname)

            print('Running from {}'.format(tmpdirname))

            shutil.copy2(__file__, tmpdirname)

            import_packages(args.src_dir, PACKAGES)
            dependencies = import_dependencies(args.deps_dirs)
            extensions = import_extensions(args.src_dir, dependencies)

            append_version(PACKAGES, args.version)

            sys.argv = sys.argv[:1] + unknown_args
            setup(name='pyrendezvous',
                  version=args.version,
                  description='Python binding for rendezvous',
                  author='Lukasz Laszko',
                  author_email='lukaszlaszko@gmail.com',
                  license='MIT',
                  classifiers=[
                      'Development Status :: 4 - Beta',
                      'Intended Audience :: Developers',
                      'License :: OSI Approved :: MIT License',
                      'Programming Language :: Python',
                      'Operating System :: POSIX :: Linux',
                      'Topic :: Communications',
                      'Topic :: Internet',
                      'Topic :: Software Development',
                      'Topic :: System',
                      'Topic :: System :: Networking',
                  ],
                  platforms='Posix',
                  url='https://bitbucket.org/lukaszlaszko/pyrendezvous',
                  long_description='Python binding for rendezvous. Efficient networking made easy.',
                  packages=PACKAGES + [dependency_name for dependency_name in dependencies.keys()],
                  package_data={**DEPENDENCIES, **dependencies},
                  data_files=[],
                  ext_modules=extensions)
    else:
        dependencies = detect_dependencies()
        extensions = detect_extensions(PACKAGES, dependencies)
        version = detected_version()
        setup(name='pyrendezvous',
              version=version,
              description='Python binding for rendezvous',
              author='Lukasz Laszko',
              author_email='lukaszlaszko@gmail.com',
              url='https://bitbucket.org/lukaszlaszko/pyrendezvous',
              long_description='',
              packages=PACKAGES,
              package_data=DEPENDENCIES,
              ext_modules=extensions)