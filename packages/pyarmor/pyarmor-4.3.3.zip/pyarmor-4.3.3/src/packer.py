#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#############################################################
#                                                           #
#      Copyright @ 2018 -  Dashingsoft corp.                #
#      All rights reserved.                                 #
#                                                           #
#      pyarmor                                              #
#                                                           #
#      Version: 4.3.2 -                                     #
#                                                           #
#############################################################
#
#
#  @File: packer.py
#
#  @Author: Jondy Zhao(jondy.zhao@gmail.com)
#
#  @Create Date: 2018/11/08
#
#  @Description:
#
#   Pack obfuscated Python scripts with any of third party
#   tools: py2exe, py2app, cx_Freeze, PyInstaller
#

'''Usage: python packer.py
    --type py2exe|py2app|freeze|installer
    --path

    /path/to/src/hello.py
'''

import logging
import os
import shutil
import subprocess
import sys
import time

from compileall import compile_dir
from py_compile import compile_file

try:
    import argparse
except ImportError:
    # argparse is new in version 2.7
    import polyfills.argparse as argparse

try:
    from pyarmor import main as _pyarmor
except ImportError:
    from pyarmor.pyarmor import main as _pyarmor

def armorcommand(func):
    return func
    # def wrap(*args, **kwargs):
    #     try:
    #         return func(*args, **kwargs)
    #     except Exception as e:
    #         logging.exception(e)
    # wrap.__doc__ = func.__doc__
    # return wrap

@armorcommand
def _init(args):
    '''Create an empty project or reinitialize an existing one

This command creates an empty project in the specified path -
basically a configure file .pyarmor_config, a project capsule
.pyarmor_capsule.zip, and a shell script "pyarmor" will be created (in
windows, it called "pyarmor.bat").

Option --src specifies where to find python source files. By default,
all .py files in this directory will be included in this project.

Option --entry specifies main script, which could be run directly
after obfuscated.

Option --capsule specifies project capsule file which has been
created. If it is set, no new project capsule is generated, just link
to this capsule.

EXAMPLES

    python pyarmor.py init --src=examples --entry=queens.py project1
    cd project1/
    ./pyarmor info

    '''
    if args.clone:
        logging.info('Warning: option --clone is deprecated, use --capsule instead ')
        _clone(args)
        return

    path = args.project
    logging.info('Create project in %s ...', path)

    if not os.path.exists(path):
        logging.info('Make project directory %s', path)
        os.makedirs(path)

    src = os.path.abspath(args.src)
    logging.info('Python scripts base path: %s', src)

    name = os.path.basename(os.path.abspath(path))
    if (args.type == 'package') or (args.type == 'pkg') or \
       (args.type == 'auto' and os.path.exists(os.path.join(src, '__init__.py'))):
        logging.info('Project is configured as package')
        project = Project(name=name, title=name, src=src, entry=args.entry,
                          is_package=1, obf_code_mode='wrap',
                          disable_restrict_mode=1)
    else:
        logging.info('Project is configured as standalone application.')
        project = Project(name=name, title=name, src=src, entry=args.entry)

    if args.capsule:
        capsule = os.path.abspath(args.capsule)
        logging.info('Share capsule with %s', capsule)
        project._update(dict(capsule=capsule))
    else:
        logging.info('Create project capsule ...')
        filename = os.path.join(path, capsule_filename)
        make_capsule(filename)
        logging.info('Project capsule %s created', filename)

    logging.info('Create configure file ...')
    filename = os.path.join(path, config_filename)
    project.save(path)
    logging.info('Configure file %s created', filename)

    logging.info('Create pyarmor command ...')
    script = make_command(plat_name, sys.executable, sys.argv[0], path)
    logging.info('Pyarmor command %s created', script)

    logging.info('Project init successfully.')

def _clone(args):
    path = args.project
    logging.info('Create project in %s ...', path)

    if not os.path.exists(path):
        logging.info('Make project directory %s', path)
        os.makedirs(path)

    src = os.path.abspath(args.src)
    logging.info('Python scripts base path: %s', src)

    logging.info('Clone project from path: %s', args.clone)
    for s in (config_filename, capsule_filename):
        logging.info('\tCopy file "%s"', s)
        shutil.copy(os.path.join(args.clone, s), os.path.join(path, s))

    logging.info('Init project settings')
    project = Project()
    project.open(path)
    name = os.path.basename(os.path.abspath(path))
    project._update(dict(name=name, title=name, src=src, entry=args.entry))
    project.save(path)

    if args.type != 'auto':
        logging.info('Option --type is ignored when --clone is specified')

    logging.info('Create pyarmor command ...')
    script = make_command(plat_name, sys.executable, sys.argv[0], path)
    logging.info('Pyarmor command %s created', script)

    logging.info('Project init successfully.')

@armorcommand
def _update(args):
    '''Update project settings.

Option --manifest is comma-separated list of manifest template
command, same as MANIFEST.in of Python Distutils. The default value is
"global-include *.py"

Option --entry is comma-separated list of entry scripts, relative to
src path of project.

Option --runtime-path is used to find _pytransform.dll(.so) in target
machine when import obfuscated scripts. It's only used in special
case. For example, use py2exe to package obfuscated scripts. Or use
many odoo modules which are obfuscated separately. In this case, copy
pyarmor runtime file to an absolute path, set this option to same path
when obfuscate each odoo module.

Examples,

    cd projects/project1
    ./pyarmor config --entry "main.py, another/main.py"
                     --manifest "global-include *.py, exclude test*.py"
                     --obf-module-mode des
                     --obf-code-mode des
                     --runtime-path "/opt/odoo/pyarmor"

    '''
    project = Project()
    project.open(args.project)
    logging.info('Update project %s ...', args.project)

    if args.src is not None:
        args.src = os.path.abspath(args.src)
        logging.info('Change src to absolute path: %s', args.src)
    if args.capsule is not None:
        args.capsule = os.path.abspath(args.capsule)
        logging.info('Change capsule to absolute path: %s', args.capsule)
    keys = project._update(dict(args._get_kwargs()))
    logging.info('Changed attributes: %s', keys)

    project.save(args.project)
    logging.info('Update project OK.')

@armorcommand
def _info(args):
    '''Show project information'''
    project = Project()
    project.open(args.project)
    logging.info('Project %s information\n%s', args.project, project.info())

@armorcommand
def _build(args):
    '''Build project, obfuscate all scripts in the project.'''
    project = Project()
    project.open(args.project)
    logging.info('Build project %s ...', args.project)

    capsule = build_path(project.capsule, args.project)
    logging.info('Use capsule: %s', capsule)

    output = build_path(project.output, args.project) \
             if args.output is None else args.output
    logging.info('Output path is: %s', output)

    if not args.only_runtime:
        mode = project.get_obfuscate_mode()
        files = project.get_build_files(args.force)
        src = project.src
        soutput = os.path.join(output, os.path.basename(src)) \
                  if project.get('is_package') else output
        filepairs = [(os.path.join(src, x), os.path.join(soutput, x))
                     for x in files]

        logging.info('%s increment build',
                     'Disable' if args.force else 'Enable')
        logging.info('Search scripts from %s', src)
        logging.info('Obfuscate %d scripts with mode %s', len(files), mode)
        for x in files:
            logging.info('\t%s', x)
        logging.info('Save obfuscated scripts to %s', soutput)

        obfuscate_scripts(filepairs, mode, capsule, soutput)

        # for x in targets:
        #     output = os.path.join(project.output, x)
        #     pairs = [(os.path.join(src, x), os.path.join(output, x))
        #              for x in files]
        #     for src, dst in pairs:
        #         try:
        #             shutil.copy2(src, dst)
        #         except Exception:
        #             os.makedirs(os.path.dirname(dst))
        #             shutil.copy2(src, dst)
        project['build_time'] = time.time()
        project.save(args.project)

        if project.entry:
            make_entry(project.entry, project.src, output,
                       rpath=project.runtime_path,
                       ispackage=project.get('is_package'))

    if not args.no_runtime:
        routput = os.path.join(output, os.path.basename(project.src)) \
            if project.get('is_package') else output
        if not os.path.exists(routput):
            logging.info('Make path: %s', routput)
            os.mkdir(routput)
        logging.info('Make runtime files to %s', routput)
        make_runtime(capsule, routput)
        if project.get('disable_restrict_mode'):
            licode = '*FLAGS:%c*CODE:Pyarmor-Project' % chr(1)
            licfile = os.path.join(routput, license_filename)
            logging.info('Generate no restrict mode license file: %s', licfile)
            make_project_license(capsule, licode, licfile)

    else:
        logging.info('\tIn order to import obfuscated scripts, insert ')
        logging.info('\t2 lines in entry script:')
        logging.info('\t\tfrom pytransfrom import pyarmor_runtime')
        logging.info('\t\tpyarmor_runtime()')

    logging.info('Build project OK.')

@armorcommand
def _licenses(args):
    '''Generate licenses for this project.

In order to bind licenses to fixed machine, use command hdinfo to get
all available hardware information:

    python pyarmor.py hdinfo

Examples,

* Expired license

    python pyarmor.py licenses --project=projects/myproject \\
                               --expired=2018-05-12 Customer-Jordan

* Bind license to fixed harddisk and expired someday

    cd projects/myproject
    ./pyarmor licenses -e 2018-05-12 \\
                       --bind-disk '100304PBN2081SF3NJ5T' Customer-Tom

* Batch expired licenses for many customers

    cd projects/myproject
    ./pyarmor licenses -e 2018-05-12 Customer-A Customer-B Customer-C

    '''
    if os.path.exists(os.path.join(args.project, config_filename)):
        logging.info('Generate licenses for project %s ...', args.project)
        project = Project()
        project.open(args.project)
        capsule = build_path(project.capsule, args.project) \
            if args.capsule is None else args.capsule
    else:
        if args.project != '':
            logging.warning('Ignore option --project, no project in %s',
                            args.project)
        capsule = capsule_filename if args.capsule is None else args.capsule
        logging.info('Generate licenses for capsule %s ...', capsule)
        project = {}

    licpath = os.path.join(
        args.project if args.output is None else args.output,
        'licenses')
    if os.path.exists(licpath):
        logging.info('Output path of licenses: %s', licpath)
    else:
        logging.info('Make output path of licenses: %s', licpath)
        os.mkdir(licpath)

    if args.expired is None:
        fmt = ''
    else:
        fmt = '*TIME:%.0f\n' % \
              time.mktime(time.strptime(args.expired, '%Y-%m-%d'))

    if (args.disable_restrict_mode is None
        and project.get('disable_restrict_mode')) \
       or args.disable_restrict_mode == 1:
        logging.info('The license files generated is in disable restrict mode')
        fmt = '%s*FLAGS:%c' % (fmt, 1)
    else:
        logging.info('The license files generated is in restrict mode')

    if args.bind_disk:
        fmt = '%s*HARDDISK:%s' % (fmt, args.bind_disk)

    if args.bind_mac:
        fmt = '%s*IFMAC:%s' % (fmt, args.bind_mac)

    if args.bind_ipv4:
        fmt = '%s*IFIPV4:%s' % (fmt, args.bind_ipv4)

    # if args.bind_ipv6:
    #     fmt = '%s*IFIPV6:%s' % (fmt, args.bind_ipv6)

    if args.bind_domain:
        fmt = '%s*DOMAIN:%s' % (fmt, args.bind_domain)

    if args.bind_file:
        bind_file, bind_key = args.bind_file.split(';', 2)
        if os.path.exists(bind_file):
            f = open(bind_file, 'rb')
            s = f.read()
            f.close()
            if sys.version_info[0] == 3:
                fmt = '%s*FIXKEY:%s;%s' % (fmt, bind_key, s.decode())
            else:
                fmt = '%s*FIXKEY:%s;%s' % (fmt, bind_key, s)
        else:
            raise RuntimeError('Bind file %s not found' % bindfile)

    # Prefix of registration code
    fmt = fmt + '*CODE:'

    for rcode in args.codes:
        output = os.path.join(licpath, rcode)
        if not os.path.exists(output):
            logging.info('Make path: %s', output)
            os.mkdir(output)

        licfile = os.path.join(output, license_filename)
        licode = fmt + rcode
        txtinfo = licode.replace('\n', r'\n')
        if args.expired:
            txtinfo = '"Expired:%s%s"' % (args.expired,
                                          txtinfo[txtinfo.find(r'\n')+2:])
        logging.info('Generate license: %s', txtinfo)
        make_project_license(capsule, licode, licfile)
        logging.info('Write license file: %s', licfile)

        logging.info('Write information to %s.txt', licfile)
        with open(os.path.join(licfile + '.txt'), 'w') as f:
            f.write(txtinfo)

    logging.info('Generate %d licenses OK.', len(args.codes))

@armorcommand
def _target(args):
    project = Project()
    project.open(args.project)

    name = args.name[0]
    if args.remove:
        logging.info('Remove target from project %s ...', args.project)
        project.remove_target(name)
    else:
        logging.info('Add target to project %s ...', args.project)
        project.add_target(name, args.platform, args.license)
    project.save(args.project)

@armorcommand
def _capsule(args):
    '''Make project capsule used to obfuscate scripts'''
    capsule = os.path.join(args.path, capsule_filename)
    logging.info('Generating capsule %s ...', capsule)
    if os.path.exists(capsule):
        logging.info('Do nothing, capsule %s has been exists', capsule)
    else:
        make_capsule(capsule)

@armorcommand
def _obfuscate(args):
    '''Obfuscate scripts without project'''
    path = args.src
    logging.info('Obfuscate scripts in path "%s" ...', path)

    capsule = args.capsule if args.capsule else capsule_filename
    if os.path.exists(capsule):
        logging.info('Use cached capsule %s', capsule)
    else:
        logging.info('Generate capsule %s', capsule)
        make_capsule(capsule)

    output = args.output
    if args.recursive:
        pat = 'global-include *.py'.decode() if hasattr('', 'decode') \
            else 'global-include *.py'
        files = Project.build_manifest([pat], path)
    else:
        files = Project.build_globfiles(args.patterns, path)
    filepairs = [(os.path.join(path, x), os.path.join(output, x))
                 for x in files]
    if args.no_restrict:
        logging.info('Restrict mode is disabled')
        mode = Project.map_obfuscate_mode(default_obf_module_mode,
                                          'wrap')
    else:
        mode = Project.map_obfuscate_mode(default_obf_module_mode,
                                          default_obf_code_mode)

    logging.info('Obfuscate scripts with mode %s', mode)
    logging.info('Save obfuscated scripts to "%s"', output)
    for a, b in filepairs:
        logging.info('\t%s -> %s', a, b)
    obfuscate_scripts(filepairs, mode, capsule, output)

    logging.info('Make runtime files')
    make_runtime(capsule, output)
    if args.no_restrict:
        licode = '*FLAGS:%c*CODE:Pyarmor-Project' % chr(1)
        licfile = os.path.join(output, license_filename)
        logging.info('Generate no restrict mode license file: %s', licfile)
        make_project_license(capsule, licode, licfile)

    if args.entry:
        make_entry(args.entry, path, output)
    logging.info('Obfuscate %d scripts OK.', len(files))

@armorcommand
def _check(args):
    '''Check consistency of project'''
    project = Project()
    project.open(args.project)
    logging.info('Check project %s ...', args.project)
    project._check(args.project)
    logging.info('Check project OK.')

@armorcommand
def _benchmark(args):
    '''Run benchmark test in current machine'''
    logging.info('Start benchmark test ...')
    logging.info('Obfuscate module mode: %s', args.obf_module_mode)
    logging.info('Obfuscate bytecode mode: %s', args.obf_code_mode)

    logging.info('Benchmark bootstrap ...')
    mode = Project.map_obfuscate_mode(args.obf_module_mode,
                                      args.obf_code_mode)
    p = subprocess.Popen(
        [sys.executable, 'benchmark.py', 'bootstrap', str(mode)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    logging.info('Benchmark bootstrap OK.')

    logging.info('Run benchmark test ...')
    p = subprocess.Popen([sys.executable, 'benchmark.py'], cwd='.benchtest')
    p.wait()

    logging.info('Finish benchmark test.')

def update_library(zipfile, dist):
    for root, dirs, files in os.walk(dist):
        for s in files:
            pass

def _packer(args):

    pyarmor_path = os.path.dirname(__file__)
    os.chdir(pyarmor_path)

    src = os.path.dirname(args.entry) if args.path is None else args.path
    entry = os.path.basename(args.entry) if args.path is None \
        else os.path.relpath(args.entry, args.path)

    project = 'build-for-%s' % args.type
    pack_cmd = 'py2exe' if args.type == 'py2exe' else 'build'
    pack_dist = 'dist' if args.type == 'py2exe' else os.path.join('build', 'exe.platname')
    dist = os.path.join(src, pack_dist)

    options = 'init', '--type', 'app', '--src', src, '--entry', entry, project
    _pyarmor(options)

    filters = ('global-include *.py', 'prune build, prune dist',
               'exclude %s setup.py pytransform.py' % entry)
    options = ('config', '--runtime-path', '',  '--disable-restrict-mode', '1',
               '--manifest', ','.join(filters), project)
    _pyarmor(options)

    options = 'build', '--no-runtime', project
    _pyarmor(options)

    shutil.copy(os.path.join(pyarmor_path, 'pytransform.py'), src)
    shutil.copy(os.path.join(src, entry), '%s.bak' % entry)
    shutil.move(os.path.join(project, 'dist', entry), src)

    p = subprocess.Popen([sys.executable, 'setup.py', build_cmd], cwd=src)
    p.wait()
    shutil.copy('%s.bak' % entry, os.path.join(src, entry))

    update_library(zipfile, os.path.join(project, 'dist'))    

    options = 'build', '--only-runtime', '-O', 'runtimes', project
    _pyarmor(options)

    for s in os.listdir(os.path.join(project, 'runtimes')):
        if s == 'pytransform.py':
            continue
        shutil.copy(os.path.join(project, 'runtimes', s), dist)


def main(args):
    parser = argparse.ArgumentParser(
        prog='packer.py',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Pack obfuscated scripts',
        epilog=__doc__,
    )
    parser.add_argument('-v', '--version', action='version', version='v0.1')

    parser.add_argument('-t', '--type', default='py2exe',
                        choices=('py2exe', 'py2app', 'cx_Freeze', 'PyInstaller'))
    parser.add_argument('-p', '--path', help='Source path of Python scripts')
    parser.add_argument('-s', '--setup', default='setup.py', help='Setup script')
    parser.add_argument('entry', metavar='Entry-Script', nargs=1, help='Entry script')

    parser.set_defaults(func=_packer)

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)-8s %(message)s',
    )
    main(sys.argv[1:])
