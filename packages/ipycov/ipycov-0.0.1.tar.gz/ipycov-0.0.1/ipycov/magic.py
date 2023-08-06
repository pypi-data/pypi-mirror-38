import logging
import os
import shutil

try:
    from coverage import Coverage, CoverageException
    from coverage.cmdline import Opts

    options = Opts()

    coverage_options = [
        getattr(options, option)
        for option in dir(options)
        if hasattr(getattr(options, option), "action")
    ]
except ImportError:
    Coverage, CoverageException, Opts = None, Exception, None
    coverage_options = []

from IPython.display import IFrame
from IPython.core import magic, magic_arguments


@magic.magics_class
class CoverageMagic(magic.Magics):
    """ An IPython Magic class to hold the magic methods. """

    HTML_REPORT_DIR = "htmlcov"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if Coverage is None:
            self.coverage = self.coverage_missing_notice
        # Default execution function used to actually run user code.
        self.default_runner = None

    @staticmethod
    def coverage_missing_notice(*args, **kwargs):
        logging.error("""\
The coverage module could not be found, install it by running
`pip install coverage`. Ignoring: {args} and {kwargs}.\
""".format(args=args, kwargs=kwargs))

    @magic_arguments.magic_arguments(name="coverage")
    @magic_arguments.argument(
        "--branch", "-b", action="store_false",
        help="Measure branch coverage in addition to statement coverage.",
    )
    @magic_arguments.argument(
        "statement", nargs="*",
        help="""Code call statement to include in the code coverage analysis. 
        You can omit this in cell magic mode.""",
    )
    @magic.line_cell_magic
    @magic.needs_local_scope
    def coverage(self, line="", cell=None, local_ns=None):
        """ Run coverage on a line or cell. """

        args = magic_arguments.parse_argstring(self.coverage, line)
        branch = args.branch

        code = "\n".join(args.statement)
        if cell:
            code += "\n" + cell

        if not code:
            return

        global_variables = self.shell.user_ns
        if local_ns is not None:
            conflict_globs = {}
            for var_name, var_val in global_variables.items():
                if var_name in local_ns:
                    conflict_globs[var_name] = var_val
            global_variables.update(local_ns)

        cov = Coverage(branch=branch)
        exception = None
        try:
            cov.start()
            exec(code, global_variables, {})
        except Exception as exc:
            logging.error(exc)
            exception = exc
        finally:
            cov.stop()

        if exception:
            return "Failed to run: \n%s\nBecause: %s" % (code, str(exception))

        cov.save()

        try:
            if os.path.exists(self.HTML_REPORT_DIR):
                shutil.rmtree(self.HTML_REPORT_DIR)
            cov.html_report()
        except CoverageException:
            return "No data to report."

        # TODO: add options for IFrame display
        return IFrame(
            # TODO: figure out why os.path.join messes up static
            self.HTML_REPORT_DIR + "/index.html",
            width="100%",
            height=600,
        )
