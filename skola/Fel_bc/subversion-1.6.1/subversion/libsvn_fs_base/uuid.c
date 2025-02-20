/* uuid.c : operations on repository uuids
 *
 * ====================================================================
 * Copyright (c) 2000-2004 CollabNet.  All rights reserved.
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

#include "fs.h"
#include "trail.h"
#include "err.h"
#include "uuid.h"
#include "bdb/uuids-table.h"
#include "../libsvn_fs/fs-loader.h"

#include "private/svn_fs_util.h"


struct get_uuid_args
{
  int idx;
  const char **uuid;
};


static svn_error_t *
txn_body_get_uuid(void *baton, trail_t *trail)
{
  struct get_uuid_args *args = baton;
  return svn_fs_bdb__get_uuid(trail->fs, args->idx, args->uuid,
                              trail, trail->pool);
}


svn_error_t *
svn_fs_base__get_uuid(svn_fs_t *fs,
                      const char **uuid,
                      apr_pool_t *pool)
{
  base_fs_data_t *bfd = fs->fsap_data;

  SVN_ERR(svn_fs__check_fs(fs, TRUE));

  /* Check for a cached UUID first.  Failing that, we hit the
     database. */
  if (bfd->uuid)
    {
      *uuid = apr_pstrdup(pool, bfd->uuid);
    }
  else
    {
      struct get_uuid_args args;
      args.idx = 1;
      args.uuid = uuid;
      SVN_ERR(svn_fs_base__retry_txn(fs, txn_body_get_uuid, &args, pool));

      /* Toss what we find into the cache. */
      if (*uuid)
        bfd->uuid = apr_pstrdup(fs->pool, *uuid);
    }

  return SVN_NO_ERROR;
}


struct set_uuid_args
{
  int idx;
  const char *uuid;
};


static svn_error_t *
txn_body_set_uuid(void *baton, trail_t *trail)
{
  struct set_uuid_args *args = baton;
  return svn_fs_bdb__set_uuid(trail->fs, args->idx, args->uuid,
                              trail, trail->pool);
}


svn_error_t *
svn_fs_base__set_uuid(svn_fs_t *fs,
                      const char *uuid,
                      apr_pool_t *pool)
{
  struct set_uuid_args args;
  base_fs_data_t *bfd = fs->fsap_data;

  SVN_ERR(svn_fs__check_fs(fs, TRUE));

  if (! uuid)
    uuid = svn_uuid_generate(pool);

  args.idx = 1;
  args.uuid = uuid;
  SVN_ERR(svn_fs_base__retry_txn(fs, txn_body_set_uuid, &args, pool));

  /* Toss our value into the cache. */
  if (uuid)
    bfd->uuid = apr_pstrdup(fs->pool, uuid);

  return SVN_NO_ERROR;
}

