#
# copyright (c) 2018 east301
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php
#

import os

import click

from .benchmark import benchmark
from .loading import WorkflowLoader, load_global_config


# ================================================================================
# commands
# ================================================================================

@click.command(help='Runs a workflow')
@click.argument('runfile', type=click.Path(exists=True))
@click.option('-d', '--dry-run', is_flag=True)
@benchmark('Total execution time')
def run(runfile, dry_run):
    executor = _create_executor_from_runfile(runfile)
    executor.submit(dry_run=dry_run)


@click.command(help='Shows task status')
@click.argument('runfile', type=click.Path(exists=True))
@benchmark('Total execution time')
def status(runfile):
    executor = _create_executor_from_runfile(runfile)
    executor.status()


@click.command(help='Cancels execution of tasks')
@click.argument('runfile', type=click.Path(exists=True))
@click.option('-f', '--force', is_flag=True)
@benchmark('Total execution time')
def cancel(runfile, force):
    executor = _create_executor_from_runfile(runfile)
    executor.cancel(force=force)


# ================================================================================
# helpers
# ================================================================================

def _create_workflow_from_funfile(runfile):
    global_config = load_global_config()
    return WorkflowLoader(global_config).load(runfile)


def _create_executor_from_runfile(runfile):
    global_config = load_global_config()
    workflow = WorkflowLoader(global_config).load(os.path.normpath(os.path.abspath(runfile)))
    return workflow.runfile.gpipe.executor_class(global_config, workflow)
