import sublime
import sublime_plugin

STVER = int(sublime.version())
ST3 = STVER >= 3000

class ConsoleWrapOpenFileCommand(sublime_plugin.ApplicationCommand):
	"""This is a wrapper class for SublimeText's `open_file` command.

	The task is to hide the command in menu if `edit_settings` is available.
	"""

	@staticmethod
	def run(file):
		"""Expand variables and open the resulting file.

		NOTE: For some unknown reason the `open_file` command doesn't expand
			  ${platform} when called by `run_command`, so it is expanded here.
		"""
		platform_name = {
			'osx': 'OSX',
			'windows': 'Windows',
			'linux': 'Linux',
		}[sublime.platform()]
		file = file.replace('${platform}', platform_name)
		sublime.run_command('open_file', {'file': file})

	@staticmethod
	def is_visible():
		"""Return True to to show the command in command pallet and menu."""
		return STVER < 3124


class ConsoleWrapEditSettingsCommand(sublime_plugin.ApplicationCommand):
	"""This is a wrapper class for SublimeText's `open_file` command.

	Hides the command in menu if `edit_settings` is not available.
	"""

	@staticmethod
	def run(**kwargs):
		"""Expand variables and open the resulting file."""
		sublime.run_command('edit_settings', kwargs)

	@staticmethod
	def is_visible():
		"""Return True to to show the command in command pallet and menu."""
		return STVER >= 3124


def settings():
	return sublime.load_settings('consolewrap.sublime-settings')
