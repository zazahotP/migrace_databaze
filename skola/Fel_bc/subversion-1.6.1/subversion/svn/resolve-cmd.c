/*
 * resolve-cmd.c -- Subversion resolve subcommand
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

/* ==================================================================== */



/*** Includes. ***/
#define APR_WANT_STDIO
#include <apr_want.h>

#include "svn_client.h"
#include "svn_error.h"
#include "svn_pools.h"
#include "cl.h"

#include "svn_private_config.h"



/*** Code. ***/

/* This implements the `svn_opt_subcommand_t' interface. */
svn_error_t *
svn_cl__resolve(apr_getopt_t *os,
                void *baton,
                apr_pool_t *pool)
{
  svn_cl__opt_state_t *opt_state = ((svn_cl__cmd_baton_t *) baton)->opt_state;
  svn_client_ctx_t *ctx = ((svn_cl__cmd_baton_t *) baton)->ctx;
  svn_wc_conflict_choice_t conflict_choice;
  svn_error_t *err;
  apr_array_header_t *targets;
  int i;
  apr_pool_t *subpool;

  switch (opt_state->accept_which)
    {
    case svn_cl__accept_working:
      conflict_choice = svn_wc_conflict_choose_merged;
      break;
    case svn_cl__accept_base:
      conflict_choice = svn_wc_conflict_choose_base;
      break;
    case svn_cl__accept_theirs_conflict:
      conflict_choice = svn_wc_conflict_choose_theirs_conflict;
      break;
    case svn_cl__accept_mine_conflict:
      conflict_choice = svn_wc_conflict_choose_mine_conflict;
      break;
    case svn_cl__accept_theirs_full:
      conflict_choice = svn_wc_conflict_choose_theirs_full;
      break;
    case svn_cl__accept_mine_full:
      conflict_choice = svn_wc_conflict_choose_mine_full;
      break;
    case svn_cl__accept_unspecified:
      return svn_error_create(SVN_ERR_CL_ARG_PARSING_ERROR, NULL,
                              _("missing --accept option"));
    default:
      return svn_error_create(SVN_ERR_CL_ARG_PARSING_ERROR, NULL,
                              _("invalid 'accept' ARG"));
    }

  SVN_ERR(svn_cl__args_to_target_array_print_reserved(&targets, os,
                                                      opt_state->targets,
                                                      ctx, pool));
  if (! targets->nelts)
    return svn_error_create(SVN_ERR_CL_INSUFFICIENT_ARGS, 0, NULL);

  subpool = svn_pool_create(pool);
  if (! opt_state->quiet)
    svn_cl__get_notifier(&ctx->notify_func2, &ctx->notify_baton2, FALSE,
                         FALSE, FALSE, pool);

  if (opt_state->depth == svn_depth_unknown)
    opt_state->depth = svn_depth_empty;

  for (i = 0; i < targets->nelts; i++)
    {
      const char *target = APR_ARRAY_IDX(targets, i, const char *);
      svn_pool_clear(subpool);
      SVN_ERR(svn_cl__check_cancel(ctx->cancel_baton));
      err = svn_client_resolve(target,
                               opt_state->depth, conflict_choice,
                               ctx,
                               subpool);
      if (err)
        {
          svn_handle_warning2(stderr, err, "svn: ");
          svn_error_clear(err);
        }
    }

  svn_pool_destroy(subpool);
  return SVN_NO_ERROR;
}
