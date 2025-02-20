#!/usr/bin/env python
#
#  lock_tests.py:  testing versioned properties
#
#  Subversion is a tool for revision control.
#  See http://subversion.tigris.org for more information.
#
# ====================================================================
# Copyright (c) 2005-2006, 2008 CollabNet.  All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.  The terms
# are also available at http://subversion.tigris.org/license-1.html.
# If newer versions of this license are posted there, you may use a
# newer version instead, at your option.
#
######################################################################

# General modules
import re, os, stat

# Our testing module
import svntest

# (abbreviation)
Skip = svntest.testcase.Skip
SkipUnless = svntest.testcase.SkipUnless
XFail = svntest.testcase.XFail
Item = svntest.wc.StateItem

######################################################################
# Tests

#----------------------------------------------------------------------
# Each test refers to a section in
# notes/locking/locking-functional-spec.txt

# II.A.2, II.C.2.a: Lock a file in wc A as user FOO and make sure we
# have a representation of it.  Checkout wc B as user BAR.  Verify
# that user BAR cannot commit changes to the file nor its properties.
def lock_file(sbox):
  "lock a file and verify that it's locked"

  sbox.build()
  wc_dir = sbox.wc_dir

  # Make a second copy of the working copy
  wc_b = sbox.add_wc_path('_b')
  svntest.actions.duplicate_dir(wc_dir, wc_b)

  # lock a file as wc_author
  fname = 'iota'
  file_path = os.path.join(sbox.wc_dir, fname)
  file_path_b = os.path.join(wc_b, fname)

  svntest.main.file_append(file_path, "This represents a binary file\n")
  svntest.main.run_svn(None, 'commit',
                       '-m', '', file_path)
  svntest.actions.run_and_verify_svn(None, ".*locked by user", [], 'lock',
                                     '-m', '', file_path)

  # --- Meanwhile, in our other working copy... ---
  err_re = "((.*User jconstant does not own lock on path.*)|(.*423 Locked.*))"

  svntest.main.run_svn(None, 'update', wc_b)
  # -- Try to change a file --
  # change the locked file
  svntest.main.file_append(file_path_b, "Covert tweak\n")

  # attempt (and fail) to commit as user Sally
  svntest.actions.run_and_verify_commit(wc_b, None, None, err_re,
                                        '--username',
                                        svntest.main.wc_author2,
                                        '-m', '', file_path_b)

  # Revert our change that we failed to commit
  svntest.main.run_svn(None, 'revert', file_path_b)

  # -- Try to change a property --
  # change the locked file's properties
  svntest.main.run_svn(None, 'propset', 'sneakyuser', 'Sally', file_path_b)

  err_re = "((.*User jconstant does not own lock on path.*)" + \
             "|(.*At least one property change failed.*))"

  # attempt (and fail) to commit as user Sally
  svntest.actions.run_and_verify_commit(wc_b, None, None, err_re,
                                        '--username',
                                        svntest.main.wc_author2,
                                        '-m', '', file_path_b)




#----------------------------------------------------------------------
# II.C.2.b.[12]: Lock a file and commit using the lock.  Make sure the
# lock is released.  Repeat, but request that the lock not be
# released.  Make sure the lock is retained.
def commit_file_keep_lock(sbox):
  "commit a file and keep lock"

  sbox.build()
  wc_dir = sbox.wc_dir

  fname = 'A/mu'
  file_path = os.path.join(sbox.wc_dir, fname)

  # lock fname as wc_author
  svntest.actions.run_and_verify_svn(None, ".*locked by user", [], 'lock',
                                     '-m', 'some lock comment', file_path)

  # make a change and commit it, holding lock
  svntest.main.file_append(file_path, "Tweak!\n")
  svntest.main.run_svn(None, 'commit', '-m', '', '--no-unlock',
                       file_path)

  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)
  expected_status.tweak(fname, wc_rev=2)
  expected_status.tweak(fname, writelocked='K')

  # Make sure the file is still locked
  svntest.actions.run_and_verify_status(wc_dir, expected_status)

def commit_file_unlock(sbox):
  "commit a file and release lock"

  sbox.build()
  wc_dir = sbox.wc_dir

  fname = 'A/mu'
  file_path = os.path.join(sbox.wc_dir, fname)

  # lock fname as wc_author
  svntest.actions.run_and_verify_svn(None, ".*locked by user", [], 'lock',
                                     '-m', 'some lock comment', file_path)

  # make a change and commit it, allowing lock to be released
  svntest.main.file_append(file_path, "Tweak!\n")
  svntest.main.run_svn(None, 'commit', '-m', '',
                       file_path)

  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)
  expected_status.tweak(fname, wc_rev=2)

  # Make sure the file is unlocked
  svntest.actions.run_and_verify_status(wc_dir, expected_status)

#----------------------------------------------------------------------
def commit_propchange(sbox):
  "commit a locked file with a prop change"

  sbox.build()
  wc_dir = sbox.wc_dir

  fname = 'A/mu'
  file_path = os.path.join(sbox.wc_dir, fname)

  # lock fname as wc_author
  svntest.actions.run_and_verify_svn(None, ".*locked by user", [], 'lock',
                                     '-m', 'some lock comment', file_path)

  # make a property change and commit it, allowing lock to be released
  svntest.main.run_svn(None, 'propset', 'blue', 'azul', file_path)
  svntest.main.run_svn(None, 'commit',
                             '-m', '', file_path)

  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)
  expected_status.tweak(fname, wc_rev=2)

  # Make sure the file is unlocked
  svntest.actions.run_and_verify_status(wc_dir, expected_status)

#----------------------------------------------------------------------
# II.C.2.c: Lock a file in wc A as user FOO.  Attempt to unlock same
# file in same wc as user BAR.  Should fail.
#
# Attempt again with --force.  Should succeed.
#
# II.C.2.c: Lock a file in wc A as user FOO.  Attempt to unlock same
# file in wc B as user FOO.  Should fail.
#
# Attempt again with --force.  Should succeed.
def break_lock(sbox):
  "lock a file and verify lock breaking behavior"

  sbox.build()
  wc_dir = sbox.wc_dir

  # Make a second copy of the working copy
  wc_b = sbox.add_wc_path('_b')
  svntest.actions.duplicate_dir(wc_dir, wc_b)

  # lock a file as wc_author
  fname = 'iota'
  file_path = os.path.join(sbox.wc_dir, fname)
  file_path_b = os.path.join(wc_b, fname)

  svntest.actions.run_and_verify_svn(None, ".*locked by user", [], 'lock',
                                     '-m', '', file_path)

  # --- Meanwhile, in our other working copy... ---

  svntest.main.run_svn(None, 'update', wc_b)

  # attempt (and fail) to unlock file

  # This should give a "iota' is not locked in this working copy" error
  svntest.actions.run_and_verify_svn(None, None, ".*not locked",
                                     'unlock',
                                     file_path_b)

  svntest.actions.run_and_verify_svn(None, ".*unlocked", [],
                                     'unlock', '--force',
                                     file_path_b)

#----------------------------------------------------------------------
# II.C.2.d: Lock a file in wc A as user FOO.  Attempt to lock same
# file in wc B as user BAR.  Should fail.
#
# Attempt again with --force.  Should succeed.
#
# II.C.2.d: Lock a file in wc A as user FOO.  Attempt to lock same
# file in wc B as user FOO.  Should fail.
#
# Attempt again with --force.  Should succeed.
def steal_lock(sbox):
  "lock a file and verify lock stealing behavior"

  sbox.build()
  wc_dir = sbox.wc_dir

  # Make a second copy of the working copy
  wc_b = sbox.add_wc_path('_b')
  svntest.actions.duplicate_dir(wc_dir, wc_b)

  # lock a file as wc_author
  fname = 'iota'
  file_path = os.path.join(sbox.wc_dir, fname)
  file_path_b = os.path.join(wc_b, fname)

  svntest.actions.run_and_verify_svn(None, ".*locked by user", [], 'lock',
                                     '-m', '', file_path)

  # --- Meanwhile, in our other working copy... ---

  svntest.main.run_svn(None, 'update', wc_b)

  # attempt (and fail) to lock file

  # This should give a "iota' is already locked... error, but exits 0.
  svntest.actions.run_and_verify_svn2(None, None,
                                      ".*already locked", 0,
                                      'lock',
                                      '-m', 'trying to break', file_path_b)

  svntest.actions.run_and_verify_svn(None, ".*locked by user", [],
                                     'lock', '--force',
                                     '-m', 'trying to break', file_path_b)

#----------------------------------------------------------------------
# II.B.2, II.C.2.e: Lock a file in wc A.  Query wc for the
# lock and verify that all lock fields are present and correct.
def examine_lock(sbox):
  "examine the fields of a lockfile for correctness"

  sbox.build()
  wc_dir = sbox.wc_dir

  fname = 'iota'
  comment = 'This is a lock test.'
  file_path = os.path.join(sbox.wc_dir, fname)

  # lock a file as wc_author
  svntest.actions.run_and_validate_lock(file_path,
                                        svntest.main.wc_author)

#----------------------------------------------------------------------
# II.C.1: Lock a file in wc A.  Check out wc B.  Break the lock in wc
# B.  Verify that wc A gracefully cleans up the lock via update as
# well as via commit.
def handle_defunct_lock(sbox):
  "verify behavior when a lock in a wc is defunct"

  sbox.build()
  wc_dir = sbox.wc_dir


  fname = 'iota'
  file_path = os.path.join(sbox.wc_dir, fname)

  # set up our expected status
  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)

  # lock the file
  svntest.actions.run_and_verify_svn(None, ".*locked by user", [], 'lock',
                                     '-m', '', file_path)

  # Make a second copy of the working copy
  wc_b = sbox.add_wc_path('_b')
  svntest.actions.duplicate_dir(wc_dir, wc_b)
  file_path_b = os.path.join(wc_b, fname)

  # --- Meanwhile, in our other working copy... ---

  # Try unlocking the file in the second wc.
  svntest.actions.run_and_verify_svn(None, ".*unlocked", [], 'unlock',
                                     file_path_b)


  # update the 1st wc, which should clear the lock there
  svntest.main.run_svn(None, 'update', wc_dir)

  # Make sure the file is unlocked
  svntest.actions.run_and_verify_status(wc_dir, expected_status)



#----------------------------------------------------------------------
# II.B.1: Set "svn:needs-lock" property on file in wc A.  Checkout wc
# B and verify that that file is set as read-only.
#
# Tests propset, propdel, lock, and unlock
def enforce_lock(sbox):
  "verify svn:needs-lock read-only behavior"

  sbox.build()
  wc_dir = sbox.wc_dir

  iota_path = os.path.join(wc_dir, 'iota')
  lambda_path = os.path.join(wc_dir, 'A', 'B', 'lambda')
  mu_path = os.path.join(wc_dir, 'A', 'mu')

  # Set some binary properties.
  propval_path = os.path.join(wc_dir, 'propval.tmp')

  # svn:needs-lock value should be forced to a '*'
  svntest.actions.set_prop(None, 'svn:needs-lock', 'foo', iota_path,
                           propval_path)
  svntest.actions.set_prop(None, 'svn:needs-lock', '*', lambda_path,
                           propval_path)
  expected_err = ".*svn: warning: To turn off the svn:needs-lock property,.*"
  svntest.actions.set_prop(expected_err, 'svn:needs-lock', '      ',
                           mu_path, propval_path)

  # Check svn:needs-lock
  svntest.actions.check_prop('svn:needs-lock', iota_path, ['*'])
  svntest.actions.check_prop('svn:needs-lock', lambda_path, ['*'])
  svntest.actions.check_prop('svn:needs-lock', mu_path, ['*'])

  svntest.main.run_svn(None, 'commit',
                       '-m', '', iota_path, lambda_path, mu_path)

  # Now make sure that the perms were flipped on all files
  if os.name == 'posix':
    mode = stat.S_IWGRP | stat.S_IWOTH | stat.S_IWRITE
    if ((os.stat(iota_path)[0] & mode)
        or (os.stat(lambda_path)[0] & mode)
        or (os.stat(mu_path)[0] & mode)):
      print("Setting 'svn:needs-lock' property on a file failed to set")
      print("file mode to read-only.")
      raise svntest.Failure

    # obtain a lock on one of these files...
    svntest.actions.run_and_verify_svn(None, ".*locked by user", [], 'lock',
                                       '-m', '', iota_path)

    # ...and verify that the write bit gets set...
    if not (os.stat(iota_path)[0] & mode):
      print("Locking a file with 'svn:needs-lock' failed to set write bit.")
      raise svntest.Failure

    # ...and unlock it...
    svntest.actions.run_and_verify_svn(None, ".*unlocked", [], 'unlock',
                                       iota_path)

    # ...and verify that the write bit gets unset
    if (os.stat(iota_path)[0] & mode):
      print("Unlocking a file with 'svn:needs-lock' failed to unset write bit.")
      raise svntest.Failure

    # Verify that removing the property restores the file to read-write
    svntest.main.run_svn(None, 'propdel', 'svn:needs-lock', iota_path)
    if not (os.stat(iota_path)[0] & mode):
      print("Deleting 'svn:needs-lock' failed to set write bit.")
      raise svntest.Failure

#----------------------------------------------------------------------
# Test that updating a file with the "svn:needs-lock" property works,
# especially on Windows, where renaming A to B fails if B already
# exists and has its read-only bit set.  See also issue #2278.
def update_while_needing_lock(sbox):
  "update handles svn:needs-lock correctly"

  sbox.build()
  wc_dir = sbox.wc_dir

  iota_path = os.path.join(wc_dir, 'iota')
  svntest.main.run_svn(None,
                       'propset', 'svn:needs-lock', 'foo', iota_path)
  svntest.main.run_svn(None,
                       'commit', '-m', 'log msg', iota_path)
  svntest.main.run_svn(None,
                       'up', wc_dir)

  # Lock, modify, commit, unlock, to create r3.
  svntest.actions.run_and_verify_svn(None, ".*locked by user", [], 'lock',
                                     '-m', '', iota_path)
  svntest.main.file_append(iota_path, "This line added in r2.\n")
  svntest.main.run_svn(None, 'commit',
                       '-m', '', iota_path) # auto-unlocks

  # Backdate to r2.
  svntest.main.run_svn(None,
                       'update', '-r2', iota_path)

  # Try updating forward to r3 again.  This is where the bug happened.
  svntest.main.run_svn(None,
                       'update', '-r3', iota_path)


#----------------------------------------------------------------------
# Tests update / checkout with changing props
def defunct_lock(sbox):
  "verify svn:needs-lock behavior with defunct lock"

  sbox.build()
  wc_dir = sbox.wc_dir

  # Make a second copy of the working copy
  wc_b = sbox.add_wc_path('_b')
  svntest.actions.duplicate_dir(wc_dir, wc_b)

  iota_path = os.path.join(wc_dir, 'iota')
  iota_path_b = os.path.join(wc_b, 'iota')

  mode = stat.S_IWGRP | stat.S_IWOTH | stat.S_IWRITE

# Set the prop in wc a
  svntest.main.run_svn(None, 'propset', 'svn:needs-lock', 'foo', iota_path)

  # commit r2
  svntest.main.run_svn(None, 'commit',
                       '-m', '', iota_path)

  # update wc_b
  svntest.main.run_svn(None, 'update', wc_b)

  # lock iota in wc_b
  svntest.actions.run_and_verify_svn(None, ".*locked by user", [], 'lock',
                                     '-m', '', iota_path_b)


  # break the lock iota in wc a
  svntest.actions.run_and_verify_svn(None, ".*locked by user", [], 'lock', '--force',
                                     '-m', '', iota_path)
  # update wc_b
  svntest.main.run_svn(None, 'update', wc_b)

  # make sure that iota got set to read-only
  if (os.stat(iota_path_b)[0] & mode):
    print("Upon removal of a defunct lock, a file with 'svn:needs-lock'")
    print("was not set back to read-only")
    raise svntest.Failure



#----------------------------------------------------------------------
# Tests dealing with a lock on a deleted path
def deleted_path_lock(sbox):
  "verify lock removal on a deleted path"

  sbox.build()
  wc_dir = sbox.wc_dir

  iota_path = os.path.join(wc_dir, 'iota')
  iota_url = sbox.repo_url + '/iota'

  svntest.actions.run_and_verify_svn(None, ".*locked by user", [], 'lock',
                                     '-m', '', iota_path)

  svntest.actions.run_and_verify_svn(None, None, [], 'delete', iota_path)

  svntest.actions.run_and_verify_svn(None, None, [], 'commit',
                                     '--no-unlock',
                                     '-m', '', iota_path)

  # Now make sure that we can delete the lock from iota via a URL
  svntest.actions.run_and_verify_svn(None, ".*unlocked", [], 'unlock',
                                     iota_url)



#----------------------------------------------------------------------
# Tests dealing with locking and unlocking
def lock_unlock(sbox):
  "lock and unlock some files"

  sbox.build()
  wc_dir = sbox.wc_dir

  pi_path = os.path.join(wc_dir, 'A', 'D', 'G', 'pi')
  rho_path = os.path.join(wc_dir, 'A', 'D', 'G', 'rho')
  tau_path = os.path.join(wc_dir, 'A', 'D', 'G', 'tau')

  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)
  expected_status.tweak('A/D/G/pi', 'A/D/G/rho', 'A/D/G/tau', writelocked='K')

  svntest.actions.run_and_verify_svn(None, ".*locked by user", [], 'lock',
                                     '-m', '', pi_path, rho_path, tau_path)

  svntest.actions.run_and_verify_status(wc_dir, expected_status)

  expected_status.tweak('A/D/G/pi', 'A/D/G/rho', 'A/D/G/tau', writelocked=None)

  svntest.actions.run_and_verify_svn(None, ".*unlocked", [], 'unlock',
                                     pi_path, rho_path, tau_path)

  svntest.actions.run_and_verify_status(wc_dir, expected_status)

#----------------------------------------------------------------------
# Tests dealing with directory deletion and locks
def deleted_dir_lock(sbox):
  "verify removal of a directory with locks inside"

  sbox.build()
  wc_dir = sbox.wc_dir

  parent_dir = os.path.join(wc_dir, 'A', 'D', 'G')
  pi_path = os.path.join(wc_dir, 'A', 'D', 'G', 'pi')
  rho_path = os.path.join(wc_dir, 'A', 'D', 'G', 'rho')
  tau_path = os.path.join(wc_dir, 'A', 'D', 'G', 'tau')

  svntest.actions.run_and_verify_svn(None, ".*locked by user", [], 'lock',
                                     '-m', '', pi_path, rho_path, tau_path)

  svntest.actions.run_and_verify_svn(None, None, [], 'delete', parent_dir)

  svntest.actions.run_and_verify_svn(None, None, [], 'commit',
                                     '--no-unlock',
                                     '-m', '', parent_dir)

#----------------------------------------------------------------------
# III.c : Lock a file and check the output of 'svn stat' from the same
# working copy and another.
def lock_status(sbox):
  "verify status of lock in working copy"
  sbox.build()
  wc_dir = sbox.wc_dir

   # Make a second copy of the working copy
  wc_b = sbox.add_wc_path('_b')
  svntest.actions.duplicate_dir(wc_dir, wc_b)

  # lock a file as wc_author
  fname = 'iota'
  file_path = os.path.join(sbox.wc_dir, fname)

  svntest.main.file_append(file_path, "This is a spreadsheet\n")
  svntest.main.run_svn(None, 'commit',
                       '-m', '', file_path)

  svntest.main.run_svn(None, 'lock',
                       '-m', '', file_path)

  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)
  expected_status.tweak(fname, wc_rev=2)
  expected_status.tweak(fname, writelocked='K')

  svntest.actions.run_and_verify_status(wc_dir, expected_status)

  # Verify status again after modifying the file
  svntest.main.file_append(file_path, "check stat output after mod")

  expected_status.tweak(fname, status='M ')

  svntest.actions.run_and_verify_status(wc_dir, expected_status)

  # Verify status of lock from another working copy
  svntest.main.run_svn(None, 'update', wc_b)
  expected_status = svntest.actions.get_virginal_state(wc_b, 2)
  expected_status.tweak(fname, writelocked='O')

  svntest.actions.run_and_verify_status(wc_b, expected_status)

#----------------------------------------------------------------------
# III.c : Steal lock on a file from another working copy with 'svn lock
# --force', and check the status of lock in the repository from the
# working copy in which the file was initially locked.
def stolen_lock_status(sbox):
  "verify status of stolen lock"
  sbox.build()
  wc_dir = sbox.wc_dir

  # Make a second copy of the working copy
  wc_b = sbox.add_wc_path('_b')
  svntest.actions.duplicate_dir(wc_dir, wc_b)

  # lock a file as wc_author
  fname = 'iota'
  file_path = os.path.join(sbox.wc_dir, fname)
  file_path_b = os.path.join(wc_b, fname)

  svntest.main.file_append(file_path, "This is a spreadsheet\n")
  svntest.main.run_svn(None, 'commit',
                       '-m', '', file_path)

  svntest.main.run_svn(None, 'lock',
                       '-m', '', file_path)

  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)
  expected_status.tweak(fname, wc_rev=2)
  expected_status.tweak(fname, writelocked='K')

  svntest.actions.run_and_verify_status(wc_dir, expected_status)

  # Forcibly lock same file (steal lock) from another working copy
  svntest.main.run_svn(None, 'update', wc_b)
  svntest.main.run_svn(None, 'lock',
                       '-m', '', '--force', file_path_b)

  # Verify status from working copy where file was initially locked
  expected_status.tweak(fname, writelocked='T')
  svntest.actions.run_and_verify_status(wc_dir, expected_status)

#----------------------------------------------------------------------
# III.c : Break lock from another working copy with 'svn unlock --force'
# and verify the status of the lock in the repository with 'svn stat -u'
# from the working copy in the file was initially locked
def broken_lock_status(sbox):
  "verify status of broken lock"
  sbox.build()
  wc_dir = sbox.wc_dir

  # Make a second copy of the working copy
  wc_b = sbox.add_wc_path('_b')
  svntest.actions.duplicate_dir(wc_dir, wc_b)

  # lock a file as wc_author
  fname = 'iota'
  file_path = os.path.join(sbox.wc_dir, fname)
  file_path_b = os.path.join(wc_b, fname)

  svntest.main.file_append(file_path, "This is a spreadsheet\n")
  svntest.main.run_svn(None, 'commit',
                       '-m', '', file_path)
  svntest.main.run_svn(None, 'lock',
                       '-m', '', file_path)

  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)
  expected_status.tweak(fname, wc_rev=2)
  expected_status.tweak(fname, writelocked='K')

  svntest.actions.run_and_verify_status(wc_dir, expected_status)

  # Forcibly unlock the same file (break lock) from another working copy
  svntest.main.run_svn(None, 'update', wc_b)
  svntest.main.run_svn(None, 'unlock',
                       '--force', file_path_b)

  # Verify status from working copy where file was initially locked
  expected_status.tweak(fname, writelocked='B')

  svntest.actions.run_and_verify_status(wc_dir, expected_status)

#----------------------------------------------------------------------
# Invalid input test - lock non-existent file
def lock_non_existent_file(sbox):
  "verify error on locking non-existent file"

  sbox.build()
  fname = 'A/foo'
  file_path = os.path.join(sbox.wc_dir, fname)

  exit_code, output, error = svntest.main.run_svn(1, 'lock',
                                                  '-m', '', file_path)

  error_msg = "foo' is not under version control"
  for line in error:
    if line.find(error_msg) != -1:
      break
  else:
    print("Error: %s : not found in: %s" % (error_msg, error))
    raise svntest.Failure

#----------------------------------------------------------------------
# Check that locking an out-of-date file fails.
def out_of_date(sbox):
  "lock an out-of-date file and ensure failure"

  sbox.build()
  wc_dir = sbox.wc_dir

  # Make a second copy of the working copy
  wc_b = sbox.add_wc_path('_b')
  svntest.actions.duplicate_dir(wc_dir, wc_b)

  fname = 'iota'
  file_path = os.path.join(sbox.wc_dir, fname)
  file_path_b = os.path.join(wc_b, fname)

  # Make a new revision of the file in the first WC.
  svntest.main.file_append(file_path, "This represents a binary file\n")
  svntest.main.run_svn(None, 'commit',
                       '-m', '', file_path)

  # --- Meanwhile, in our other working copy... ---
  svntest.actions.run_and_verify_svn2(None, None,
                                      ".*newer version of '/iota' exists", 0,
                                      'lock',
                                      '--username', svntest.main.wc_author2,
                                      '-m', '', file_path_b)

#----------------------------------------------------------------------
# Tests reverting a svn:needs-lock file
def revert_lock(sbox):
  "verify svn:needs-lock behavior with revert"

  sbox.build()
  wc_dir = sbox.wc_dir

  iota_path = os.path.join(wc_dir, 'iota')

  mode = stat.S_IWGRP | stat.S_IWOTH | stat.S_IWRITE

  # set the prop in wc
  svntest.actions.run_and_verify_svn(None, None, [], 'propset',
                                  'svn:needs-lock', 'foo', iota_path)

  # commit r2
  svntest.actions.run_and_verify_svn(None, None, [], 'commit',
                       '-m', '', iota_path)

  # make sure that iota got set to read-only
  if (os.stat(iota_path)[0] & mode):
    print("Committing a file with 'svn:needs-lock'")
    print("did not set the file to read-only")
    raise svntest.Failure

  # verify status is as we expect
  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)
  expected_status.tweak('iota', wc_rev=2)
  svntest.actions.run_and_verify_status(wc_dir, expected_status)

  # remove read-only-ness
  svntest.actions.run_and_verify_svn(None, None, [], 'propdel',
                                  'svn:needs-lock', iota_path)

  # make sure that iota got read-only-ness removed
  if (os.stat(iota_path)[0] & mode == 0):
    print("Deleting the 'svn:needs-lock' property ")
    print("did not remove read-only-ness")
    raise svntest.Failure

  # revert the change
  svntest.actions.run_and_verify_svn(None, None, [], 'revert', iota_path)

  # make sure that iota got set back to read-only
  if (os.stat(iota_path)[0] & mode):
    print("Reverting a file with 'svn:needs-lock'")
    print("did not set the file back to read-only")
    raise svntest.Failure

  # try propdel and revert from a different directory so
  # full filenames are used
  extra_name = 'xx'

  # now lock the file
  svntest.actions.run_and_verify_svn(None, ".*locked by user", [], 'lock',
                       '-m', '', iota_path)

  # modify it
  svntest.main.file_append(iota_path, "This line added\n")

  expected_status.tweak(wc_rev=1)
  expected_status.tweak('iota', wc_rev=2)
  expected_status.tweak('iota', status='M ', writelocked='K')
  svntest.actions.run_and_verify_status(wc_dir, expected_status)

  # revert it
  svntest.actions.run_and_verify_svn(None, None, [], 'revert', iota_path)

  # make sure it is still writable since we have the lock
  if (os.stat(iota_path)[0] & mode == 0):
    print("Reverting a 'svn:needs-lock' file (with lock in wc) ")
    print("did not leave the file writable")
    raise svntest.Failure


#----------------------------------------------------------------------
def examine_lock_via_url(sbox):
  "examine the fields of a lock from a URL"

  sbox.build()
  wc_dir = sbox.wc_dir

  fname = 'iota'
  comment = 'This is a lock test.'
  file_path = os.path.join(sbox.wc_dir, fname)
  file_url = sbox.repo_url + '/' + fname

  # lock the file url and check the contents of lock
  svntest.actions.run_and_validate_lock(file_url,
                                        svntest.main.wc_author2)

#----------------------------------------------------------------------
def lock_several_files(sbox):
  "lock/unlock several files in one go"

  sbox.build()
  wc_dir = sbox.wc_dir

  # Deliberately have no direct child of A as a target
  iota_path = os.path.join(sbox.wc_dir, 'iota')
  lambda_path = os.path.join(sbox.wc_dir, 'A', 'B', 'lambda')
  alpha_path = os.path.join(sbox.wc_dir, 'A', 'B', 'E', 'alpha')

  svntest.actions.run_and_verify_svn(None, ".*locked by user", [], 'lock',
                                     '--username', svntest.main.wc_author2,
                                     '-m', 'lock several',
                                     iota_path, lambda_path, alpha_path)

  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)
  expected_status.tweak('iota', 'A/B/lambda', 'A/B/E/alpha', writelocked='K')
  svntest.actions.run_and_verify_status(wc_dir, expected_status)

  svntest.actions.run_and_verify_svn(None, ".*unlocked", [], 'unlock',
                                     '--username', svntest.main.wc_author2,
                                     iota_path, lambda_path, alpha_path)

  expected_status.tweak('iota', 'A/B/lambda', 'A/B/E/alpha', writelocked=None)
  svntest.actions.run_and_verify_status(wc_dir, expected_status)

#----------------------------------------------------------------------
def lock_switched_files(sbox):
  "lock/unlock switched files"

  sbox.build()
  wc_dir = sbox.wc_dir

  gamma_path = os.path.join(wc_dir, 'A', 'D', 'gamma')
  lambda_path = os.path.join(wc_dir, 'A', 'B', 'lambda')
  iota_URL = sbox.repo_url + '/iota'
  alpha_URL = sbox.repo_url + '/A/B/E/alpha'

  svntest.actions.run_and_verify_svn(None, None, [], 'switch',
                                     iota_URL, gamma_path)
  svntest.actions.run_and_verify_svn(None, None, [], 'switch',
                                     alpha_URL, lambda_path)

  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)
  expected_status.tweak('A/D/gamma', 'A/B/lambda', switched='S')
  svntest.actions.run_and_verify_status(wc_dir, expected_status)

  svntest.actions.run_and_verify_svn(None, ".*locked by user", [], 'lock',
                                     '-m', 'lock several',
                                     gamma_path, lambda_path)

  expected_status.tweak('A/D/gamma', 'A/B/lambda', writelocked='K')
  expected_status.tweak('A/B/E/alpha', 'iota', writelocked='O')
  svntest.actions.run_and_verify_status(wc_dir, expected_status)

  svntest.actions.run_and_verify_svn(None, ".*unlocked", [], 'unlock',
                                     gamma_path, lambda_path)

  expected_status.tweak('A/D/gamma', 'A/B/lambda', writelocked=None)
  expected_status.tweak('A/B/E/alpha', 'iota', writelocked=None)
  svntest.actions.run_and_verify_status(wc_dir, expected_status)

def lock_uri_encoded(sbox):
  "lock and unlock a file with an URI-unsafe name"

  sbox.build()
  wc_dir = sbox.wc_dir

  # lock a file as wc_author
  fname = 'amazing space'
  file_path = os.path.join(wc_dir, fname)

  svntest.main.file_append(file_path, "This represents a binary file\n")
  svntest.actions.run_and_verify_svn(None, None, [], "add", file_path)

  expected_output = svntest.wc.State(wc_dir, {
    fname : Item(verb='Adding'),
    })

  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)
  expected_status.add({ fname: Item(wc_rev=2, status='  ') })

  # Commit the file.
  svntest.actions.run_and_verify_commit(wc_dir,
                                        expected_output,
                                        expected_status,
                                        None,
                                        file_path)

  svntest.actions.run_and_verify_svn(None, ".*locked by user", [], 'lock',
                                     '-m', '', file_path)

  # Make sure that the file was locked.
  expected_status.tweak(fname, writelocked='K')
  svntest.actions.run_and_verify_status(wc_dir, expected_status)

  svntest.actions.run_and_verify_svn(None, ".*unlocked", [], 'unlock',
                                     file_path)

  # Make sure it was successfully unlocked again.
  expected_status.tweak(fname, writelocked=None)
  svntest.actions.run_and_verify_status(wc_dir, expected_status)

  # And now the URL case.
  file_url = sbox.repo_url + '/' + fname
  svntest.actions.run_and_verify_svn(None, ".*locked by user", [], 'lock',
                                     '-m', '', file_url)

  # Make sure that the file was locked.
  expected_status.tweak(fname, writelocked='O')
  svntest.actions.run_and_verify_status(wc_dir, expected_status)

  svntest.actions.run_and_verify_svn(None, ".*unlocked", [], 'unlock',
                                     file_url)

  # Make sure it was successfully unlocked again.
  expected_status.tweak(fname, writelocked=None)
  svntest.actions.run_and_verify_status(wc_dir, expected_status)


#----------------------------------------------------------------------
# A regression test for a bug when svn:needs-lock and svn:executable
# interact badly. The bug was fixed in trunk @ r14859.
def lock_and_exebit1(sbox):
  "svn:needs-lock and svn:executable, part I"

  mode_w = stat.S_IWUSR
  mode_x = stat.S_IXUSR
  mode_r = stat.S_IRUSR

  sbox.build()
  wc_dir = sbox.wc_dir

  gamma_path = os.path.join(wc_dir, 'A', 'D', 'gamma')

  expected_err = ".*svn: warning: To turn off the svn:needs-lock property,.*"
  svntest.actions.run_and_verify_svn2(None, None, expected_err, 0,
                                      'ps', 'svn:needs-lock', ' ', gamma_path)

  expected_err = ".*svn: warning: To turn off the svn:executable property,.*"
  svntest.actions.run_and_verify_svn2(None, None, expected_err, 0,
                                      'ps', 'svn:executable', ' ', gamma_path)

  # commit
  svntest.actions.run_and_verify_svn(None, None, [], 'commit',
                                     '-m', '', gamma_path)
  # mode should be +r, -w, +x
  gamma_stat = os.stat(gamma_path)[0]
  if (not gamma_stat & mode_r
      or gamma_stat & mode_w
      or not gamma_stat & mode_x):
    print("Committing a file with 'svn:needs-lock, svn:executable'")
    print("did not set the file to read-only, executable")
    raise svntest.Failure

  # lock
  svntest.actions.run_and_verify_svn(None, ".*locked by user", [], 'lock',
                                     '-m', '', gamma_path)
  # mode should be +r, +w, +x
  gamma_stat = os.stat(gamma_path)[0]
  if (not gamma_stat & mode_r
      or not gamma_stat & mode_w
      or not gamma_stat & mode_x):
    print("Locking a file with 'svn:needs-lock, svn:executable'")
    print("did not set the file to read-write, executable")
    raise svntest.Failure

  # modify
  svntest.main.file_append(gamma_path, "check stat output after mod & unlock")

  # unlock
  svntest.actions.run_and_verify_svn(None, ".*unlocked", [], 'unlock',
                                     gamma_path)

  # Mode should be +r, -w, +x
  gamma_stat = os.stat(gamma_path)[0]
  if (not gamma_stat & mode_r
      or gamma_stat & mode_w
      or not gamma_stat & mode_x):
    print("Unlocking a file with 'svn:needs-lock, svn:executable'")
    print("did not set the file to read-only, executable")
    raise svntest.Failure

  # ci
  svntest.actions.run_and_verify_svn(None, None, [], 'commit',
                                     '-m', '', gamma_path)

  # Mode should be still +r, -w, +x
  gamma_stat = os.stat(gamma_path)[0]
  if (not gamma_stat & mode_r
      or gamma_stat & mode_w
      or not gamma_stat & mode_x):
    print("Commiting a file with 'svn:needs-lock, svn:executable'")
    print("after unlocking modified file's permissions")
    raise svntest.Failure


#----------------------------------------------------------------------
# A variant of lock_and_exebit1: same test without unlock
def lock_and_exebit2(sbox):
  "svn:needs-lock and svn:executable, part II"

  mode_w = stat.S_IWUSR
  mode_x = stat.S_IXUSR
  mode_r = stat.S_IRUSR

  sbox.build()
  wc_dir = sbox.wc_dir

  gamma_path = os.path.join(wc_dir, 'A', 'D', 'gamma')

  expected_err = ".*svn: warning: To turn off the svn:needs-lock property,.*"
  svntest.actions.run_and_verify_svn2(None, None, expected_err, 0,
                                      'ps', 'svn:needs-lock', ' ', gamma_path)

  expected_err = ".*svn: warning: To turn off the svn:executable property,.*"
  svntest.actions.run_and_verify_svn2(None, None, expected_err, 0,
                                     'ps', 'svn:executable', ' ', gamma_path)

  # commit
  svntest.actions.run_and_verify_svn(None, None, [], 'commit',
                                     '-m', '', gamma_path)
  # mode should be +r, -w, +x
  gamma_stat = os.stat(gamma_path)[0]
  if (not gamma_stat & mode_r
      or gamma_stat & mode_w
      or not gamma_stat & mode_x):
    print("Committing a file with 'svn:needs-lock, svn:executable'")
    print("did not set the file to read-only, executable")
    raise svntest.Failure

  # lock
  svntest.actions.run_and_verify_svn(None, ".*locked by user", [], 'lock',
                                     '-m', '', gamma_path)
  # mode should be +r, +w, +x
  gamma_stat = os.stat(gamma_path)[0]
  if (not gamma_stat & mode_r
      or not gamma_stat & mode_w
      or not gamma_stat & mode_x):
    print("Locking a file with 'svn:needs-lock, svn:executable'")
    print("did not set the file to read-write, executable")
    raise svntest.Failure

  # modify
  svntest.main.file_append(gamma_path, "check stat output after mod & unlock")

  # commit
  svntest.actions.run_and_verify_svn(None, None, [], 'commit',
                                     '-m', '', gamma_path)

  # Mode should be +r, -w, +x
  gamma_stat = os.stat(gamma_path)[0]
  if (not gamma_stat & mode_r
      or gamma_stat & mode_w
      or not gamma_stat & mode_x):
    print("Commiting a file with 'svn:needs-lock, svn:executable'")
    print("did not set the file to read-only, executable")
    raise svntest.Failure

def commit_xml_unsafe_file_unlock(sbox):
  "commit file with xml-unsafe name and release lock"

  sbox.build()
  wc_dir = sbox.wc_dir

  fname = 'foo & bar'
  file_path = os.path.join(sbox.wc_dir, fname)
  svntest.main.file_append(file_path, "Initial data.\n")
  svntest.main.run_svn(None, 'add', file_path)
  svntest.main.run_svn(None,
                       'commit', '-m', '', file_path)

  # lock fname as wc_author
  svntest.actions.run_and_verify_svn(None, ".*locked by user", [], 'lock',
                                     '-m', 'some lock comment', file_path)

  # make a change and commit it, allowing lock to be released
  svntest.main.file_append(file_path, "Followup data.\n")
  svntest.main.run_svn(None,
                       'commit', '-m', '', file_path)

  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)
  expected_status.add({ fname : Item(status='  ', wc_rev=3), })

  # Make sure the file is unlocked
  svntest.actions.run_and_verify_status(wc_dir, expected_status)

#----------------------------------------------------------------------
def repos_lock_with_info(sbox):
  "verify info path@X or path -rY return repos lock"

  sbox.build()
  wc_dir = sbox.wc_dir

  fname = 'iota'
  comment = 'This is a lock test.'
  file_path = os.path.join(sbox.wc_dir, fname)
  file_url = sbox.repo_url + '/' + fname

  # lock wc file
  svntest.actions.run_and_verify_svn(None, ".*locked by user", [], 'lock',
                                     '--username', svntest.main.wc_author2,
                                     '-m', comment, file_path)
  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)
  expected_status.tweak(fname, writelocked='K')
  svntest.actions.run_and_verify_status(wc_dir, expected_status)

  # Steal lock on wc file
  svntest.actions.run_and_verify_svn(None, ".*locked by user", [], 'lock',
                                     '--username', svntest.main.wc_author2,
                                     '--force',
                                     '-m', comment, file_url)
  expected_status.tweak(fname, writelocked='T')
  svntest.actions.run_and_verify_status(wc_dir, expected_status)

  # Get repository lock token
  exit_code, output, err = svntest.actions.run_and_verify_svn(None, None, [],
                                                              'info', file_url)
  for line in output:
    if line.find("Lock Token:") != -1:
      repos_lock_token = line[12:]
      break
  else:
    print("Error: Lock token not found")
    raise svntest.Failure

  # info with revision option
  exit_code, output, err = svntest.actions.run_and_verify_svn(None, None, [],
                                                              'info',
                                                              file_path, '-r1')

  for line in output:
    if line.find("Lock Token:") != -1:
      lock_token = line[12:]
      break
  else:
    print("Error: Lock token not found")
    raise svntest.Failure

  if (repos_lock_token != lock_token):
    print("Error: expected repository lock information not found.")
    raise svntest.Failure

  # info with peg revision
  exit_code, output, err = svntest.actions.run_and_verify_svn(None, None, [],
                                                              'info',
                                                              file_path + '@1')
  for line in output:
    if line.find("Lock Token:") != -1:
      lock_token = line[12:]
      break
  else:
    print("Error: Lock token not found")
    raise svntest.Failure

  if (repos_lock_token != lock_token):
    print("Error: expected repository lock information not found.")
    raise svntest.Failure

#----------------------------------------------------------------------
def unlock_already_unlocked_files(sbox):
  "(un)lock set of files, one already (un)locked"

  sbox.build()
  wc_dir = sbox.wc_dir

  # Deliberately have no direct child of A as a target
  iota_path = os.path.join(wc_dir, 'iota')
  lambda_path = os.path.join(wc_dir, 'A', 'B', 'lambda')
  alpha_path = os.path.join(wc_dir, 'A', 'B', 'E', 'alpha')
  gamma_path = os.path.join(wc_dir, 'A', 'D', 'gamma')

  svntest.actions.run_and_verify_svn(None, ".*locked by user", [], 'lock',
                                     '--username', svntest.main.wc_author2,
                                     '-m', 'lock several',
                                     iota_path, lambda_path, alpha_path)

  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)
  expected_status.tweak('iota', 'A/B/lambda', 'A/B/E/alpha', writelocked='K')
  svntest.actions.run_and_verify_status(wc_dir, expected_status)

  error_msg = ".*Path '/A/B/E/alpha' is already locked by user '" + \
              svntest.main.wc_author2 + "'.*"
  svntest.actions.run_and_verify_svn2(None, None, error_msg, 0,
                                      'lock',
                                      '--username', svntest.main.wc_author2,
                                      alpha_path, gamma_path)
  expected_status.tweak('A/D/gamma', writelocked='K')
  svntest.actions.run_and_verify_status(wc_dir, expected_status)

  svntest.actions.run_and_verify_svn(None, ".*unlocked", [], 'unlock',
                                     '--username', svntest.main.wc_author2,
                                     lambda_path)

  expected_status.tweak('A/B/lambda', writelocked=None)
  svntest.actions.run_and_verify_status(wc_dir, expected_status)

  error_msg = "(.*No lock on path '/A/B/lambda'.*)" + \
              "|(.*'A/B/lambda' is not locked.*)"
  svntest.actions.run_and_verify_svn2(None, None, error_msg, 0,
                                      'unlock',
                                      '--username', svntest.main.wc_author2,
                                      '--force',
                                      iota_path, lambda_path, alpha_path)


  expected_status.tweak('iota', 'A/B/E/alpha', writelocked=None)
  svntest.actions.run_and_verify_status(wc_dir, expected_status)

#----------------------------------------------------------------------
def info_moved_path(sbox):
  "show correct lock info on moved path"

  sbox.build()
  wc_dir = sbox.wc_dir
  fname = os.path.join(wc_dir, "iota")
  fname2 = os.path.join(wc_dir, "iota2")

  # Move iota, creating r2.
  svntest.actions.run_and_verify_svn(None, None, [],
                                     "mv", fname, fname2)
  expected_output = svntest.wc.State(wc_dir, {
    'iota2' : Item(verb='Adding'),
    'iota' : Item(verb='Deleting'),
    })
  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)
  expected_status.add({
    "iota2" : Item(status='  ', wc_rev=2)
    })
  expected_status.remove("iota")
  svntest.actions.run_and_verify_commit(wc_dir,
                                        expected_output,
                                        expected_status,
                                        None,
                                        wc_dir)

  # Create a new, unrelated iota, creating r3.
  svntest.main.file_append(fname, "Another iota")
  svntest.actions.run_and_verify_svn(None, None, [],
                                     "add", fname)
  expected_output = svntest.wc.State(wc_dir, {
    'iota' : Item(verb='Adding'),
    })
  expected_status.add({
    "iota" : Item(status='  ', wc_rev=3)
    })
  svntest.actions.run_and_verify_commit(wc_dir,
                                        expected_output,
                                        expected_status,
                                        None,
                                        wc_dir)

  # Lock the new iota.
  svntest.actions.run_and_verify_svn(None, ".*locked by user", [],
                                     "lock", fname)
  expected_status.tweak("iota", writelocked="K")
  svntest.actions.run_and_verify_status(wc_dir, expected_status)

  # Get info for old iota at r1. This shouldn't give us any lock info.
  exit_code, output, errput = svntest.actions.run_and_verify_svn(
    None, None, [], 'info', fname2, '-r1')

  # Since we want to make sure that there is *no* lock info, to make this
  # more robust, we also check that the info command actually output some info.
  got_url = 0
  for line in output:
    if line.find("URL:") >= 0:
      got_url = 1
    if line.find("Lock Token:") >= 0:
      print(fname2 + " was reported as locked.")
      raise svntest.Failure
  if not got_url:
    print("Info didn't output an URL.")
    raise svntest.Failure

#----------------------------------------------------------------------
def ls_url_encoded(sbox):
  "ls locked path needing URL encoding"

  sbox.build()
  wc_dir = sbox.wc_dir
  dirname = os.path.join(wc_dir, "space dir")
  fname = os.path.join(dirname, "f")

  # Create a dir with a space in its name and a file therein.
  svntest.actions.run_and_verify_svn(None, None, [],
                                     "mkdir", dirname)
  svntest.main.file_append(fname, "someone was here")
  svntest.actions.run_and_verify_svn(None, None, [],
                                     "add", fname)
  expected_output = svntest.wc.State(wc_dir, {
    'space dir' : Item(verb='Adding'),
    'space dir/f' : Item(verb='Adding'),
    })
  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)
  expected_status.add({
    "space dir" : Item(status='  ', wc_rev=2),
    "space dir/f" : Item(status='  ', wc_rev=2),
    })
  svntest.actions.run_and_verify_commit(wc_dir,
                                        expected_output,
                                        expected_status,
                                        None,
                                        wc_dir)

  # Lock the file.
  svntest.actions.run_and_verify_svn("Lock space dir/f", ".*locked by user",
                                     [], "lock", fname)

  # Make sure ls shows it being locked.
  expected_output = " +2 " + re.escape(svntest.main.wc_author) + " +O .+f|" \
                    " +2 " + re.escape(svntest.main.wc_author) + "    .+\./"
  svntest.actions.run_and_verify_svn("List space dir",
                                     expected_output, [],
                                     "list", "-v", dirname)

#----------------------------------------------------------------------
# Make sure unlocking a path with the wrong lock token fails.
def unlock_wrong_token(sbox):
  "verify unlocking with wrong lock token"

  sbox.build()
  wc_dir = sbox.wc_dir

  # lock a file as wc_author
  fname = 'iota'
  file_path = os.path.join(sbox.wc_dir, fname)
  file_url = sbox.repo_url + "/iota"

  svntest.actions.run_and_verify_svn(None, ".*locked by user", [], 'lock',
                                     file_path)

  # Steal the lock as the same author, but using an URL to keep the old token
  # in the WC.
  svntest.actions.run_and_verify_svn(None, ".*locked by user", [], 'lock',
                                     "--force", file_url)

  # Then, unlocking the WC path should fail.
  # ### The error message returned is actually this, but let's worry about that
  # ### another day...
  svntest.actions.run_and_verify_svn2(
    None, None, ".*((No lock on path)|(400 Bad Request))", 0,
    'unlock', file_path)

#----------------------------------------------------------------------
# Verify that info shows lock info for locked files with URI-unsafe names
# when run in recursive mode.
def examine_lock_encoded_recurse(sbox):
  "verify recursive info shows lock info"

  sbox.build()
  wc_dir = sbox.wc_dir

  fname = 'A/B/F/one iota'
  file_path = os.path.join(sbox.wc_dir, fname)

  svntest.main.file_append(file_path, "This represents a binary file\n")
  svntest.actions.run_and_verify_svn(None, None, [], "add", file_path)

  expected_output = svntest.wc.State(wc_dir, {
    fname : Item(verb='Adding'),
    })

  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)
  expected_status.add({ fname: Item(wc_rev=2, status='  ') })

  # Commit the file.
  svntest.actions.run_and_verify_commit(wc_dir,
                                        expected_output,
                                        expected_status,
                                        None,
                                        file_path)

  # lock the file and validate the contents
  svntest.actions.run_and_validate_lock(file_path,
                                        svntest.main.wc_author)

# Trying to unlock someone else's lock with --force should fail.
def unlocked_lock_of_other_user(sbox):
  "unlock file locked by other user"

  sbox.build()
  wc_dir = sbox.wc_dir

  # lock a file with user jrandom
  pi_path = os.path.join(wc_dir, 'A', 'D', 'G', 'pi')
  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)
  expected_status.tweak('A/D/G/pi', writelocked='K')

  svntest.actions.run_and_verify_svn(None, ".*locked by user", [], 'lock',
                                     '-m', '', pi_path)

  svntest.actions.run_and_verify_status(wc_dir, expected_status)

  # now try to unlock with user jconstant, should fail but exit 0.
  if sbox.repo_url.startswith("http"):
    expected_err = ".*403 Forbidden.*"
  else:
    expected_err = "svn: warning: User '%s' is trying to use a lock owned by "\
                   "'%s'.*" % (svntest.main.wc_author2, svntest.main.wc_author)
  svntest.actions.run_and_verify_svn2(None, [], expected_err, 0,
                                      'unlock',
                                      '--username', svntest.main.wc_author2,
                                      pi_path)
  svntest.actions.run_and_verify_status(wc_dir, expected_status)


########################################################################
# Run the tests

# list all tests here, starting with None:
test_list = [ None,
              lock_file,
              commit_file_keep_lock,
              commit_file_unlock,
              commit_propchange,
              break_lock,
              steal_lock,
              examine_lock,
              handle_defunct_lock,
              enforce_lock,
              defunct_lock,
              deleted_path_lock,
              lock_unlock,
              deleted_dir_lock,
              lock_status,
              stolen_lock_status,
              broken_lock_status,
              lock_non_existent_file,
              out_of_date,
              update_while_needing_lock,
              revert_lock,
              examine_lock_via_url,
              lock_several_files,
              lock_switched_files,
              lock_uri_encoded,
              SkipUnless(lock_and_exebit1, svntest.main.is_posix_os),
              SkipUnless(lock_and_exebit2, svntest.main.is_posix_os),
              commit_xml_unsafe_file_unlock,
              repos_lock_with_info,
              unlock_already_unlocked_files,
              info_moved_path,
              ls_url_encoded,
              XFail(unlock_wrong_token, svntest.main.is_ra_type_dav),
              examine_lock_encoded_recurse,
              XFail(unlocked_lock_of_other_user,
                    svntest.main.is_ra_type_dav)
            ]

if __name__ == '__main__':
  svntest.main.run_tests(test_list)
  # NOTREACHED


### End of file.
