/***********************************************************
Copyright 1991-1995 by Stichting Mathematisch Centrum, Amsterdam,
The Netherlands.

                        All Rights Reserved

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee is hereby granted,
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in
supporting documentation, and that the names of Stichting Mathematisch
Centrum or CWI or Corporation for National Research Initiatives or
CNRI not be used in advertising or publicity pertaining to
distribution of the software without specific, written prior
permission.

While CWI is the initial source for this software, a modified version
is made available by the Corporation for National Research Initiatives
(CNRI) at the Internet address ftp://ftp.python.org.

STICHTING MATHEMATISCH CENTRUM AND CNRI DISCLAIM ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL STICHTING MATHEMATISCH
CENTRUM OR CNRI BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR
PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.

******************************************************************/

/* Return the initial module search path. */
/* Used by DOS, OS/2, Windows 3.1.  Works on NT too. */

#include "Python.h"
#include "osdefs.h"

#include <sys/types.h>
#include <sys/stat.h>
#include <string.h>

#if HAVE_UNISTD_H
#include <unistd.h>
#endif /* HAVE_UNISTD_H */

/* Search in some common locations for the associated Python libraries.
 *
 * This version always returns "" for both prefix and exec_prefix.
 *
 * Py_GetPath() tries to return a sensible Python module search path.
 *
 * First, we look to see if the executable is in a subdirectory of
 * the Python build directory.  We calculate the full path of the
 * directory containing the executable as progpath.  We work backwards
 * along progpath and look for $dir/Modules/Setup.in, a distinctive
 * landmark.  If found, we use $dir/Lib as $root.  The returned
 * Python path is the compiled #define PYTHONPATH with all the initial
 * "./lib" replaced by $root.
 *
 * Otherwise, if there is a PYTHONPATH environment variable, we return that.
 *
 * Otherwise we try to find $progpath/lib/string.py, and if found, then
 * root is $progpath/lib, and we return Python path as compiled PYTHONPATH
 * with all "./lib" replaced by $root (as above).
 *
 */

#ifndef LANDMARK
#define LANDMARK "Modules\\Setup.in"
#endif

static char prefix[MAXPATHLEN+1];
static char progpath[MAXPATHLEN+1];
static char *module_search_path = NULL;

static int
is_sep(ch)	/* determine if "ch" is a separator character */
	char ch;
{
#ifdef ALTSEP
	return ch == SEP || ch == ALTSEP;
#else
	return ch == SEP;
#endif
}

static void
reduce(dir)
	char *dir;
{
	int i = strlen(dir);
	while (i > 0 && !is_sep(dir[i]))
		--i;
	dir[i] = '\0';
}
	

static int
exists(filename)
	char *filename;
{
	struct stat buf;
	return stat(filename, &buf) == 0;
}


static void
join(buffer, stuff)
	char *buffer;
	char *stuff;
{
	int n, k;
	if (is_sep(stuff[0]))
		n = 0;
	else {
		n = strlen(buffer);
		if (n > 0 && !is_sep(buffer[n-1]) && n < MAXPATHLEN)
			buffer[n++] = SEP;
	}
	k = strlen(stuff);
	if (n + k > MAXPATHLEN)
		k = MAXPATHLEN - n;
	strncpy(buffer+n, stuff, k);
	buffer[n+k] = '\0';
}


static int
search_for_prefix(argv0_path, landmark)
	char *argv0_path;
	char *landmark;
{
	int n;

	/* Search from argv0_path, until root is found */
	strcpy(prefix, argv0_path);
	do {
		n = strlen(prefix);
		join(prefix, landmark);
		if (exists(prefix))
			return 1;
		prefix[n] = '\0';
		reduce(prefix);
	} while (prefix[0]);
	return 0;
}

static void
get_progpath()
{
#ifdef MS_WIN32
#include <windows.h>
	if (!GetModuleFileName(NULL, progpath, MAXPATHLEN))
		progpath[0] = '\0';	/* failure */
#else
	extern char *Py_GetProgramName();
	char *path = getenv("PATH");
	char *prog = Py_GetProgramName();

	/* If there is no slash in the argv0 path, then we have to
	 * assume python is on the user's $PATH, since there's no
	 * other way to find a directory to start the search from.  If
	 * $PATH isn't exported, you lose.
	 */
#ifdef ALTSEP
	if (strchr(prog, SEP) || strchr(prog, ALTSEP))
#else
	if (strchr(prog, SEP))
#endif
		strcpy(progpath, prog);
	else if (path) {
		while (1) {
			char *delim = strchr(path, DELIM);

			if (delim) {
				int len = delim - path;
				strncpy(progpath, path, len);
				*(progpath + len) = '\0';
			}
			else
				strcpy(progpath, path);

			join(progpath, prog);
			if (exists(progpath))
				break;

			if (!delim) {
				progpath[0] = '\0';
				break;
			}
			path = delim + 1;
		}
	}
	else
		progpath[0] = '\0';
#endif
}

static void
calculate_path()
{
	char ch, *pt, *pt2;
	char argv0_path[MAXPATHLEN+1];
	char *buf;
	int bufsz;

	get_progpath();
	strcpy(argv0_path, progpath);
	reduce(argv0_path);

	if (search_for_prefix(argv0_path, LANDMARK)) {
		reduce(prefix);
		reduce(prefix);
		join(prefix, "lib");
	}
	else if ((module_search_path = getenv("PYTHONPATH")) != 0) {
		return;	/* if PYTHONPATH environment variable exists, we are done */
	}
	else {	/* Try the executable_directory/lib */
		strcpy(prefix, progpath);
		reduce(prefix);
		join(prefix, "lib");
		join(prefix, "string.py");	/* Look for lib/string.py */
		if (exists(prefix)) {
			reduce(prefix);
		}
		else {	/* No module search path!!! */
			module_search_path = PYTHONPATH;
			return;
		}
	}
	

	/* If we get here, we need to return a path equal to the compiled
	   PYTHONPATH with ".\lib" replaced by our "prefix" directory */

	bufsz = 1;	/* Calculate size of return buffer.  */
	for (pt = PYTHONPATH; *pt; pt++)
		if (*pt == DELIM)
			bufsz++;	/* number of DELIM plus one */
	bufsz *= strlen(PYTHONPATH) + strlen(prefix);  /* high estimate */

	module_search_path = buf = malloc(bufsz);

	if (buf == NULL) {
		/* We can't exit, so print a warning and limp along */
		fprintf(stderr, "Not enough memory for dynamic PYTHONPATH.\n");
		fprintf(stderr, "Using default static PYTHONPATH.\n");
		module_search_path = PYTHONPATH;
		return;
	}
	for (pt = PYTHONPATH; *pt; pt++) {
		if (!strncmp(pt, ".\\lib", 5) &&
			((ch = *(pt + 5)) == '\\' || ch == DELIM || !ch)){
			pt += 4;
			for (pt2 = prefix; *pt2; pt2++)
				*buf++ = *pt2;
		}
		else
			*buf++ = *pt;
	}
	*buf = '\0';
}


/* External interface */

char *
Py_GetPath()
{
	if (!module_search_path)
		calculate_path();
	return module_search_path;
}

char *
Py_GetPrefix()
{
	return "";
}

char *
Py_GetExecPrefix()
{
	return "";
}

char *
Py_GetProgramFullPath()	/* Full path to Python executable */
{
	if (!module_search_path)
		calculate_path();
	return progpath;
}
