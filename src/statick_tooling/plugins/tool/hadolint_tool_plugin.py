"""Apply hadolint tool and gather results."""

import argparse
import json
import logging
import subprocess
from typing import List, Optional

from statick_tool.issue import Issue
from statick_tool.package import Package
from statick_tool.tool_plugin import ToolPlugin


class HadolintToolPlugin(ToolPlugin):  # type: ignore
    """Apply hadolint tool and gather results."""

    def get_name(self) -> str:
        """Get name of tool."""
        return "hadolint"

    def gather_args(self, args: argparse.Namespace) -> None:
        """Gather arguments."""
        args.add_argument(
            "--hadolint-bin",
            dest="hadolint_bin",
            type=str,
            help="hadolint binary path",
        )

    # pylint: disable=too-many-locals
    def scan(self, package: Package, level: str) -> Optional[List[Issue]]:
        """Run tool and gather output."""
        tool_bin = "hadolint"

        # If the user explicitly specifies a binary, let that override the user_version
        if (
            self.plugin_context
            and self.plugin_context.args.hadolint_bin is not None
        ):
            tool_bin = self.plugin_context.args.hadolint_bin

        tool_config = ".hadolint.yaml"
        user_config = self.plugin_context.config.get_tool_config(
            self.get_name(), level, "config"
        )
        if user_config is not None:
            tool_config = user_config

        format_file_name = self.plugin_context.resources.get_file(tool_config)
        flags: List[str] = []
        if format_file_name is not None:
            flags += ["-c", format_file_name]
        flags += ["-f", "json", "--no-fail"]
        user_flags = self.get_user_flags(level)
        flags += user_flags

        files: List[str] = []
        if "dockerfile_src" in package:
            files += package["dockerfile_src"]

        total_output: List[str] = []

        try:
            exe = [tool_bin] + flags
            exe.extend(files)
            output = subprocess.check_output(
                exe, stderr=subprocess.STDOUT, universal_newlines=True
            )
            total_output.append(output)

        except subprocess.CalledProcessError as ex:
            logging.warning(
                "%s failed! Returncode = %d", tool_bin, ex.returncode
            )
            logging.warning("%s exception: %s", self.get_name(), ex.output)
            return None

        except OSError as ex:
            logging.warning("Couldn't find %s! (%s)", tool_bin, ex)
            return None

        for output in total_output:
            logging.debug("%s", output)

        with open(self.get_name() + ".log", "w") as fid:
            for output in total_output:
                fid.write(output)

        issues: List[Issue] = self.parse_output(total_output)
        return issues

    # pylint: enable=too-many-locals

    def parse_output(self, total_output: List[str]) -> List[Issue]:
        """Parse tool output and report issues."""
        issues: List[Issue] = []

        # pylint: disable=too-many-nested-blocks
        for output in total_output:
            for line in output.split("\n"):
                if line:
                    try:
                        err_arr = json.loads(line)
                        for issue in err_arr:
                            severity_str = issue["level"]
                            severity = "1"
                            if severity_str == "style":
                                severity = "1"
                            elif severity_str == "info":
                                severity = "1"
                            elif severity_str == "warning":
                                severity = "3"
                            elif severity_str == "error":
                                severity = "5"
                            issues.append(
                                Issue(
                                    issue["file"],
                                    str(issue["line"]),
                                    self.get_name(),
                                    issue["code"],
                                    severity,
                                    issue["message"],
                                    None,
                                )
                            )

                    except ValueError as ex:
                        logging.warning("ValueError: %s, line: %s", ex, line)
        # pylint: enable=too-many-nested-blocks
        return issues
