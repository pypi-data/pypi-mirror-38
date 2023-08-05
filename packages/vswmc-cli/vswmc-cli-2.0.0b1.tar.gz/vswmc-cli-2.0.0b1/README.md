# VSWMC Command-Line Interface

The `vswmc` command-line interface is a tool for remote execution via can be installed using pip:

    pip install --upgrade vswmc

This will install a `vswmc` command on your system. The `vswmc` command has a few global options:

`-u USER`

&nbsp;&nbsp;&nbsp; SSA Username

`-p PASSWORD`

&nbsp;&nbsp;&nbsp; SSA Password


## List configurations
    vswmc configurations list


## Delete one or more configurations
    vswmc configurations delete CONFIGURATION ...


## Copy a result file to disk
    vswmc cp SRC DST

Downloads a remote result file to local disk. The source should be specified in the format <tt>RUN:FILE</tt>. The <tt>DST</tt> argument can be a local file or directory.


## Fetch the logs of a run
    vswmc logs RUN


## List the results of a run
    vswmc ls [-l] RUN

OPTIONS
<dl>
<dt><tt>-l</tt></dt>
<dd>Print long listing</dd>
</dl>


## List runs
    vswmc ps [--configuration CONFIGURATION] [-a, --all]

OPTIONS
<dl>
<dt><tt>--configuration CONFIGURATION</tt></dt>
<dd>Filter on configuration.</dd>
<dt><tt>-a, --all</tt></dt>
<dd>List all runs (default shows only ongoing)</dd>
</dl>


## Remove one or more runs
    vswmc rm RUN ...


## Start a run
    vswmc run [--param-file PARAM_FILE] [--param PARAM=VALUE ...] -- CONFIGURATION

OPTIONS
<dl>
<dt><tt>--param-file PARAM_FILE</tt></dt>
<dd>Read parameters from a file.</dd>
<dt><tt>--param PARAM=VALUE ...</tt></dt>
<dd>Set parameters.</dd>
</dl>

Each model supports different parameters.

<table style="width: 100%">
  <tr>
    <td colspan="2" style="border-bottom: 3px double black"><tt>euhforia_corona</tt></td>
  </tr>
  <tr>
    <td><tt>euhforia_corona.magnetogram</tt></td>
    <td>File path to a local magnetogram file</td>
  </tr>
</table>

Example:

    vswmc -u myuser run --param euhforia_corona.magnetogram=/some/magnetogram.tar.gz -- "My configuration"

This commands returns the ID of the new run via stdout. You can use this ID to fetch the log or fetch result files.


<table style="width: 100%">
  <tr>
    <td colspan="2" style="border-bottom: 3px double black"><tt>euhforia_helio</tt></td>
  </tr>
  <tr>
    <td>TODO</td>
    <td></td>
  </tr>
</table>


## Save all results of a run
    vswmc save RUN

Saves all result files of a run. The results of each individual task in this run are compressed and saved into a zip archive named after the model for that task.
