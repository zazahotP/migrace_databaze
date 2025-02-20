#
# get-py-info.py: get various Python info (for building)
#
######################################################################
#
# Copyright (c) 2002-2006, 2008 CollabNet.  All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.  The terms
# are also available at http://subversion.tigris.org/license-1.html.
# If newer versions of this license are posted there, you may use a
# newer version instead, at your option.
#
######################################################################
#
# This should be loaded/run by the appropriate Python, rather than executed
# directly as a program. In other words, you should:
#
#    $ python2 get-py-info.py --includes
#

import sys
import os

def usage():
  print('USAGE: python %s WHAT' % sys.argv[0])
  print('  Returns information about how to build Python extensions.')
  print('  WHAT may be one of:')
  print("    --includes : return -I include flags")
  print("    --compile  : return a compile command")
  print("    --link     : return a link command")
  print("    --libs     : return just the library options for linking")
  print("    --site     : return the path to site-packages")
  sys.exit(1)

if len(sys.argv) != 2:
  usage()

try:
  from distutils import sysconfig
except ImportError:
  # No information available
  print("none")
  sys.exit(1)

if sys.argv[1] == '--includes':
  inc = sysconfig.get_python_inc()
  plat = sysconfig.get_python_inc(plat_specific=1)
  if inc == plat:
    print("-I" + inc)
  else:
    print("-I%s -I%s" % (inc, plat))
  sys.exit(0)

if sys.argv[1] == '--compile':
  cc, ccshared = sysconfig.get_config_vars('CC', 'CCSHARED')
  print("%s %s" % (cc, ccshared))
  sys.exit(0)

def add_option(options, name, value=None):
  """Add option to list of options"""
  options.append(name)
  if value is not None:
    options.append(value)

def add_option_if_missing(options, name, value=None):
  """Add option to list of options, if it is not already present"""
  if options.count(name) == 0 and options.count("-Wl,%s" % name) == 0:
    add_option(options, name, value)

def link_options():
  """Get list of Python linker options"""

  # Initialize config variables
  assert os.name == "posix"
  options = sysconfig.get_config_var('LDSHARED').split()
  fwdir = sysconfig.get_config_var('PYTHONFRAMEWORKDIR')

  if fwdir and fwdir != "no-framework":

    # Setup the framework prefix
    fwprefix = sysconfig.get_config_var('PYTHONFRAMEWORKPREFIX')
    if fwprefix != "/System/Library/Frameworks":
      add_option_if_missing(options, "-F%s" % fwprefix)

    # Load in the framework
    fw = sysconfig.get_config_var('PYTHONFRAMEWORK')
    add_option(options, "-framework", fw)

  elif sys.platform == 'darwin':

    # Load bundles from python
    python_exe = os.path.join(sysconfig.get_config_var("BINDIR"),
      sysconfig.get_config_var('PYTHON'))
    add_option_if_missing(options, "-bundle_loader", python_exe)

  elif sys.platform == 'cygwin' or sys.platform.startswith('openbsd'):

    # Add flags to build against the Python library (also necessary
    # for Darwin, but handled elsewhere).

    # Find the path to the library, and add a flag to include it as a
    # library search path.
    shared_libdir = sysconfig.get_config_var('LIBDIR')
    static_libdir = sysconfig.get_config_var('LIBPL')
    ldlibrary = sysconfig.get_config_var('LDLIBRARY')
    if os.path.exists(os.path.join(shared_libdir, ldlibrary)):
      if shared_libdir != '/usr/lib':
        add_option_if_missing(options, '-L%s' % shared_libdir)
    elif os.path.exists(os.path.join(static_libdir, ldlibrary)):
      add_option_if_missing(options, "-L%s" % static_libdir)

    # Add a flag to build against the library itself.
    python_version = sysconfig.get_config_var('VERSION')
    add_option_if_missing(options, "-lpython%s" % python_version)

  return options

def lib_options():
  """Get list of Python library options"""
  link_command = link_options()
  options = []

  # Extract library-related options from link command
  for i in range(len(link_command)):
    option = link_command[i]
    if (not option.startswith("-L:") and option.startswith("-L") or
        option.startswith("-Wl,") or option.startswith("-l") or
        option.startswith("-F") or option == "-bundle" or
        option == "-flat_namespace"):
      options.append(option)
    elif (option == "-undefined" or option == "-bundle_loader" or
          option == "-framework"):
      options.append(option)
      options.append(link_command[i+1])

  return options

if sys.argv[1] == '--link':
  print(" ".join(link_options()))
  sys.exit(0)

if sys.argv[1] == '--libs':
  print(" ".join(lib_options()))
  sys.exit(0)

if sys.argv[1] == '--site':
  print(sysconfig.get_python_lib())
  sys.exit(0)

usage()
