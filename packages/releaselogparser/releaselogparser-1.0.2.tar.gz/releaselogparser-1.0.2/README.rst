Release Log Parser
==================
Software packages usually include textual files describing noteworthy
changes in each subsequent release. There exist several variants (or
formats) of such files.

This package provides Python framework for parsing the most often used
formats of such release log files. Support for any new format can be
easily added.

Release Logs
============
``Release Log`` is a textual file included in a software package, which
contains descriptions of existing releases of the package. Such a
file is normally included in each distributed archive of the package
and is present in its VCS repository.

Little or no effort has been invested into standartization of release
log formats. There exists a plethora of variations which differ more
or less considerably. The choice of a particular variation for a given
package depends mostly on the language this package is written in and
the distribution system adopted for this package. Authors' preferences
play certain role as well.

Despite the diversity of release log formats, similarities between
them overnumber their differences. The following observations hold true:

1. Release logs are plaintext files.
2. Within a file, each release is described by a separate entry.
3. Each such entry consists of a heading, containing at least the
   version number and date of the release, and a textual block discussing
   the changes introduced with this release.
4. Entries are arranged in reverse chronological order, the most
   recent release being described first.
5. Format of the headings is consistent throughout the given release
   log.
6. Entry description is usually a list of changes. However, more
   verbose and general descriptions may also appear within it. In
   general, it is safest to assume the description to be an opaque block
   of arbitrary text.
7. Release logs can contain additional textual information before the
   first release entry (a "prologue") and after the last release entry
   (an "epilogue").

Supported Formats
=================
Most frequently used release log formats can be grouped into three
main families:

``GNU-style`` release logs

  These are normally used by GNU software. Such log files are usually named
  "NEWS". Example heading lines are::

    version 1.30 - Sergey Poznyakoff, 2017-12-17
    Version 1.18 - 2018-08-21
    * Version 4.2, 2014-05-23

``Perl-style`` release logs

  These are the "Changes" files included in each Perl package
  distributed via CPAN. Example heading lines::

    2.00 2018-03-08
    1.01 Sat Jul  7 19:11:35 2018  

``Python package`` release logs

  The "CHANGES.txt" files found in many Python packages. Example heading
  lines:

    v2.0.1, 2014/12/14 -- Update token generator
    2.7 (23 June 2018)

  The special feature of the first heading variant is that the first
  line of the changeset description follows the heading on the same
  physical line. Quite often this is the only line in the description.

Usage
=====
The ``ReleaseLog`` class is a fabric returning actual release history
implementation, depending on the first argument to its constructor.
Typical usage::

      rl = ReleaseLog('GNU', content, count=1)

The two mandatory arguments are the format name and the list of lines
obtained from the release log file.

Valid format names for this version of ``releaselogparser`` are:

``GNU``, ``NEWS``
  GNU-style news file.
``CPAN``, ``Changes``
  Perl-style release log.
``Python``, ``python``
  Python-style release log.

Supported keyword arguments are:

start = *N*
  Start parsing from the entry *N*. Entries are numbered from 0.
stop = *N*
  Stop parsing on the entry *N*.
count = *N*
  Collect at most *N* entries

If all three keywords are given, the actual range of history entries
is computed as

  [start, min(start+count, stop)]

Two derived classes are provided that read input data from various
sources:

class ``ReleaseLogFile``
------------------------
The ``ReleaseLogFile`` class reads release log from the file::

  rl = ReleaseLogFile(fmt, file [, kwargs...])

Here, ``fmt`` is the name of the format, ``file`` is the name of the
input file, and ``kwargs`` are keyword arguments described above.

class ``ReleaseLogURL``
-----------------------
The ``ReleaseLogURL`` class reads log entries from a URL::

  rl = ReleaseLogURL(fmt, url [, kwargs...])

Acessing release information
----------------------------
The returned object can be indexed to obtain particular log
entries. Indices start with 0, which corresponds to the most recent
entry, e.g.:

  entry = cl[0]

The ``entry`` is an object of class ``Release``, which has three
attributes:

``version``
  Release version number.
``date``
  Date and time of the release (a datetime object)
``descr``
  Textual description of the release - a list of lines.

The obtained entry can be printed as string, e.g.:

  print(entry)

The output format is as shown in the example below:

  Version 1.0, released at 2018-08-19 15:30:00

Example
=======
The following simple program reads release log entries from the file
``NEWS`` and prints them on the standard output::

  from releaselogparser.input import ReleaseLogFile

  for log in ReleaseLogFile('GNU', 'NEWS'):
      print(log)
      print('\n'.join(log.descr))

Extending Release Log
=====================
Implementing support for new release log format is fairly easy. To do
so, provide a class inherited from ``ReleaseHistory``. This base class has
the following attributes:

``format``
  List of names for this format. Names from this list can be used
  interchangeably to identify this log format, e.g. as a first
  argument to the ``ReleaseLog`` or derived constructor.
``filename``
  Name of the file used normally for release logs in this format.
``header``
  Compiled regular expression that returns a match for
  history entry heading lines. The expression must contain two named
  groups: ``version``, which returns part of the string corresponding
  to the release version number, and ``date``, returning its
  timestamp.

  If it contains a named group ``rest``, part of the header string
  corresponding to this group will be added to the ``descr`` list of
  the created history entry.

``end_of_entry_rx``
  Compiled regular expression that matches end of entry. Can be
  ``None``, if not needed.

The file with the definition of the inherited class must be placed in
the directory ``releaselogparser/format`` reachable from the Python search path
for module files.

The following example implements a simplified version of CHANGES.txt log
format::

  import re
  from releaselogparser import ReleaseHistory

  class ChangesLogFormat(ReleaseHistory):
      format = ['changes']
      filename = 'CHANGES.txt'
      header = re.compile("""^[vV](?P<version>\d[\d.]*)\s*
                          ,\s*
                          (?P<date>.*?)
                          \s+-+\s*
                          (?P<rest>.*)$
                          """, re.X)

More sophisticated implementations can overload the ``parse_header``
method of the parent class. This method is defined as follows::

  def parse_header(self, line):

If the input ``line`` is an entry header, the method should return
a triplet::

  (date, version, first_line)

where ``date`` is textual representation of the date of the release,
``version`` is the release version string, and ``first_line`` is the
first line of the description (can be None).

If the line is not a valid entry header, the method returns
``(None, None, None)``.


The ``releaselog`` utility
==========================
The ``releaselog`` tool reads release logs in various formats from a
given file or URL. Its usage is::

 releaselog [OPTIONS] FILE-or-URL

The argument is treated as file name by default. To read from a URL,
use the ``--url`` option.

Options:

``-H FORMAT``, ``--format=FORMAT``
  Read logs in the given format.
``-f N``, ``--from=N``, ``--start=N``
  Start from *N* th entry.
``-t N``, ``--to=N``, ``--stop=N``
  End on *N* th entry.
``-n COUNT``, ``--count=COUNT``
  Read at most that much entries.
``-u``, ``--url``
  Treat argument as URL
``-l``, ``--list``
  List supported formats
``--version``
  Show program version number and exit.
``-h``, ``--help``
  Show a short help message and exit.
