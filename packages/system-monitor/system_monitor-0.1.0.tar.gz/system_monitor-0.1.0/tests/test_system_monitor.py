#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `system_monitor` package."""


import unittest
from click.testing import CliRunner

from system_monitor import system_monitor
from system_monitor import cli


class TestSystem_monitor(unittest.TestCase):
    """Tests for `system_monitor` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'system_monitor.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
