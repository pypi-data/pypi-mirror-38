# -*- coding: utf-8 -*-

"""
"law run" cli subprogram.
"""


import os
import sys
import logging

from luigi.cmdline import luigi_run

from law.task.base import Task
from law.config import Config
from law.util import abort


logger = logging.getLogger(__name__)


def setup_parser(sub_parsers):
    """
    Sets up the command line parser for the *run* subprogram and adds it to *sub_parsers*.
    """
    parser = sub_parsers.add_parser("run", prog="law run", description="Run a task with"
        " configurable parameters. See http://luigi.rtfd.io/en/stable/running_luigi.html for more"
        " info.")

    parser.add_argument("task_family", help="a task family registered in the task database file or"
        " a module and task class in the format <module>.<class>")
    parser.add_argument("parameter", nargs="*", help="task parameters")


def execute(args):
    """
    Executes the *run* subprogram with parsed commandline *args*.
    """
    task_family = None
    error = None

    # try to infer the task module from the passed task family and import it
    parts = args.task_family.rsplit(".", 1)
    if len(parts) == 2:
        modid, cls_name = parts
        try:
            mod = __import__(modid, globals(), locals(), [cls_name])
            if hasattr(mod, cls_name):
                task_cls = getattr(mod, cls_name)
                if not issubclass(task_cls, Task):
                    abort("object '{}' is not a Task".format(args.task_family))
                task_family = task_cls.task_family
        except ImportError as e:
            logger.debug("import error in module {}: {}".format(modid, e))
            error = e

    # read task info from the db file and import it
    if task_family is None:
        db_file = Config.instance().get_expanded("core", "db_file")
        if os.path.exists(db_file):
            info = read_task_from_db(args.task_family, db_file)
            if not info:
                abort("task family '{}' not found in db".format(args.task_family))
            modid, task_family, _ = info
            __import__(modid, globals(), locals())

    # complain when no task could be found
    if task_family is None:
        if error:
            raise error
        else:
            abort("task '{}' not found".format(args.task_family))

    # import the module and run luigi
    luigi_run([task_family] + sys.argv[3:])


def read_task_from_db(task_family, db_file=None):
    """
    Returns module id, task family and space-separated parameters in a tuple for a task given by
    *task_family* from the *db_file*. When *None*, the *db_file* refers to the default as defined in
    :py:mod:`law.config`. Returns *None* when the task could not be found.
    """
    # read task information from the db file given a task family
    if db_file is None:
        db_file = Config.instance().get_expanded("core", "db_file")

    # open and go through lines
    with open(db_file, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line.count(":") >= 2:
                modid, family, params = line.split(":", 2)
                if family == task_family:
                    return modid, family, params

    return None
