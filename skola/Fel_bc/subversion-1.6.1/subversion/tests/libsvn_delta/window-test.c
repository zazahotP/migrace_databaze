/*
 * window-test.c:  Test delta window generation
 *
 * ====================================================================
 * Copyright (c) 2008 CollabNet.  All rights reserved.
 *
 * This software is licensed as described in the file COPYING, which
 * you should have received as part of this distribution.  The terms
 * are also available at http://subversion.tigris.org/license-1.html.
 * If newer versions of this license are posted there, you may use a
 * newer version instead, at your option.
 *
 * This software consists of voluntary contributions made by many
 * individuals.  For exact contribution history, see the revision
 * history and logs, available at http://subversion.tigris.org/.
 * ====================================================================
 */

#include <apr_pools.h>

#include "../svn_test.h"

#include "svn_types.h"
#include "svn_error.h"
#include "svn_delta.h"


static svn_error_t *
stream_window_test(const char **msg,
                   svn_boolean_t msg_only,
                   svn_test_opts_t *opts,
                   apr_pool_t *pool)
{
  /* Note: put these in data segment, not the stack */
  static char source[109001];
  static char target[109001];
  int i;
  char *p = &source[9];
  svn_checksum_t *expected;
  svn_checksum_t *actual;
  svn_string_t source_str;
  svn_string_t target_str;
  svn_stream_t *source_stream;
  svn_stream_t *target_stream;
  svn_txdelta_stream_t *txstream;

  *msg = "txdelta stream and windows test";
  if (msg_only)
    return SVN_NO_ERROR;

  memcpy(source, "a\nb\nc\nd\ne", 9);
  for (i = 100; i--; )
    *p++ = '\n';
  for (i = 999; i--; p += 109)
    memcpy(p, source, 109);
  source[109000] = '\0';

  memcpy(target, source, 109001);
  for (i = 1000; i--; )
    target[i*109 + 4] = 'X';

  SVN_ERR(svn_checksum(&expected, svn_checksum_md5, target, 109000, pool));
  /* f6fd44565e14c6e44b35292719deb77e */
  printf("expected: %s\n", svn_checksum_to_cstring(expected, pool));

  source_str.data = source;
  source_str.len = 109000;
  source_stream = svn_stream_from_string(&source_str, pool);

  target_str.data = target;
  target_str.len = 109000;
  target_stream = svn_stream_from_string(&target_str, pool);

  svn_txdelta(&txstream, source_stream, target_stream, pool);

  while (1)
    {
      svn_txdelta_window_t *window;

      SVN_ERR(svn_txdelta_next_window(&window, txstream, pool));
      if (window == NULL)
        break;

      /* ### examine the window */
    }

  actual = svn_checksum__from_digest(svn_txdelta_md5_digest(txstream),
                                     svn_checksum_md5, pool);;
  printf("  actual: %s\n", svn_checksum_to_cstring(actual, pool));

  if (!svn_checksum_match(expected, actual))
    {
      return svn_error_create(SVN_ERR_TEST_FAILED, NULL,
                              "Checksums did not match.");
    }

  return SVN_NO_ERROR;
}



/* The test table.  */

struct svn_test_descriptor_t test_funcs[] =
  {
    SVN_TEST_NULL,
    SVN_TEST_PASS(stream_window_test),
    SVN_TEST_NULL
  };
