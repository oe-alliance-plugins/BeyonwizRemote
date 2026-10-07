from glob import glob
from os import makedirs
from os.path import basename, join, splitext
from subprocess import run
from setuptools import Command
from setuptools.command.build import build as Build


class BuildTranslations(Command):
	description = "Compile translations with GNU gettext"
	user_options = []

	def initialize_options(self):
		pass

	def finalize_options(self):
		pass

	def run(self):
		localePath = join("BeyonwizRemote", "locale")
		for source in sorted(glob(join(localePath, "*.po"))):
			language = splitext(basename(source))[0]
			destination = join(localePath, language, "LC_MESSAGES")
			makedirs(destination, exist_ok=True)
			run(["msgfmt", "--check", source, "-o", join(destination, "RemoteControlCode.mo")], check=True)


class BuildWithTranslations(Build):
	# Translations must exist before build_py collects package_data.
	sub_commands = [("build_trans", None)] + Build.sub_commands


cmdclass = {"build": BuildWithTranslations, "build_trans": BuildTranslations}
