"""Unit tests for the dockerfilelint plugin."""

import argparse
import os
import subprocess

import mock
import pytest
from yapsy.PluginManager import PluginManager

import statick_tool
from statick_tool.config import Config
from statick_tool.package import Package
from statick_tool.plugin_context import PluginContext
from statick_tool.plugins.tool.dockerfile_lint_tool_plugin import (
    DockerfileULintToolPlugin,
)
from statick_tool.resources import Resources
from statick_tool.tool_plugin import ToolPlugin


def setup_dockerfilelint_tool_plugin():
    """Initialize and return an instance of the dockerfilelint plugin."""
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--show-tool-output",
        dest="show_tool_output",
        action="store_false",
        help="Show tool output",
    )

    resources = Resources(
        [
            os.path.join(os.path.dirname(statick_tool.__file__), "plugins"),
            os.path.join(os.path.dirname(__file__), "valid_package"),
        ]
    )
    config = Config(resources.get_file("config.yaml"))
    plugin_context = PluginContext(arg_parser.parse_args([]), resources, config)
    plugin = DockerfileULintToolPlugin()
    plugin.set_plugin_context(plugin_context)
    return plugin


def test_dockerfilelint_tool_plugin_found():
    """Test that the plugin manager can find the dockerfilelint plugin."""
    manager = PluginManager()
    # Get the path to statick_tool/__init__.py, get the directory part, and
    # add 'plugins' to that to get the standard plugins dir
    manager.setPluginPlaces(
        [os.path.join(os.path.dirname(statick_tool.__file__), "plugins")]
    )
    manager.setCategoriesFilter(
        {
            "Tool": ToolPlugin,
        }
    )
    manager.collectPlugins()
    # Verify that a plugin's get_name() function returns "dockerfilelint"
    assert any(
        plugin_info.plugin_object.get_name() == "dockerfile-lint"
        for plugin_info in manager.getPluginsOfCategory("Tool")
    )
    # While we're at it, verify that a plugin is named dockerfilelint Tool Plugin
    assert any(
        plugin_info.name == "Dockerfile Lint Tool Plugin"
        for plugin_info in manager.getPluginsOfCategory("Tool")
    )


def test_dockerfilelint_tool_plugin_scan_valid():
    """Integration test: Make sure the dockerfilelint output hasn't changed."""
    plugin = setup_dockerfilelint_tool_plugin()
    if not plugin.command_exists("dockerfile_lint"):
        pytest.skip("Missing dockerfile_lint executable.")
    package = Package(
        "valid_package", os.path.join(os.path.dirname(__file__), "valid_package")
    )
    package["dockerfile_src"] = [
        os.path.join(os.path.dirname(__file__), "valid_package", "Dockerfile.noissues")
    ]
    issues = plugin.scan(package, "level")
    assert not issues


def test_dockerfilelint_tool_plugin_scan_valid_with_issues():
    """Integration test: Make sure the dockerfilelint output hasn't changed."""
    plugin = setup_dockerfilelint_tool_plugin()
    if not plugin.command_exists("dockerfile_lint"):
        pytest.skip("Missing dockerfile_lint executable.")
    package = Package(
        "valid_package", os.path.join(os.path.dirname(__file__), "valid_package")
    )
    package["dockerfile_src"] = [
        os.path.join(os.path.dirname(__file__), "valid_package", "Dockerfile")
    ]
    issues = plugin.scan(package, "level")
    # We expect a base image latest tag, one expose command missing, one invalid parameters, and two required label not defined issues
    assert len(issues) == 5


def test_dockerfilelint_tool_plugin_parse_valid():
    """Verify that we can parse the expected output of dockerfilelint."""
    plugin = setup_dockerfilelint_tool_plugin()
    output = '{"error":{"count":1,"data":[{"label":"is_latest_tag","level":"error","message":"base image uses \'latest\' tag","description":"using the \'latest\' tag may cause unpredictable builds. It is recommended that a specific tag is used in the FROM line or *-released which is the latest supported release.","reference_url":["https://docs.docker.com/engine/reference/builder/","#from"],"lineContent":"FROM scratch:latest","line":1}]},"warn":{"count":0,"data":[]},"info":{"count":0,"data":[]},"summary":[],"filename":"Dockerfile"}'
    issues = plugin.parse_output([output])
    assert len(issues) == 1
    assert issues[0].filename == "Dockerfile"
    assert issues[0].line_number == "1"
    assert issues[0].tool == "dockerfile-lint"
    assert issues[0].issue_type == "is_latest_tag"
    assert issues[0].severity == "5"
    assert (
        issues[0].message
        == "base image uses 'latest' tag: using the 'latest' tag may cause unpredictable builds. It is recommended that a specific tag is used in the FROM line or *-released which is the latest supported release."
    )


def test_dockerfilelint_tool_plugin_parse_invalid():
    """Verify that invalid output of dockerfilelint is ignored."""
    plugin = setup_dockerfilelint_tool_plugin()
    output = "invalid text"
    issues = plugin.parse_output(output)
    assert not issues


@mock.patch(
    "statick_tool.plugins.tool.dockerfilelint_tool_plugin.subprocess.check_output"
)
def test_dockerfilelint_tool_plugin_scan_calledprocesserror(
    mock_subprocess_check_output,
):
    """
    Test what happens when a CalledProcessError is raised (usually means dockerfilelint hit an error).

    Expected result: issues is None
    """
    mock_subprocess_check_output.side_effect = subprocess.CalledProcessError(
        0, "", output="mocked error"
    )
    plugin = setup_dockerfilelint_tool_plugin()
    package = Package(
        "valid_package", os.path.join(os.path.dirname(__file__), "valid_package")
    )
    package["dockerfile_src"] = [
        os.path.join(os.path.dirname(__file__), "valid_package", "Dockerfile")
    ]
    issues = plugin.scan(package, "level")
    assert issues is None

    mock_subprocess_check_output.side_effect = subprocess.CalledProcessError(
        2, "", output="mocked error"
    )
    issues = plugin.scan(package, "level")
    assert not issues


@mock.patch(
    "statick_tool.plugins.tool.dockerfilelint_tool_plugin.subprocess.check_output"
)
def test_dockerfilelint_tool_plugin_scan_oserror(mock_subprocess_check_output):
    """
    Test what happens when an OSError is raised (usually means dockerfilelint doesn't exist).

    Expected result: issues is None
    """
    mock_subprocess_check_output.side_effect = OSError("mocked error")
    plugin = setup_dockerfilelint_tool_plugin()
    package = Package(
        "valid_package", os.path.join(os.path.dirname(__file__), "valid_package")
    )
    package["dockerfile_src"] = [
        os.path.join(os.path.dirname(__file__), "valid_package", "Dockerfile")
    ]
    issues = plugin.scan(package, "level")
    assert issues is None
