# -*- coding: utf-8 -*-
import os
import sys
import json
import argparse

from subprocess import Popen, PIPE
from virtualenv import create_environment

from spip import __version__
from spip.logger import Logger, Verbosity, Color

_logger = Logger()

_skipping_packages = [
    'spip',
    'python',
    'wsgiref',
    'argparse',
    'pip',
    'setuptools',
    'distribute',
    'wheel'
]

_spip_path = "%s/spip.json" % os.getcwd()
_venv_home = "%s/venv" % os.getcwd()
_venv_path = "%s/bin/activate_this.py" % _venv_home

_get_dependencies_code = """from pkg_resources import working_set

for p in working_set:
    result = p.project_name
    deps = [dep.project_name + ('@' + str(dep.specifier) if dep.specifier else '') for dep in p.requires()]
    print(result + '/' + '$'.join(deps))
"""

parser = argparse.ArgumentParser(prog="spip")
parser.add_argument('-V', '--version', action="store_true",
                    help='Print the spip version number and exit')
parser.add_argument('-v', '--verbose', action="store_true",
                    help='Print more output.')
parser.add_argument('-q', '--quiet', action="store_true",
                    help='Print nothing except errors.')
parser.add_argument('-qq', '--no-output', action="store_true",
                    help='Print nothing.')

subparsers = parser.add_subparsers(dest='which', help='all possible commands')

init_parser = subparsers.add_parser(
    'init', help='initialize new python application')
init_parser.add_argument('path', nargs='?', default='.')

add_parser = subparsers.add_parser('add', help='install packages')
add_parser.add_argument('-U', '--upgrade', action='store_true',
                        help='Upgrade packages')
add_parser.add_argument('packages', nargs='+')

remove_parser = subparsers.add_parser('remove', help='uninstall packages')
remove_parser.add_argument('packages', nargs='+')

deps_parser = subparsers.add_parser(
    'deps', help='show dependencies of installed packages')

info_parser = subparsers.add_parser(
    'info', help='get information of the package from PyPi')
info_parser.add_argument('package')

freeze_parser = subparsers.add_parser(
    'freeze', help='get a list of installed packges')


def _set_logger_verbosity(args):
    """Set Logger Verbosity with parsed arguments"""
    if args.verbose:
        _logger.verbosity = Verbosity.DEBUG
    if args.quiet:
        _logger.verbosity = Verbosity.ERROR
    if args.no_output:
        _logger.verbosity = Verbosity.NO_OUTPUT

    _logger.debug("Logger Verbosity: %s" % (_logger.verbosity))


def _print_version():
    """print version of this tool"""
    short_version = "%s.%s.%s" % (
        sys.version_info.major,
        sys.version_info.minor,
        sys.version_info.micro
    )
    _logger.always("Simple PIP \"%s\" from \"%s\" (%s)" %
                   (__version__, sys.argv[0], short_version))


def _check_virtualenv_exists():
    """returns True if virtualenv already created"""
    if not os.path.exists(_spip_path):
        _logger.error(
            "You have to initialize the application with Simple PIP.")

        return False

    if not os.path.exists(_venv_path):
        _logger.error("Is your application using spip?🧐  " +
                      "Check virtualenv is created in `./venv`.")

        return False

    return True


def _activate_venv():
    _logger.debug('activate %s' % _venv_path)
    with open(_venv_path) as f:
        exec(f.read(), {'__file__': _venv_path})


def _get_pip_path():
    return os.path.join(_venv_home, 'bin', 'pip')


def _get_python_path():
    return os.path.join(_venv_home, 'bin', 'python')


def _outdated_pip_warning(stderr):
    if "You are using pip version" in stderr.decode('utf8'):
        _logger.default("You should upgrade pip. `spip add -U pip`")


def _get_installed_packages():
    pip_path = _get_pip_path()
    _logger.debug("pip path : %s" % pip_path)

    p = Popen([pip_path, 'freeze'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()

    _outdated_pip_warning(stderr)

    return [x for x in stdout.decode('utf8').split('\n') if x]


def _get_dependencies():
    python_path = _get_python_path()
    p = Popen([python_path, '-c', _get_dependencies_code],
              stdout=PIPE, stderr=PIPE)
    stdout, _ = p.communicate()

    packages = stdout.decode('utf8').split('\n')
    dependencies = {
        x.split('/')[0]: x.split('/')[1].split('$')
        for x in packages if x
    }

    return dependencies


def _create_virtualenv():
    # TODO create virutalenv with selected python version
    # refer
    #        from virtualenv import resolve_interpreter
    #        print(resolve_interpreter('python3.4'))
    _logger.default('Home dir of virutalenv will be `%s`.' % _venv_home)
    _logger.default('Creating virtualenv...')
    create_environment(_venv_home)
    _logger.default('Creating virtualenv is complete.')


def _install(packages, upgrade=False):
    _logger.debug("install packges: %s" % ", ".join(packages))
    pip_path = _get_pip_path()
    _logger.debug("pip path : %s" % pip_path)

    params = [pip_path, 'install']
    if upgrade:
        params.append('-U')

    params.extend(packages)

    p = Popen(params, stdout=PIPE, stderr=PIPE)
    _, stderr = p.communicate()

    _outdated_pip_warning(stderr)


def _remove(packages):
    _logger.debug("remove packges: %s" % ", ".join(packages))
    pip_path = _get_pip_path()
    _logger.debug("pip path : %s" % pip_path)

    params = [pip_path, 'uninstall', '-y']
    params.extend(packages)

    p = Popen(params, stdout=PIPE, stderr=PIPE)
    _, stderr = p.communicate()

    _outdated_pip_warning(stderr)


def _add_packages_into_spip(packages):
    installed_packages = [x.split('==') for x in _get_installed_packages()]
    installed_packages = {x[0].lower(): x[1] for x in installed_packages}

    with open(_spip_path) as f:
        project = json.loads(f.read())
        if 'dependencies' not in project:
            project['dependencies'] = {}

        for package in packages:
            if package not in _skipping_packages:
                project['dependencies'][package] = installed_packages[package.lower()]

    with open(_spip_path, 'w') as f:
        f.write(json.dumps(project, indent=2, ensure_ascii=False, sort_keys=True))


def _remove_packages_from_spip(packages):
    with open(_spip_path) as f:
        project = json.loads(f.read())

    if 'dependencies' not in project:
        return

    project['dependencies'] = {
        k: v for k, v in project['dependencies'].items() if k not in packages}

    with open(_spip_path, 'w') as f:
        f.write(json.dumps(project, indent=2, ensure_ascii=False, sort_keys=True))


def _get_application_info():
    # application name
    current_dir = os.path.basename(os.getcwd())
    application_name = input("{}✔{} application name ({}): ".format(
        Color.GREEN, Color.RESET, current_dir)).strip()

    if ' ' in application_name or '\t' in application_name:
        _logger.error('Cannot initialize an application. ' +
                      'Application name should not contain whitespaces.')
        return None

    if not application_name:
        application_name = current_dir

    # version
    version = input("{}✔{} version (0.0.1): ".format(
        Color.GREEN, Color.RESET)).strip()

    if not version:
        version = '0.0.1'

    # description
    description = input("{}✔{} description (None): ".format(
        Color.GREEN, Color.RESET)).strip()

    if not description:
        description = None

    _logger.always("")

    return {
        "name": application_name,
        "version": version,
        "description": description
    }


def fetch_info_from_pypi(name):
    try:
        import urllib.request as urlrequest
    except ImportError:
        import urllib as urlrequest

    url = "https://pypi.python.org/pypi/%s/json" % name

    resp = urlrequest.urlopen(url).read()

    if type(resp) == bytes:
        # for python2
        resp = resp.decode('utf8')

    resp = json.loads(resp)

    _logger.always('%sTitle\t\t:%s %s' %
                   (
                       Color.GRAY,
                       Color.RESET,
                       resp['info']['name']
                   ))
    _logger.always('%sAuthor\t\t:%s %s <%s>' %
                   (
                       Color.GRAY,
                       Color.RESET,
                       resp['info']['author'],
                       resp['info']['author_email']
                   ))
    _logger.always('%sSummary\t\t:%s %s' %
                   (
                       Color.GRAY,
                       Color.RESET,
                       resp['info']['summary']
                   ))
    _logger.always('%sHomepage\t:%s %s' %
                   (
                       Color.GRAY,
                       Color.RESET,
                       resp['info']['home_page']
                   ))
    _logger.always('%sClassifiers\t:%s\n%s' %
                   (
                       Color.GRAY,
                       Color.RESET,
                       "\n".join(resp['info']['classifiers'])
                   ))
    # FIXME sort versions
    releases = resp['releases']
    _logger.always('%sVersions\t:%s\n%s\n' %
                   (
                       Color.GRAY,
                       Color.RESET,
                       "\n".join(["%-20s\t%s" % (k, releases[k][-1]['upload_time'])
                                  for k in reversed(sorted(releases.keys()))])
                   ))


def _create_spip_json(application_info):
    _logger.default('Creating spip.json on `%s`.' % _spip_path)
    with open(_spip_path, 'w') as f:
        f.write(json.dumps(application_info,
                           indent=2,
                           ensure_ascii=False,
                           sort_keys=True))
    _logger.default('Creating spip.json is completes.')


def _get_packages_from_spip(only_prod=False):
    packages = {}
    with open(_spip_path) as f:
        project = json.loads(f.read())

    if 'devDependencies' in project:
        packages.update(project['devDependencies'])
    if 'dependencies' in project:
        packages.update(project['dependencies'])

    return packages


def _preprocess_deps(dependencies):
    deps = {}
    for pack, _deps in dependencies.items():
        deps[pack] = {}
        for dep in _deps:
            if '@' in dep:
                name, version = dep.split('@')
            else:
                name, version = dep, None

            if name:
                deps[pack][name.lower()] = version
    return deps


def _create_tree(package, version, dependencies):
    tree = {
        'n': package,
        'v': version,
        'r': []
    }

    if package.lower() in dependencies:
        for k, v in dependencies[package.lower()].items():
            tree['r'].append(_create_tree(k, v, dependencies))

    return tree


def _print_tree(depth, last, tree):
    for idx in range(len(tree)):
        item = tree[idx]
        li = idx + 1 < len(tree)

        prefix = ''.join(['│   ' if last[i] else '    ' for i in range(depth)])

        print('%s%s── %s %s' % (
            prefix,
            '├' if li else '└',
            item['n'],
            '(%s)' % item['v'] if item['v'] else ''
        ))

        last2 = last.copy()
        last2.append(li)
        _print_tree(depth + 1, last2, item['r'])


def _print_deps(packages, dependencies):
    tree = []
    deps = _preprocess_deps(dependencies)

    for k, v in packages.items():
        tree.append(_create_tree(k, v, deps))

    print('\nspip.json')
    _print_tree(0, [], tree)


def _get_deps_children(package, deps):
    children = []
    if package.lower() in deps:
        for k, _ in deps[package.lower()].items():
            children.append(k)
            children.extend(_get_deps_children(k, deps))

    return children


def _get_2d_deps(packages, dependencies):
    result = {}
    deps = _preprocess_deps(dependencies)

    for k, _ in packages.items():
        result[k] = _get_deps_children(k, deps)

    return result


def _get_reversed_deps(deps):
    result = {}

    for k, v in deps.items():
        for item in v:
            if item not in result:
                result[item] = set()

            result[item].add(k)

    return {k: list(v) for k, v in result.items()}


def _get_removable_packages(packages):
    packages = [x.lower() for x in packages]

    installed_packages = _get_packages_from_spip()
    dependencies = {k.lower(): v for k, v in _get_dependencies().items()}

    deps = _get_2d_deps(installed_packages, dependencies)
    reversed_deps = _get_reversed_deps(deps)

    dest = set()
    for package in packages:
        if package not in deps:
            _logger.error(
                "Don't remove packages that is not specified in `spip.json`.")
            _logger.error("Removing %s will be skipped" % package)
            continue

        dest.add(package)
        dest.update(deps[package])

    for package in dest.copy():
        if package not in reversed_deps:
            continue

        if package in installed_packages and \
                package not in packages:
            # if package is in spip.json and user doesnot try to remove it, dont remove.
            dest.remove(package)

        for item in reversed_deps[package]:
            if item not in packages:
                dest.remove(package)
                break

    return list(dest)


def main(params=sys.argv[1:]):
    """Cli main"""
    # FIXME: commands should return the exit code
    args = parser.parse_args(params)

    # set verbose of logger
    _set_logger_verbosity(args)

    if args.version:
        # print version
        _print_version()
        return

    if args.which is None:
        # install all packages in spip.json
        if not _check_virtualenv_exists():
            return

        _logger.default("install all packages in `spip.json`")
        _activate_venv()

        _install(['%s==%s' % (k, v)
                  for k, v in _get_packages_from_spip().items()])

    elif args.which == 'init':
        # initialize the application
        if os.path.exists(_venv_home):
            _logger.error('`%s` already exists.' % _venv_home)
            return

        if os.path.exists(_spip_path):
            _logger.error('`%s` already exists.' % _spip_path)
            return

        application_info = _get_application_info()
        if not application_info:
            return

        _create_spip_json(application_info)
        _create_virtualenv()

    elif args.which == 'add':
        # install all packages in spip.json
        if not _check_virtualenv_exists():
            return

        _activate_venv()
        _install(args.packages, upgrade=args.upgrade)
        _add_packages_into_spip(args.packages)

    elif args.which == 'info':
        # fetch information from PyPi
        try:
            fetch_info_from_pypi(args.package)
        except Exception as e:
            _logger.debug(e)
            _logger.error("Cannot parse `https://pypi.python.org/pypi/%s/json`. " % args.package +
                          "Does the package `%s` exist?" % args.package)

    elif args.which == 'remove':
        packages = _get_removable_packages(args.packages)
        _remove(packages)

        _remove_packages_from_spip(args.packages)

    elif args.which == 'deps':
        _logger.default("show dependencies of installed packages")
        packages = _get_packages_from_spip()
        dependencies = {k.lower(): v for k, v in _get_dependencies().items()}
        _print_deps(packages, dependencies)

    elif args.which == 'freeze':
        if not _check_virtualenv_exists():
            return

        print("\n".join(_get_installed_packages()))
