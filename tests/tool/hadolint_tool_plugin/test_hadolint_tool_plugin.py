"""Unit tests for the hadolint plugin."""

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
from statick_tool.plugins.tool.hadolint_tool_plugin import HadolintToolPlugin
from statick_tool.resources import Resources
from statick_tool.tool_plugin import ToolPlugin


def setup_hadolint_tool_plugin(binary=None):
    """Initialize and return an instance of the hadolint plugin."""
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--hadolint-bin", dest="hadolint_bin")

    resources = Resources(
        [
            os.path.join(os.path.dirname(statick_tool.__file__), "plugins"),
            os.path.join(os.path.dirname(__file__), "valid_package"),
        ]
    )
    config = Config(resources.get_file("config.yaml"))
    plugin_context = PluginContext(arg_parser.parse_args([]), resources, config)
    plugin = HadolintToolPlugin()
    if binary:
        plugin_context.args.hadolint_bin = binary
    plugin.set_plugin_context(plugin_context)
    return plugin


def test_hadolint_tool_plugin_found():
    """Test that the plugin manager can find the hadolint plugin."""
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
    # Verify that a plugin's get_name() function returns "hadolint"
    assert any(
        plugin_info.plugin_object.get_name() == "hadolint"
        for plugin_info in manager.getPluginsOfCategory("Tool")
    )
    # While we're at it, verify that a plugin is named hadolint Tool Plugin
    assert any(
        plugin_info.name == "Hadolint Tool Plugin"
        for plugin_info in manager.getPluginsOfCategory("Tool")
    )


def test_hadolint_tool_plugin_scan_valid():
    """Integration test: Make sure the hadolint output hasn't changed."""
    plugin = setup_hadolint_tool_plugin()
    if not plugin.command_exists("hadolint"):
        pytest.skip("Missing hadolint executable.")
    package = Package(
        "valid_package", os.path.join(os.path.dirname(__file__), "valid_package")
    )
    package["dockerfile_src"] = [
        os.path.join(os.path.dirname(__file__), "valid_package", "Dockerfile.noissues")
    ]
    issues = plugin.scan(package, "level")
    assert not issues


def test_hadolint_tool_plugin_scan_valid_with_issues():
    """Integration test: Make sure the hadolint output hasn't changed."""
    plugin = setup_hadolint_tool_plugin()
    if not plugin.command_exists("hadolint"):
        pytest.skip("Missing hadolint executable.")
    package = Package(
        "valid_package", os.path.join(os.path.dirname(__file__), "valid_package")
    )
    package["dockerfile_src"] = [
        os.path.join(os.path.dirname(__file__), "valid_package", "Dockerfile")
    ]
    issues = plugin.scan(package, "level")
    # We expect a 2 issues: DL3020 use COPY instead of ADD, DL3007 using latest is prone to errors
    assert len(issues) == 2


def test_hadolint_tool_plugin_parse_valid():
    """Verify that we can parse the expected output of hadolint."""
    plugin = setup_hadolint_tool_plugin()
    output = '[{"file":"Dockerfile","column":1,"message":"Use COPY instead of ADD for files and folders","code":"DL3020","level":"error","line":3}]'
    issues = plugin.parse_output([output])
    assert len(issues) == 1
    assert issues[0].filename == "Dockerfile"
    assert issues[0].line_number == "3"
    assert issues[0].tool == "hadolint"
    assert issues[0].issue_type == "DL3020"
    assert issues[0].severity == "5"
    assert issues[0].message == "Use COPY instead of ADD for files and folders"


def test_hadolint_tool_plugin_parse_invalid():
    """Verify that invalid output of hadolint is ignored."""
    plugin = setup_hadolint_tool_plugin()
    output = "invalid text"
    issues = plugin.parse_output(output)
    assert not issues


def test_hadolint_tool_plugin_scan_different_binary():
    """Test that issues are None when binary is different."""
    plugin = setup_hadolint_tool_plugin(binary="wrong-binary")
    package = Package(
        "valid_package", os.path.join(os.path.dirname(__file__), "valid_package")
    )
    package["dockerfile_src"] = [
        os.path.join(os.path.dirname(__file__), "valid_package", "Dockerfile")
    ]
    issues = plugin.scan(package, "level")
    assert issues is None


@mock.patch(
    "statick_tool.plugins.tool.hadolint_tool_plugin.subprocess.check_output"
)
def test_hadolint_tool_plugin_scan_calledprocesserror(
    mock_subprocess_check_output,
):
    """
    Test what happens when a CalledProcessError is raised (usually means hadolint hit an error).

    Expected result: issues is None
    """
    mock_subprocess_check_output.side_effect = subprocess.CalledProcessError(
        0, "", output="mocked error"
    )
    plugin = setup_hadolint_tool_plugin()
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
    "statick_tool.plugins.tool.hadolint_tool_plugin.subprocess.check_output"
)
def test_hadolint_tool_plugin_scan_oserror(mock_subprocess_check_output):
    """
    Test what happens when an OSError is raised (usually means hadolint doesn't exist).

    Expected result: issues is None
    """
    mock_subprocess_check_output.side_effect = OSError("mocked error")
    plugin = setup_hadolint_tool_plugin()
    package = Package(
        "valid_package", os.path.join(os.path.dirname(__file__), "valid_package")
    )
    package["dockerfile_src"] = [
        os.path.join(os.path.dirname(__file__), "valid_package", "Dockerfile")
    ]
    issues = plugin.scan(package, "level")
    assert issues is None
