dnl
dnl find_apu.m4 : locate the APR-util (APU) include files and libraries
dnl
dnl This macro file can be used by applications to find and use the APU
dnl library. It provides a standardized mechanism for using APU. It supports
dnl embedding APU into the application source, or locating an installed
dnl copy of APU.
dnl
dnl APR_FIND_APU(srcdir, builddir, implicit-install-check, acceptable-majors)
dnl
dnl   where srcdir is the location of the bundled APU source directory, or
dnl   empty if source is not bundled.
dnl
dnl   where builddir is the location where the bundled APU will be built,
dnl   or empty if the build will occur in the srcdir.
dnl
dnl   where implicit-install-check set to 1 indicates if there is no
dnl   --with-apr-util option specified, we will look for installed copies.
dnl
dnl   where acceptable-majors is a space separated list of acceptable major
dnl   version numbers. Often only a single major version will be acceptable.
dnl   If multiple versions are specified, and --with-apr-util=PREFIX or the
dnl   implicit installed search are used, then the first (leftmost) version
dnl   in the list that is found will be used.  Currently defaults to [0 1].
dnl
dnl Sets the following variables on exit:
dnl
dnl   apu_found : "yes", "no", "reconfig"
dnl
dnl   apu_config : If the apu-config tool exists, this refers to it.  If
dnl                apu_found is "reconfig", then the bundled directory
dnl                should be reconfigured *before* using apu_config.
dnl
dnl Note: this macro file assumes that apr-config has been installed; it
dnl       is normally considered a required part of an APR installation.
dnl
dnl Note: At this time, we cannot find *both* a source dir and a build dir.
dnl       If both are available, the build directory should be passed to
dnl       the --with-apr-util switch.
dnl
dnl Note: the installation layout is presumed to follow the standard
dnl       PREFIX/lib and PREFIX/include pattern. If the APU config file
dnl       is available (and can be found), then non-standard layouts are
dnl       possible, since it will be described in the config file.
dnl
dnl If a bundled source directory is available and needs to be (re)configured,
dnl then apu_found is set to "reconfig". The caller should reconfigure the
dnl (passed-in) source directory, placing the result in the build directory,
dnl as appropriate.
dnl
dnl If apu_found is "yes" or "reconfig", then the caller should use the
dnl value of apu_config to fetch any necessary build/link information.
dnl

AC_DEFUN([APR_FIND_APU], [
  apu_found="no"

  if test "$ac_cv_emxos2" = "yes"; then
    # Scripts don't pass test -x on OS/2
    TEST_X="test -f"
  else
    TEST_X="test -x"
  fi

  ifelse([$4], [],
  [
    ifdef(AC_WARNING,([$0: missing argument 4 (acceptable-majors): Defaulting to APU 0.x then APU 1.x]))
    acceptable_majors="0 1"
  ], [acceptable_majors="$4"])

  apu_temp_acceptable_apu_config=""
  for apu_temp_major in $acceptable_majors
  do
    case $apu_temp_major in
      0)
      apu_temp_acceptable_apu_config="$apu_temp_acceptable_apu_config apu-config"
      ;;
      *)
      apu_temp_acceptable_apu_config="$apu_temp_acceptable_apu_config apu-$apu_temp_major-config"
      ;;
    esac
  done

  AC_MSG_CHECKING(for APR-util)
  AC_ARG_WITH(apr-util,
  [  --with-apr-util=PATH    prefix for installed APU, path to APU build tree,
                          or the full path to apu-config],
  [
    if test "$withval" = "no" || test "$withval" = "yes"; then
      AC_MSG_ERROR([--with-apr-util requires a directory or file to be provided])
    fi

    for apu_temp_apu_config_file in $apu_temp_acceptable_apu_config
    do
      for lookdir in "$withval/bin" "$withval"
      do
        if $TEST_X "$lookdir/$apu_temp_apu_config_file"; then
          apu_found="yes"
          apu_config="$lookdir/$apu_temp_apu_config_file"
          break 2
        fi
      done
    done

    if test "$apu_found" != "yes" && $TEST_X "$withval" && $withval --help > /dev/null 2>&1 ; then
      apu_found="yes"
      apu_config="$withval"
    fi

    dnl if --with-apr-util is used, it is a fatal error for its argument
    dnl to be invalid
    if test "$apu_found" != "yes"; then
      AC_MSG_ERROR([the --with-apr-util parameter is incorrect. It must specify an install prefix, a build directory, or an apu-config file.])
    fi
  ],[
    dnl if we have a bundled source directory, use it
    if test -d "$1"; then
      apu_temp_abs_srcdir="`cd $1 && pwd`"
      apu_found="reconfig"
      apu_bundled_major="`sed -n '/#define.*APU_MAJOR_VERSION/s/^[^0-9]*\([0-9]*\).*$/\1/p' \"$1/include/apu_version.h\"`"
      case $apu_bundled_major in
        "")
          AC_MSG_ERROR([failed to find major version of bundled APU])
        ;;
        0)
          apu_temp_apu_config_file="apu-config"
        ;;
        *)
          apu_temp_apu_config_file="apu-$apu_bundled_major-config"
        ;;
      esac
      if test -n "$2"; then
        apu_config="$2/$apu_temp_apu_config_file"
      else
        apu_config="$1/$apu_temp_apu_config_file"
      fi
    fi
    if test "$apu_found" = "no" && test -n "$3" && test "$3" = "1"; then
      for apu_temp_apu_config_file in $apu_temp_acceptable_apu_config
      do
        if $apu_temp_apu_config_file --help > /dev/null 2>&1 ; then
          apu_found="yes"
          apu_config="$apu_temp_apu_config_file"
          break
        else
          dnl look in some standard places (apparently not in builtin/default)
          for lookdir in /usr /usr/local /opt/apr /usr/local/apache2 ; do
            if $TEST_X "$lookdir/bin/$apu_temp_apu_config_file"; then
              apu_found="yes"
              apu_config="$lookdir/bin/$apu_temp_apu_config_file"
              break 2
            fi
          done
        fi
      done
    fi
  ])

  AC_MSG_RESULT($apu_found)
])
