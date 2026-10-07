from setuptools import setup
from setup_translate import cmdclass

pkg = "SystemPlugins.RemoteControlCode"
setup(
	name="enigma2-plugin-systemplugins-remotecontrolcode",
	version="1.0",
	description="Change Beyonwiz Remote Control Code",
	license="GPL-3.0-only",
	package_dir={pkg: "BeyonwizRemote"},
	packages=[pkg],
	package_data={pkg: ["*.png", "*.xml", "locale/*/LC_MESSAGES/*.mo"]},
	cmdclass=cmdclass,
)
