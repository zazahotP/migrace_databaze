#!/usr/bin/env python
#
#  stat_tests.py:  testing the svn stat command
#
#  Subversion is a tool for revision control.
#  See http://subversion.tigris.org for more information.
#
# ====================================================================
# Copyright (c) 2000-2009 CollabNet.  All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.  The terms
# are also available at http://subversion.tigris.org/license-1.html.
# If newer versions of this license are posted there, you may use a
# newer version instead, at your option.
#
######################################################################

# General modules
import os, re, time

# Our testing module
import svntest
from svntest import wc

# (abbreviation)
Skip = svntest.testcase.Skip
SkipUnless = svntest.testcase.SkipUnless
XFail = svntest.testcase.XFail
Item = svntest.wc.StateItem



######################################################################
# Tests
#
#   Each test must return on success or raise on failure.

#----------------------------------------------------------------------

def status_unversioned_file_in_current_dir(sbox):
  "status on unversioned file in current directory"

  sbox.build(read_only = True)
  wc_dir = sbox.wc_dir

  os.chdir(wc_dir)

  svntest.main.file_append('foo', 'a new file')

  svntest.actions.run_and_verify_svn(None, [ "?       foo\n" ], [],
                                     'stat', 'foo')

#----------------------------------------------------------------------
# Regression for issue #590

def status_update_with_nested_adds(sbox):
  "run 'status -u' when nested additions are pending"

  sbox.build()
  wc_dir = sbox.wc_dir

  # Make a backup copy of the working copy
  wc_backup = sbox.add_wc_path('backup')
  svntest.actions.duplicate_dir(wc_dir, wc_backup)

  # Create newdir and newfile
  newdir_path = os.path.join(wc_dir, 'newdir')
  newfile_path = os.path.join(wc_dir, 'newdir', 'newfile')
  os.makedirs(newdir_path)
  svntest.main.file_append(newfile_path, 'new text')

  # Schedule newdir and newfile for addition (note that the add is recursive)
  svntest.main.run_svn(None, 'add', newdir_path)

  # Created expected output tree for commit
  expected_output = svntest.wc.State(wc_dir, {
    'newdir' : Item(verb='Adding'),
    'newdir/newfile' : Item(verb='Adding'),
    })

  # Create expected status tree; all local revisions should be at 1,
  # but newdir and newfile should be at revision 2.
  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)
  expected_status.add({
    'newdir' : Item(status='  ', wc_rev=2),
    'newdir/newfile' : Item(status='  ', wc_rev=2),
    })

  # Commit.
  svntest.actions.run_and_verify_commit(wc_dir, expected_output,
                                        expected_status, None, wc_dir)

  # Now we go to the backup working copy, still at revision 1.
  # We will run 'svn st -u', and make sure that newdir/newfile is reported
  # as a nonexistent (but pending) path.
  expected_status = svntest.actions.get_virginal_state(wc_backup, 1)
  expected_status.add({
    'newdir'         : Item(status='  '),
    'newdir/newfile' : Item(status='  '),
    })
  svntest.actions.run_and_verify_unquiet_status(wc_backup,
                                                expected_status)

#----------------------------------------------------------------------

# svn status -vN should include all entries in a directory
def status_shows_all_in_current_dir(sbox):
  "status -vN shows all items in current directory"

  sbox.build(read_only = True)
  wc_dir = sbox.wc_dir

  os.chdir(wc_dir)
  exit_code, output, err = svntest.actions.run_and_verify_svn(None, None, [],
                                                              'stat', '-vN')

  if (len(output) != len(os.listdir("."))):
    raise svntest.Failure


#----------------------------------------------------------------------

def status_missing_file(sbox):
  "status with a versioned file missing"

  sbox.build(read_only = True)
  wc_dir = sbox.wc_dir

  os.chdir(wc_dir)

  os.remove('iota')

  exit_code, output, err = svntest.actions.run_and_verify_svn(None, None, [],
                                                              'status')
  for line in output:
    if not re.match("! +iota", line):
      raise svntest.Failure

  # This invocation is for issue #2127.
  exit_code, output, err = svntest.actions.run_and_verify_svn(None, None, [],
                                                              'status', '-u',
                                                              'iota')
  found_it = 0
  for line in output:
    if re.match("! +1 +iota", line):
      found_it = 1
  if not found_it:
    raise svntest.Failure

#----------------------------------------------------------------------

def status_type_change(sbox):
  "status on versioned items whose type has changed"

  sbox.build(read_only = True)
  wc_dir = sbox.wc_dir

  os.chdir(wc_dir)

  # First replace a versioned dir with a file and a versioned file
  # with a versioned dir.
  os.rename('iota', 'was_iota')
  os.rename('A', 'iota')
  os.rename('was_iota', 'A')

  exit_code, output, err = svntest.actions.run_and_verify_svn(None, None, [],
                                                              'status')
  if len(output) != 2:
    raise svntest.Failure
  for line in output:
    if not re.match("~ +(iota|A)", line):
      raise svntest.Failure

  # Now change the file that is obstructing the versioned dir into an
  # unversioned dir.
  os.remove('A')
  os.mkdir('A')

  exit_code, output, err = svntest.actions.run_and_verify_svn(None, None, [],
                                                              'status')
  if len(output) != 2:
    raise svntest.Failure
  for line in output:
    if not re.match("~ +(iota|A)", line):
      raise svntest.Failure

  # Now change the versioned dir that is obstructing the file into an
  # unversioned dir.
  svntest.main.safe_rmtree('iota')
  os.mkdir('iota')

  exit_code, output, err = svntest.actions.run_and_verify_svn(None, None, [],
                                                              'status')
  if len(output) != 2:
    raise svntest.Failure
  for line in output:
    if not re.match("~ +(iota|A)", line):
      raise svntest.Failure

#----------------------------------------------------------------------

def status_type_change_to_symlink(sbox):
  "status on versioned items replaced by symlinks"

  sbox.build(read_only = True)
  wc_dir = sbox.wc_dir

  os.chdir(wc_dir)

  # "broken" symlinks
  os.remove('iota')
  os.symlink('foo', 'iota')
  svntest.main.safe_rmtree('A/D')
  os.symlink('bar', 'A/D')

  exit_code, output, err = svntest.actions.run_and_verify_svn(None, None, [],
                                                              'status')
  if len(output) != 2:
    raise svntest.Failure
  for line in output:
    if not re.match("~ +(iota|A/D)", line):
      raise svntest.Failure

  # "valid" symlinks
  os.remove('iota')
  os.remove('A/D')
  os.symlink('A/mu', 'iota')
  os.symlink('C', 'A/D')

  exit_code, output, err = svntest.actions.run_and_verify_svn(None, None, [],
                                                              'status')
  if len(output) != 2:
    raise svntest.Failure
  for line in output:
    if not re.match("~ +(iota|A/D)", line):
      raise svntest.Failure

#----------------------------------------------------------------------
# Regression test for revision 3686.

def status_with_new_files_pending(sbox):
  "status -u with new files in the repository"

  sbox.build()
  wc_dir = sbox.wc_dir

  os.chdir(wc_dir)

  svntest.main.file_append('newfile', 'this is a new file')
  svntest.main.run_svn(None, 'add', 'newfile')
  svntest.main.run_svn(None,
                       'ci', '-m', 'logmsg')
  svntest.main.run_svn(None,
                       'up', '-r', '1')

  exit_code, output, err = svntest.actions.run_and_verify_svn(None, None, [],
                                                              'status', '-u')

  # The bug fixed in revision 3686 was a segmentation fault.
  # TODO: Check exit code.
  # In the meantime, no output means there was a problem.
  for line in output:
    if line.find('newfile') != -1:
      break
  else:
    raise svntest.Failure

#----------------------------------------------------------------------

def status_for_unignored_file(sbox):
  "status for unignored file and directory"

  sbox.build(read_only = True)
  wc_dir = sbox.wc_dir

  os.chdir(wc_dir)

  # use a temp file to set properties with wildcards in their values
  # otherwise Win32/VS2005 will expand them
  svntest.main.file_append('proptmp', 'new*')
  svntest.main.file_append('newfile', 'this is a new file')
  os.makedirs('newdir')
  svntest.main.run_svn(None, 'propset', 'svn:ignore', '-F', 'proptmp', '.')
  os.remove('proptmp')

  # status on the directory with --no-ignore
  expected = svntest.verify.UnorderedOutput(
        ['I       newdir\n',
         'I       newfile\n',
         ' M      .\n'])
  svntest.actions.run_and_verify_svn(None,
                                     expected,
                                     [],
                                     'status', '--no-ignore', '.')

  # status specifying the file explicitly on the command line
  expected = svntest.verify.UnorderedOutput(
        ['I       newdir\n',
         'I       newfile\n'])
  svntest.actions.run_and_verify_svn(None,
                                     expected,
                                     [],
                                     'status', 'newdir', 'newfile')

#----------------------------------------------------------------------

def status_for_nonexistent_file(sbox):
  "status on missing and unversioned file"

  sbox.build(read_only = True)

  wc_dir = sbox.wc_dir

  os.chdir(wc_dir)

  exit_code, output, err = svntest.actions.run_and_verify_svn(
    None, None, [], 'status', 'nonexistent-file')

  # there should *not* be a status line printed for the nonexistent file
  for line in output:
    if re.match(" +nonexistent-file", line):
      raise svntest.Failure

#----------------------------------------------------------------------

def status_nonrecursive_update_different_cwd(sbox):
  "status -v -N -u from different current directories"

  # check combination of status -u and -N
  # create A/C/J in repository
  # create A/C/K in working copy
  # check status output with -u and -N on target C
  # check status output with -u and -N on target . (in C)

  sbox.build()
  wc_dir = sbox.wc_dir

  J_url  = sbox.repo_url + '/A/C/J'
  K_path = os.path.join(wc_dir, 'A', 'C', 'K' )

  svntest.actions.run_and_verify_svn(None, None, [],
                                     'mkdir', '-m', 'rev 2', J_url)

  svntest.actions.run_and_verify_svn(None, None, [],
                                     'mkdir', K_path)

  os.chdir(wc_dir)

  expected_output = [
    '        *                                %s\n' % os.path.join("C", "J"),
    'A                0       ?   ?           %s\n' % os.path.join("C", "K"),
    '        *        1        1 jrandom      C\n',
    'Status against revision:      2\n' ]

  os.chdir('A')
  svntest.actions.run_and_verify_svn(None,
                                     expected_output,
                                     [],
                                     'status', '-v', '-N', '-u', 'C')

  expected_output = [
    '        *                                J\n',
    'A                0       ?   ?           K\n',
    '        *        1        1 jrandom      .\n',
    'Status against revision:      2\n']

  os.chdir('C')
  svntest.actions.run_and_verify_svn(None,
                                     expected_output,
                                     [],
                                     'status', '-v', '-N', '-u', '.')


#----------------------------------------------------------------------

def status_file_needs_update(sbox):
  "status -u indicates out-of-dateness"

  # See this thread:
  #
  #    http://subversion.tigris.org/servlets/ReadMsg?list=dev&msgNo=27975
  #
  # Basically, Andreas was seeing inconsistent results depending on
  # whether or not he accompanied 'svn status -u' with '-v':
  #
  #    % svn st -u
  #    Head revision:     67
  #    %
  #
  # ...and yet...
  #
  #    % svn st -u -v
  #                   56        6          k   cron-daily.pl
  #           *       56       44          k   crontab.root
  #                   56        6          k   gmls-lR.pl
  #    Head revision:     67
  #    %
  #
  # The first status should show the asterisk, too.  There was never
  # any issue for this bug, so this comment and the thread are your
  # audit trail :-).

  sbox.build()
  wc_dir = sbox.wc_dir

  other_wc = sbox.add_wc_path('other')

  svntest.actions.duplicate_dir(wc_dir, other_wc)

  was_cwd = os.getcwd()

  os.chdir(wc_dir)
  svntest.main.file_append('crontab.root', 'New file crontab.root.\n')
  svntest.main.run_svn(None, 'add', 'crontab.root')
  svntest.main.run_svn(None,
                       'ci', '-m', 'log msg')
  os.chdir(was_cwd)
  os.chdir(other_wc)
  svntest.main.run_svn(None,
                       'up')

  os.chdir(was_cwd)
  os.chdir(wc_dir)
  svntest.main.file_append('crontab.root', 'New line in crontab.root.\n')
  svntest.main.run_svn(None,
                       'ci', '-m', 'log msg')

  # The `svntest.actions.run_and_verify_*_status' routines all pass
  # the -v flag, which we don't want, as this bug never appeared when
  # -v was passed.  So we run status by hand:
  os.chdir(was_cwd)
  exit_code, out, err = svntest.actions.run_and_verify_svn(None, None, [],
                                                           'status', '-u',
                                                           other_wc)

  for line in out:
    if re.match("\\s+\\*.*crontab\\.root$", line):
      break
  else:
    raise svntest.Failure

#----------------------------------------------------------------------

def status_uninvited_parent_directory(sbox):
  "status -u on outdated, added file shows only that"

  # To reproduce, check out working copies wc1 and wc2, then do:
  #
  #   $ cd wc1
  #   $ echo "new file" >> newfile
  #   $ svn add newfile
  #   $ svn ci -m 'log msg'
  #
  #   $ cd ../wc2
  #   $ echo "new file" >> newfile
  #   $ svn add newfile
  #
  #   $ cd ..
  #   $ svn st wc2/newfile
  #
  # You *should* get one line of status output, for newfile.  The bug
  # is that you get two instead, one for newfile, and one for its
  # parent directory, wc2/.
  #
  # This bug was originally discovered during investigations into
  # issue #1042, "fixed" in revision 4181, then later the fix was
  # reverted because it caused other status problems (see the test
  # status_file_needs_update(), which fails when 4181 is present).

  sbox.build()
  wc_dir = sbox.wc_dir

  other_wc = sbox.add_wc_path('other')

  svntest.actions.duplicate_dir(wc_dir, other_wc)

  was_cwd = os.getcwd()

  os.chdir(wc_dir)
  svntest.main.file_append('newfile', 'New file.\n')
  svntest.main.run_svn(None, 'add', 'newfile')
  svntest.main.run_svn(None,
                       'ci', '-m', 'log msg')

  os.chdir(was_cwd)
  os.chdir(other_wc)
  svntest.main.file_append('newfile', 'New file.\n')
  svntest.main.run_svn(None, 'add', 'newfile')

  os.chdir(was_cwd)

  # We don't want a full status tree here, just one line (or two, if
  # the bug is present).  So run status by hand:
  os.chdir(was_cwd)
  exit_code, out, err = svntest.actions.run_and_verify_svn(
    None, None, [],
    'status', '-u', os.path.join(other_wc, 'newfile'))

  for line in out:
    # The "/?" is just to allow for an optional trailing slash.
    if re.match("\\s+\\*.*\.other/?$", line):
      raise svntest.Failure

def status_on_forward_deletion(sbox):
  "status -u on working copy deleted in HEAD"
  # See issue #1289.
  sbox.build(create_wc = False)
  wc_dir = sbox.wc_dir

  top_url = sbox.repo_url
  A_url = top_url + '/A'

  svntest.main.run_svn(None,
                       'rm', '-m', 'Remove A.', A_url)

  svntest.main.safe_rmtree(wc_dir)
  os.mkdir(wc_dir)

  os.chdir(wc_dir)

  svntest.main.run_svn(None,
                       'co', '-r1', top_url + "@1", 'wc')
  # If the bug is present, this will error with
  #
  #    subversion/libsvn_wc/lock.c:513: (apr_err=155005)
  #    svn: Working copy not locked
  #    svn: directory '' not locked
  #
  svntest.actions.run_and_verify_svn(None, None, [], 'st', '-u', 'wc')

  # Try again another way; the error would look like this:
  #
  #    subversion/libsvn_repos/delta.c:207: (apr_err=160005)
  #    svn: Invalid filesystem path syntax
  #    svn: svn_repos_dir_delta: invalid editor anchoring; at least \
  #       one of the input paths is not a directory and there was   \
  #       no source entry.
  #
  # (Dang!  Hope a user never has to see that :-) ).
  #
  svntest.main.safe_rmtree('wc')
  svntest.main.run_svn(None,
                       'co', '-r1', A_url + "@1", 'wc')
  svntest.actions.run_and_verify_svn(None, None, [], 'st', '-u', 'wc')

#----------------------------------------------------------------------

def get_last_changed_date(path):
  "get the Last Changed Date for path using svn info"
  exit_code, out, err = svntest.actions.run_and_verify_svn(None, None, [],
                                                           'info', path)
  for line in out:
    if re.match("^Last Changed Date", line):
      return line
  print("Didn't find Last Changed Date for " + path)
  raise svntest.Failure

# Helper for timestamp_behaviour test
def get_text_timestamp(path):
  "get the text-time for path using svn info"
  exit_code, out, err = svntest.actions.run_and_verify_svn(None, None, [],
                                                           'info', path)
  for line in out:
    if re.match("^Text Last Updated", line):
      return line
  print("Didn't find text-time for " + path)
  raise svntest.Failure

# Helper for timestamp_behaviour test
def text_time_behaviour(wc_dir, wc_path, status_path, expected_status, cmd):
  "text-time behaviour"

  # Pristine text and text-time
  fp = open(wc_path, 'rb')
  pre_text = fp.readlines()
  pre_text_time = get_text_timestamp(wc_path)

  # Modifying the text does not affect text-time
  svntest.main.file_append(wc_path, "some mod")
  expected_status.tweak(status_path, status='M ')
  svntest.actions.run_and_verify_status(wc_dir, expected_status)
  text_time = get_text_timestamp(wc_path)
  if text_time != pre_text_time:
    raise svntest.Failure

  # Manually reverting the text does not affect the text-time
  fp = open(wc_path, 'wb')
  fp.writelines(pre_text)
  fp.close()
  expected_status.tweak(status_path, status='  ')
  svntest.actions.run_and_verify_status(wc_dir, expected_status)
  text_time = get_text_timestamp(wc_path)
  if text_time != pre_text_time:
    raise svntest.Failure

  # revert/cleanup change the text-time even though the text doesn't change
  if cmd == 'cleanup':
    svntest.actions.run_and_verify_svn(None, None, [], cmd, wc_dir)
  else:
    svntest.actions.run_and_verify_svn(None, None, [], cmd, wc_path)
  svntest.actions.run_and_verify_status(wc_dir, expected_status)
  text_time = get_text_timestamp(wc_path)
  if text_time == pre_text_time:
    raise svntest.Failure


# Is this really a status test?  I'm not sure, but I don't know where
# else to put it.
def timestamp_behaviour(sbox):
  "timestamp behaviour"

  sbox.build()
  wc_dir = sbox.wc_dir

  A_path = os.path.join(wc_dir, 'A')
  iota_path = os.path.join(wc_dir, 'iota')

  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)
  svntest.actions.run_and_verify_status(wc_dir, expected_status)

  # Sleep to ensure timestamps change
  time.sleep(2)

  # Check behaviour of revert on text-time
  text_time_behaviour(wc_dir, iota_path, 'iota', expected_status, 'revert')

  # Sleep to ensure timestamps change
  time.sleep(2)

  # Check behaviour of cleanup on text-time
  text_time_behaviour(wc_dir, iota_path, 'iota', expected_status, 'cleanup')

  # Create a config to enable use-commit-times
  config_dir = os.path.join(os.path.abspath(svntest.main.temp_dir),
                            'use_commit_config')
  config_contents = '''\
[miscellany]
use-commit-times = yes
'''
  svntest.main.create_config_dir(config_dir, config_contents)

  other_wc = sbox.add_wc_path('other')
  svntest.actions.run_and_verify_svn("checkout failed", None, [],
                                     'co', sbox.repo_url,
                                     other_wc,
                                     '--config-dir', config_dir)

  other_iota_path = os.path.join(other_wc, 'iota')
  iota_text_timestamp = get_text_timestamp(other_iota_path)
  iota_last_changed = get_last_changed_date(other_iota_path)
  if (iota_text_timestamp[17] != ':' or
      iota_text_timestamp[17:] != iota_last_changed[17:]):
    raise svntest.Failure

  ### FIXME: check the working file's timestamp as well

#----------------------------------------------------------------------

def status_on_unversioned_dotdot(sbox):
  "status on '..' where '..' is not versioned"
  # See issue #1617 (and #2030).
  sbox.build(read_only = True)
  wc_dir = sbox.wc_dir

  new_dir = os.path.join(wc_dir, 'new_dir')
  new_subdir = os.path.join(new_dir, 'new_subdir')
  os.mkdir(new_dir)
  os.mkdir(new_subdir)

  os.chdir(new_subdir)

  exit_code, out, err = svntest.main.run_svn(1, 'st', '..')
  for line in err:
    if line.find('svn: warning: \'..\' is not a working copy') != -1:
      break
  else:
    raise svntest.Failure

#----------------------------------------------------------------------

def status_on_partially_nonrecursive_wc(sbox):
  "status -u in partially non-recursive wc"
  # Based on issue #2122.
  #
  #    $ svn co -N -r 213 svn://svn.debian.org/pkg-kde .
  #    A  README
  #    Checked out revision 213.
  #
  #    $ svn up -r 213 scripts www
  #    [ List of scripts/* files.]
  #    Updated to revision 213.
  #    [ List of www/* files.]
  #    Updated to revision 213.
  #
  #    $ svn st -u
  #       *      213   www/IGNORE-ME
  #       *      213   www
  #    svn: subversion/libsvn_wc/status.c:910: tweak_statushash:         \
  #         Assertion `repos_text_status == svn_wc_status_added' failed. \
  #         Aborted (core dumped)
  #
  # You might think that the intermediate "svn up -r 213 scripts www"
  # step is unnecessary, but when I tried eliminating it, I got
  #
  #    $ svn st -u
  #    subversion/libsvn_wc/lock.c:642: (apr_err=155005)
  #    svn: Working copy 'www' not locked
  #    $
  #
  # instead of the assertion error.

  sbox.build()
  wc_dir = sbox.wc_dir

  top_url = sbox.repo_url
  A_url = top_url + '/A'
  D_url = top_url + '/A/D'
  G_url = top_url + '/A/D/G'
  H_url = top_url + '/A/D/H'
  rho = os.path.join(wc_dir, 'A', 'D', 'G', 'rho')

  # Commit a change to A/D/G/rho.  This will be our equivalent of
  # whatever change it was that happened between r213 and HEAD in the
  # reproduction recipe.  For us, it's r2.
  svntest.main.file_append(rho, 'Whan that Aprille with his shoores soote\n')
  svntest.main.run_svn(None,
                       'ci', '-m', 'log msg', rho)

  # Make the working copy weird in the right way, then try status -u.
  D_wc = sbox.add_wc_path('D')
  svntest.main.run_svn(None,
                       'co', '-r1', '-N', D_url, D_wc)

  os.chdir(D_wc)
  svntest.main.run_svn(None,
                       'up', '-r1', 'H')
  svntest.main.run_svn(None,
                       'st', '-u')


def missing_dir_in_anchor(sbox):
  "a missing dir in the anchor"

  sbox.build(read_only = True)
  wc_dir = sbox.wc_dir

  foo_path = os.path.join(wc_dir, 'foo')
  svntest.actions.run_and_verify_svn(None, None, [], 'mkdir', foo_path)
  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)
  expected_status.add({
    'foo' : Item(status='A ', wc_rev=0),
    })
  svntest.actions.run_and_verify_status(wc_dir, expected_status)

  # At one point this caused a "foo not locked" error
  svntest.main.safe_rmtree(foo_path)
  expected_status.tweak('foo', status='! ', wc_rev='?')
  svntest.actions.run_and_verify_status(wc_dir, expected_status)


def status_in_xml(sbox):
  "status output in XML format"

  sbox.build(read_only = True)
  wc_dir = sbox.wc_dir

  file_name = "iota"
  file_path = os.path.join(wc_dir, file_name)
  svntest.main.file_append(file_path, "test status --xml\n")

  # Retrieve last changed date from svn log
  exit_code, output, error = svntest.actions.run_and_verify_svn(
    None, None, [], 'log', file_path, '--xml', '-rHEAD')

  info_msg = "<date>"
  for line in output:
    if line.find(info_msg) >= 0:
      time_str = line[:len(line)]
      break
  else:
    raise svntest.Failure

  template = ["<?xml version=\"1.0\"?>\n",
              "<status>\n",
              "<target\n",
              "   path=\"%s\">\n" % (file_path),
              "<entry\n",
              "   path=\"%s\">\n" % (file_path),
              "<wc-status\n",
              "   props=\"none\"\n",
              "   item=\"modified\"\n",
              "   revision=\"1\">\n",
              "<commit\n",
              "   revision=\"1\">\n",
              "<author>%s</author>\n" % svntest.main.wc_author,
              time_str,
              "</commit>\n",
              "</wc-status>\n",
              "</entry>\n",
              "<against\n",
              "   revision=\"1\"/>\n",
              "</target>\n",
              "</status>\n",
             ]

  exit_code, output, error = svntest.actions.run_and_verify_svn(None, None, [],
                                                                'status',
                                                                file_path,
                                                                '--xml', '-u')

  for i in range(0, len(output)):
    if output[i] != template[i]:
      print("ERROR: expected: %s actual: %s" % (template[i], output[i]))
      raise svntest.Failure

#----------------------------------------------------------------------

def status_ignored_dir(sbox):
  "status on ignored directory"
  sbox.build()
  wc_dir = sbox.wc_dir
  new_dir = os.path.join(wc_dir, "dir.o")
  new_dir_url = sbox.repo_url + "/dir.o"

  svntest.actions.run_and_verify_svn("Create dir", "\n|Committed revision 2.", [],
                                     'mkdir', new_dir_url, '-m', 'msg')

  # Make a dir that is ignored by the default ignore patterns.
  os.mkdir(new_dir)

  # run_and_verify_status doesn't handle this weird kind of entry.
  svntest.actions.run_and_verify_svn(None,
                                     ['I       *            ' + new_dir + "\n",
                                      '        *        1   ' + wc_dir + "\n",
                                      'Status against revision:      2\n'], [],
                                     "status", "-u", wc_dir)

#----------------------------------------------------------------------

def status_unversioned_dir(sbox):
  "status on unversioned dir (issue 2030)"
  sbox.build(read_only = True)
  dir = sbox.repo_dir
  expected_err = ["svn: warning: '" + dir + "' is not a working copy\n",
                  "svn: warning: '" + dir + "' is not a working copy\n"]
  svntest.actions.run_and_verify_svn2(None, [], expected_err, 0,
                                      "status", dir, dir)

#----------------------------------------------------------------------

def status_missing_dir(sbox):
  "status with a versioned directory missing"
  sbox.build(read_only = True)
  wc_dir = sbox.wc_dir
  a_d_g = os.path.join(wc_dir, "A", "D", "G")

  # ok, blow away the A/D/G directory
  svntest.main.safe_rmtree(a_d_g)

  expected = svntest.verify.UnorderedOutput(["!       " + a_d_g + "\n"])
  svntest.actions.run_and_verify_svn(None, expected, [], "status", wc_dir)

  expected = svntest.verify.UnorderedOutput(
         ["        *            " + os.path.join(a_d_g, "pi") + "\n",
          "        *            " + os.path.join(a_d_g, "rho") + "\n",
          "        *            " + os.path.join(a_d_g, "tau") + "\n",
          "!       *       ?    " + a_d_g + "\n",
          "        *        1   " + os.path.join(wc_dir, "A", "D") + "\n",
          "Status against revision:      1\n" ])

  # now run status -u, we should be able to do this without crashing
  svntest.actions.run_and_verify_svn(None, expected, [],
                                     "status", "-u", wc_dir)

def status_add_plus_conflict(sbox):
  "status on conflicted added file"
  sbox.build()
  svntest.actions.do_sleep_for_timestamps()

  wc_dir = sbox.wc_dir

  branch_url  = sbox.repo_url + '/branch'
  trunk_url  = sbox.repo_url + '/trunk'

  svntest.actions.run_and_verify_svn(None, None, [],
                                     'mkdir', '-m', 'rev 2',
                                     branch_url, trunk_url)

  svntest.actions.run_and_verify_svn(None, None, [],
                                     'update', wc_dir)

  branch_file = os.path.join(wc_dir, 'branch', 'file')

  svntest.main.file_write(branch_file, "line 1\nline2\nline3\n", 'wb+')

  svntest.actions.run_and_verify_svn(None, None, [], 'add', branch_file)

  svntest.actions.run_and_verify_svn(None, None, [],
                                     'commit',
                                     branch_file, '-m', 'rev 3')

  svntest.main.file_write(branch_file, "line 1\nline3\n", 'wb')

  svntest.actions.run_and_verify_svn(None, None, [],
                                     'commit',
                                     branch_file, '-m', 'rev 4')

  svntest.main.file_write(branch_file, "line 1\nline2\n", 'wb')

  svntest.actions.run_and_verify_svn(None, None, [],
                                     'commit',
                                     branch_file, '-m', 'rev 5')

  trunk_dir = os.path.join(wc_dir, 'trunk')

  svntest.actions.run_and_verify_svn(None, None, [],
                                     'merge',
                                     branch_url, '-r', '2:3', trunk_dir)

  svntest.actions.run_and_verify_svn(None, None, [],
                                     'merge',
                                     branch_url, '-r', '4:5', trunk_dir)

  lines = [
    "?       " + os.path.join(wc_dir, "trunk", "file.merge-left.r4") + "\n",
    "?       " + os.path.join(wc_dir, "trunk", "file.merge-right.r5") + "\n",
    "?       " + os.path.join(wc_dir, "trunk", "file.working") + "\n",
    "C  +    " + os.path.join(wc_dir, "trunk", "file") + "\n",
  ]
  if svntest.main.server_has_mergeinfo():
    lines.append(" M      " + os.path.join(wc_dir, "trunk") + "\n")

  expected_output = svntest.verify.UnorderedOutput(lines)

  svntest.actions.run_and_verify_svn(None, expected_output, [],
                                     'status', wc_dir)

#----------------------------------------------------------------------

def inconsistent_eol(sbox):
  "status with inconsistent eol style"

  sbox.build()
  wc_dir = sbox.wc_dir
  iota_path = os.path.join(wc_dir, "iota")

  svntest.main.file_write(iota_path, "line 1\nline 2\n", "wb")

  svntest.actions.run_and_verify_svn(None,
                                     "property 'svn:eol-style' set on.*iota",
                                     [],
                                     'propset', 'svn:eol-style', 'native',
                                     os.path.join(wc_dir, 'iota'))

  expected_output = svntest.wc.State(wc_dir, {
    'iota' : Item(verb='Sending'),
    })

  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)
  expected_status.tweak('iota', wc_rev=2)

  svntest.actions.run_and_verify_commit(wc_dir, expected_output,
                                        expected_status, None, wc_dir)

  # Make the eol style inconsistent and verify that status says nothing.
  svntest.main.file_write(iota_path, "line 1\nline 2\r\n", "wb")
  svntest.actions.run_and_verify_status(wc_dir, expected_status)

#----------------------------------------------------------------------
# Test for issue #2533
def status_update_with_incoming_props(sbox):
  "run 'status -u' variations w/ incoming propchanges"

  sbox.build()
  wc_dir = sbox.wc_dir
  A_path = os.path.join(wc_dir, 'A')

  # Add a property to the root folder and a subdir
  svntest.main.run_svn(None, 'propset', 'red', 'rojo', wc_dir)
  svntest.main.run_svn(None, 'propset', 'black', 'bobo', A_path)

  # Create expected output tree.
  expected_output = svntest.wc.State(wc_dir, {
    ''  : Item(verb='Sending'),
    'A' : Item(verb='Sending'),
    })

  # Created expected status tree.
  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)
  expected_status.tweak('', wc_rev=2, status='  ')
  expected_status.tweak('A', wc_rev=2, status='  ')

  # Commit the working copy
  svntest.actions.run_and_verify_commit(wc_dir, expected_output,
                                        expected_status,
                                        None, wc_dir)

  # Create expected trees for an update to revision 1.
  expected_output = svntest.wc.State(wc_dir, {
    ''  : Item(status=' U'),
    'A' : Item(status=' U'),
    })
  expected_disk = svntest.main.greek_state.copy()
  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)

  # Do the update and check the results in three ways... INCLUDING PROPS
  svntest.actions.run_and_verify_update(wc_dir,
                                        expected_output,
                                        expected_disk,
                                        expected_status,
                                        None, None, None, None, None, 1,
                                        '-r', '1', wc_dir)

  # Can't use run_and_verify_status here because the out-of-date
  # information in the status output isn't copied in the status tree.
  expected = svntest.verify.UnorderedOutput(
         ["        *        1   " + A_path + "\n",
          "        *        1   " + wc_dir + "\n",
          "Status against revision:      2\n" ])

  svntest.actions.run_and_verify_svn(None,
                                     expected,
                                     [],
                                     "status", "-u",
                                     wc_dir)

  expected = svntest.verify.UnorderedOutput(
         ["                 1        1 jrandom      " +
          os.path.join(wc_dir, "iota") + "\n",
          "        *        1        1 jrandom      " + A_path + "\n",
          "        *        1        1 jrandom      " + wc_dir + "\n",
          "Status against revision:      2\n" ])

  svntest.actions.run_and_verify_svn(None, expected, [],
                                     "status", "-uvN",
                                     wc_dir)

  # Retrieve last changed date from svn log
  exit_code, output, error = svntest.actions.run_and_verify_svn(None, None, [],
                                                                'log', wc_dir,
                                                                '--xml', '-r1')

  info_msg = "<date>"
  for line in output:
    if line.find(info_msg) >= 0:
      time_str = line[:len(line)]
      break
  else:
    raise svntest.Failure

  xout = ["<?xml version=\"1.0\"?>\n",
          "<status>\n",
          "<target\n",
          "   path=\"%s\">\n" % (wc_dir),
          "<entry\n",
          "   path=\"%s\">\n" % (A_path),
          "<wc-status\n",
          "   props=\"none\"\n",
          "   item=\"normal\"\n",
          "   revision=\"1\">\n",
          "<commit\n",
          "   revision=\"1\">\n",
          "<author>%s</author>\n" % svntest.main.wc_author,
          time_str,
          "</commit>\n",
          "</wc-status>\n",
          "<repos-status\n",
          "   props=\"modified\"\n",
          "   item=\"none\">\n",
          "</repos-status>\n",
          "</entry>\n",
          "<entry\n",
          "   path=\"%s\">\n" % (wc_dir),
          "<wc-status\n",
          "   props=\"none\"\n",
          "   item=\"normal\"\n",
          "   revision=\"1\">\n",
          "<commit\n",
          "   revision=\"1\">\n",
          "<author>%s</author>\n" % svntest.main.wc_author,
          time_str,
          "</commit>\n",
          "</wc-status>\n",
          "<repos-status\n",
          "   props=\"modified\"\n",
          "   item=\"none\">\n",
          "</repos-status>\n",
          "</entry>\n",
          "<against\n",
          "   revision=\"2\"/>\n",
          "</target>\n",
          "</status>\n",]

  exit_code, output, error = svntest.actions.run_and_verify_svn(None, xout, [],
                                                                'status',
                                                                wc_dir,
                                                                '--xml', '-uN')

# more incoming prop updates.
def status_update_verbose_with_incoming_props(sbox):
  "run 'status -uv' w/ incoming propchanges"

  sbox.build()
  wc_dir = sbox.wc_dir
  A_path = os.path.join(wc_dir, 'A')
  D_path = os.path.join(A_path, 'D')
  B_path = os.path.join(A_path, 'B')
  E_path = os.path.join(A_path, 'B', 'E')
  G_path = os.path.join(A_path, 'D', 'G')
  H_path = os.path.join(A_path, 'D', 'H')
  # Add a property to the root folder and a subdir
  svntest.main.run_svn(None, 'propset', 'red', 'rojo', D_path)
  svntest.main.run_svn(None, 'propset', 'black', 'bobo', E_path)
  svntest.main.run_svn(None, 'propset', 'black', 'bobo', wc_dir)

  # Create expected output tree.
  expected_output = svntest.wc.State(wc_dir, {
    'A/D'   : Item(verb='Sending'),
    'A/B/E' : Item(verb='Sending'),
    ''      : Item(verb='Sending'),
    })
  # Created expected status tree.
  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)
  expected_status.tweak('A/D', wc_rev=2, status='  ')
  expected_status.tweak('A/B/E', wc_rev=2, status='  ')
  expected_status.tweak('', wc_rev=2, status='  ')

  # Commit the working copy
  svntest.actions.run_and_verify_commit(wc_dir, expected_output,
                                        expected_status,
                                        None, wc_dir)

  # Create expected trees for an update to revision 1.
  expected_output = svntest.wc.State(wc_dir, {
    'A/D'   : Item(status=' U'),
    'A/B/E' : Item(status=' U'),
    ''      : Item(status=' U'),
    })
  expected_disk = svntest.main.greek_state.copy()
  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)

  # Do the update and check the results in three ways... INCLUDING PROPS
  svntest.actions.run_and_verify_update(wc_dir,
                                        expected_output,
                                        expected_disk,
                                        expected_status,
                                        None, None, None, None, None, 1,
                                        '-r', '1', wc_dir)

  # Can't use run_and_verify_status here because the out-of-date
  # information in the status output isn't copied in the status tree.
  common = "        1        1 jrandom      "
  expected = svntest.verify.UnorderedOutput(
         ["         " + common + os.path.join(E_path, 'alpha') + "\n",
          "         " + common + os.path.join(E_path, 'beta') + "\n",
          "        *" + common + os.path.join(E_path) + "\n",
          "         " + common + os.path.join(B_path, 'lambda') + "\n",
          "         " + common + os.path.join(B_path, 'F') + "\n",
          "         " + common + B_path + "\n",
          "         " + common + os.path.join(G_path, 'pi') + "\n",
          "         " + common + os.path.join(G_path, 'rho') + "\n",
          "         " + common + os.path.join(G_path, 'tau') + "\n",
          "         " + common + G_path + "\n",
          "         " + common + os.path.join(H_path, 'chi') + "\n",
          "         " + common + os.path.join(H_path, 'omega') + "\n",
          "         " + common + os.path.join(H_path, 'psi') + "\n",
          "         " + common + H_path + "\n",
          "         " + common + os.path.join(D_path, 'gamma') + "\n",
          "        *" + common + D_path + "\n",
          "         " + common + os.path.join(A_path, 'mu') + "\n",
          "         " + common + os.path.join(A_path, 'C') + "\n",
          "         " + common + A_path + "\n",
          "         " + common + os.path.join(wc_dir, 'iota') + "\n",
          "        *" + common + wc_dir  + "\n",
          "Status against revision:      2\n" ])

  svntest.actions.run_and_verify_svn(None,
                                     expected,
                                     [],
                                     "status", "-uv", wc_dir)

#----------------------------------------------------------------------
# Test for issue #2468
def status_nonrecursive_update(sbox):
  "run 'status -uN' with incoming changes"

  sbox.build()
  wc_dir = sbox.wc_dir
  A_path = os.path.join(wc_dir, 'A')
  D_path = os.path.join(A_path, 'D')
  mu_path = os.path.join(A_path, 'mu')
  gamma_path = os.path.join(D_path, 'gamma')

  # Change files in A and D and commit
  svntest.main.file_append(mu_path, "new line of text")
  svntest.main.file_append(gamma_path, "new line of text")

  # Create expected trees for commit
  expected_output = svntest.wc.State(wc_dir, {
    'A/mu' : Item(verb='Sending'),
    'A/D/gamma' : Item(verb='Sending')
    })
  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)
  expected_status.tweak('A/mu', wc_rev=2, status='  ')
  expected_status.tweak('A/D/gamma', wc_rev=2, status='  ')

  svntest.actions.run_and_verify_commit(wc_dir, expected_output,
                                        expected_status,
                                        None, wc_dir)

  # Create expected trees for an update to revision 1.
  expected_output = svntest.wc.State(wc_dir, {
    'A/mu' : Item(status='U '),
    'A/D/gamma' : Item(status='U '),
    })
  expected_disk = svntest.main.greek_state.copy()
  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)

  # Do the update and check the results in three ways
  svntest.actions.run_and_verify_update(wc_dir,
                                        expected_output,
                                        expected_disk,
                                        expected_status,
                                        None, None, None, None, None, 0,
                                        '-r', '1', wc_dir)

  # Check the remote status of folder A (non-recursively)
  xout = ["        *        1   " + os.path.join(wc_dir, "A", "mu") + "\n",
          "Status against revision:      2\n" ]

  svntest.actions.run_and_verify_svn(None,
                                     xout,
                                     [],
                                     "status", "-uN", A_path)

def change_files(wc_dir, files):
  """Make a basic change to the files.
     files = a list of paths relative to the wc root directory
  """

  for file in files:
    filepath = os.path.join(wc_dir, file)
    svntest.main.file_append(filepath, "new line of text")

def change_files_and_commit(wc_dir, files, baserev=1):
  """Make a basic change to the files and commit them.
     files = a list of paths relative to the wc root directory
  """

  change_files(wc_dir, files)

  # Prepare expected trees for commit
  expected_output = svntest.wc.State(wc_dir, {
    'A/mu' : Item(verb='Sending'),
    'A/D/gamma' : Item(verb='Sending')
    })
  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)

  commitrev = baserev + 1
  for file in files:
    expected_output.add({file : Item(verb='Sending')})
    expected_status.tweak(file, wc_rev=commitrev, status='  ')

  svntest.actions.run_and_verify_commit(wc_dir, expected_output,
                                        expected_status,
                                        None, wc_dir)

def status_depth_local(sbox):
  "run 'status --depth=X' with local changes"

  sbox.build(read_only = True)
  wc_dir = sbox.wc_dir
  A_path = os.path.join(wc_dir, 'A')
  D_path = os.path.join(A_path, 'D')

  mu_path = os.path.join(A_path, 'mu')
  gamma_path = os.path.join(D_path, 'gamma')

  # make some changes to the greek tree
  change_files(wc_dir, ['A/mu', 'A/D/gamma'])
  svntest.main.run_svn(None, 'propset', 'svn:test', 'value', A_path)
  svntest.main.run_svn(None, 'propset', 'svn:test', 'value', D_path)

  # for all the possible types of depth, check the status

  # depth=empty
  expected = svntest.verify.UnorderedOutput(
                  [" M      %s\n" % A_path])
  svntest.actions.run_and_verify_svn(None,
                                     expected,
                                     [],
                                     "status", "--depth=empty", A_path)

  # depth=files
  expected = svntest.verify.UnorderedOutput(
                  [" M      %s\n" % A_path,
                   "M       %s\n" % mu_path])

  svntest.actions.run_and_verify_svn(None,
                                     expected,
                                     [],
                                     "status", "--depth=files", A_path)

  # depth=immediates
  expected = svntest.verify.UnorderedOutput(
                  [" M      %s\n" % A_path,
                   " M      %s\n" % D_path,
                   "M       %s\n" % mu_path])

  svntest.actions.run_and_verify_svn(None,
                                     expected,
                                     [],
                                     "status", "--depth=immediates", A_path)

  # depth=infinity (the default)
  expected = svntest.verify.UnorderedOutput(
                  [" M      %s\n" % A_path,
                   " M      %s\n" % D_path,
                   "M       %s\n" % mu_path,
                   "M       %s\n" % gamma_path])

  svntest.actions.run_and_verify_svn(None,
                                     expected,
                                     [],
                                     "status", "--depth=infinity", A_path)

def status_depth_update(sbox):
  "run 'status --depth=X -u' with incoming changes"

  sbox.build()
  wc_dir = sbox.wc_dir
  A_path = os.path.join(wc_dir, 'A')
  D_path = os.path.join(A_path, 'D')

  mu_path = os.path.join(A_path, 'mu')
  gamma_path = os.path.join(D_path, 'gamma')

  # add some files, change directory properties
  change_files_and_commit(wc_dir, ['A/mu', 'A/D/gamma'])
  svntest.main.run_svn(None, 'up', wc_dir)
  svntest.main.run_svn(None, 'propset', 'svn:test', 'value', A_path)
  svntest.main.run_svn(None, 'propset', 'svn:test', 'value', D_path)
  svntest.main.run_svn(None, 'ci', '-m', 'log message', wc_dir)

  # update to r1
  svntest.main.run_svn(None, 'up', '-r', '1', wc_dir)

  # for all the possible types of depth, check the status

  # depth=empty
  expected = svntest.verify.UnorderedOutput(
                  ["        *        1   %s\n" % A_path,
                   "Status against revision:      3\n"])

  svntest.actions.run_and_verify_svn(None,
                                     expected,
                                     [],
                                     "status", "-u", "--depth=empty", A_path)

  # depth=files
  expected = svntest.verify.UnorderedOutput(
                  ["        *        1   %s\n" % mu_path,
                   "        *        1   %s\n" % A_path,
                   "Status against revision:      3\n"])

  svntest.actions.run_and_verify_svn(None,
                                     expected,
                                     [],
                                     "status", "-u", "--depth=files",
                                     A_path)

  # depth=immediates
  expected = svntest.verify.UnorderedOutput(
                  ["        *        1   %s\n" % A_path,
                   "        *        1   %s\n" % D_path,
                   "        *        1   %s\n" % mu_path,
                   "Status against revision:      3\n"])

  svntest.actions.run_and_verify_svn(None,
                                     expected,
                                     [],
                                     "status", "-u", "--depth=immediates",
                                     A_path)

  # depth=infinity (the default)
  expected = svntest.verify.UnorderedOutput(
                  ["        *        1   %s\n" % A_path,
                   "        *        1   %s\n" % D_path,
                   "        *        1   %s\n" % mu_path,
                   "        *        1   %s\n" % gamma_path,
                   "Status against revision:      3\n"])

  svntest.actions.run_and_verify_svn(None,
                                     expected,
                                     [],
                                     "status", "-u", "--depth=infinity",
                                     A_path)


#----------------------------------------------------------------------
# Test for issue #2420
def status_dash_u_deleted_directories(sbox):
  "run 'status -u' with locally deleted directories"

  sbox.build()
  wc_dir = sbox.wc_dir
  A_path = os.path.join(wc_dir, 'A')
  B_path = os.path.join(A_path, 'B')

  # delete the B directory
  svntest.actions.run_and_verify_svn(None, None, [],
                                     'rm', B_path)

  # now run status -u on B and its children
  was_cwd = os.getcwd()

  os.chdir(A_path)

  # check status -u of B
  expected = svntest.verify.UnorderedOutput(
         ["D                1   %s\n" % "B",
          "D                1   %s\n" % os.path.join("B", "lambda"),
          "D                1   %s\n" % os.path.join("B", "E"),
          "D                1   %s\n" % os.path.join("B", "E", "alpha"),
          "D                1   %s\n" % os.path.join("B", "E", "beta"),
          "D                1   %s\n" % os.path.join("B", "F"),
          "Status against revision:      1\n" ])
  svntest.actions.run_and_verify_svn(None,
                                     expected,
                                     [],
                                     "status", "-u", "B")

  # again, but now from inside B, should give the same output
  os.chdir("B")
  expected = svntest.verify.UnorderedOutput(
         ["D                1   %s\n" % ".",
          "D                1   %s\n" % "lambda",
          "D                1   %s\n" % "E",
          "D                1   %s\n" % os.path.join("E", "alpha"),
          "D                1   %s\n" % os.path.join("E", "beta"),
          "D                1   %s\n" % "F",
          "Status against revision:      1\n" ])
  svntest.actions.run_and_verify_svn(None,
                                     expected,
                                     [],
                                     "status", "-u", ".")

  # check status -u of B/E
  expected = svntest.verify.UnorderedOutput(
         ["D                1   %s\n" % os.path.join("B", "E"),
          "D                1   %s\n" % os.path.join("B", "E", "alpha"),
          "D                1   %s\n" % os.path.join("B", "E", "beta"),
          "Status against revision:      1\n" ])

  os.chdir(was_cwd)
  os.chdir(A_path)
  svntest.actions.run_and_verify_svn(None,
                                     expected,
                                     [],
                                     "status", "-u",
                                     os.path.join("B", "E"))

#----------------------------------------------------------------------

# Test for issue #2737: show obstructed status for versioned directories
# replaced by local directories.
def status_dash_u_type_change(sbox):
  "status -u on versioned items whose type changed"

  sbox.build(read_only = True)
  wc_dir = sbox.wc_dir

  os.chdir(wc_dir)

  # Change the versioned file iota into an unversioned dir.
  os.remove('iota')
  os.mkdir('iota')

  xout = ["~                1   iota\n",
          "Status against revision:      1\n" ]

  svntest.actions.run_and_verify_svn(None,
                                     xout,
                                     [],
                                     "status", "-u")

  # Change the versioned directory A into an unversioned dir.
  svntest.main.safe_rmtree('A')
  os.mkdir('A')

  expected = svntest.verify.UnorderedOutput(
         ["~                1   iota\n",
          "~               ?    A\n",
          "Status against revision:      1\n" ])

  svntest.actions.run_and_verify_svn(None,
                                     expected,
                                     [],
                                     "status", "-u")

#----------------------------------------------------------------------

def status_with_tree_conflicts(sbox):
  "status with tree conflicts"

  # Status messages reflecting tree conflict status.
  # These tests correspond to use cases 1-3 in
  # notes/tree-conflicts/use-cases.txt.

  svntest.actions.build_greek_tree_conflicts(sbox)
  wc_dir = sbox.wc_dir
  G = os.path.join(wc_dir, 'A', 'D', 'G')
  pi = os.path.join(G, 'pi')
  rho = os.path.join(G, 'rho')
  tau = os.path.join(G, 'tau')

  # check status of G
  expected = svntest.verify.UnorderedOutput(
         ["D     C %s\n" % pi,
          "      >   local delete, incoming edit upon update\n",
          "A  +  C %s\n" % rho,
          "      >   local edit, incoming delete upon update\n",
          "!     C %s\n" % tau,
          "      >   local delete, incoming delete upon update\n",
          ])

  svntest.actions.run_and_verify_svn(None,
                                     expected,
                                     [],
                                     "status", G)

  # check status of G, with -v
  expected = svntest.verify.UnorderedOutput(
         ["                 2        2 jrandom      %s\n" % G,
          "D     C          2        2 jrandom      %s\n" % pi,
          "      >   local delete, incoming edit upon update\n",
          "A  +  C          -        1 jrandom      %s\n" % rho,
          "      >   local edit, incoming delete upon update\n",
          "!     C                                  %s\n" % tau,
          "      >   local delete, incoming delete upon update\n",
          ])


  svntest.actions.run_and_verify_svn(None,
                                     expected,
                                     [],
                                     "status", "-v", G)

  # check status of G, with -xml
  exit_code, output, error = svntest.main.run_svn(None, 'status', G, '--xml',
                                                  '-v')

  should_be_victim = {
    G:   False,
    pi:  True,
    rho: True,
    tau: True,
    }

  real_entry_count = 0
  output_str = r"".join(output)
  # skip the first string, which contains only 'status' and 'target' elements
  entries = output_str.split("<entry")[1:]

  for entry in entries:
    # get the entry's path
    m = re.search('path="([^"]+)"', entry)
    if m:
      real_entry_count += 1
      path = m.group(1)
      # check if the path should be a victim
      m = re.search('tree-conflicted="true"', entry)
      if (m is None) and should_be_victim[path]:
        print("ERROR: expected '%s' to be a tree conflict victim." % path)
        print("ACTUAL STATUS OUTPUT:")
        print(output_str)
        raise svntest.Failure
      if m and not should_be_victim[path]:
        print("ERROR: did NOT expect '%s' to be a tree conflict victim." % path)
        print("ACTUAL STATUS OUTPUT:")
        print(output_str)
        raise svntest.Failure

  if real_entry_count != len(should_be_victim):
    print("ERROR: 'status --xml' output is incomplete.")
    raise svntest.Failure


########################################################################
# Run the tests


# list all tests here, starting with None:
test_list = [ None,
              status_unversioned_file_in_current_dir,
              status_update_with_nested_adds,
              status_shows_all_in_current_dir,
              status_missing_file,
              status_type_change,
              SkipUnless(status_type_change_to_symlink,
                         svntest.main.is_posix_os),
              status_with_new_files_pending,
              status_for_unignored_file,
              status_for_nonexistent_file,
              status_file_needs_update,
              status_uninvited_parent_directory,
              status_on_forward_deletion,
              timestamp_behaviour,
              status_on_unversioned_dotdot,
              status_on_partially_nonrecursive_wc,
              missing_dir_in_anchor,
              status_in_xml,
              status_ignored_dir,
              status_unversioned_dir,
              status_missing_dir,
              status_nonrecursive_update_different_cwd,
              status_add_plus_conflict,
              inconsistent_eol,
              status_update_with_incoming_props,
              status_update_verbose_with_incoming_props,
              status_nonrecursive_update,
              status_dash_u_deleted_directories,
              status_depth_local,
              status_depth_update,
              status_dash_u_type_change,
              status_with_tree_conflicts,
             ]

if __name__ == '__main__':
  svntest.main.run_tests(test_list)
  # NOTREACHED


### End of file.
