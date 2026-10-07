from os.path import isfile
from Components.config import ConfigSelection, ConfigSubsection, config, configfile
from Components.SystemInfo import BoxInfo
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Screens.Setup import Setup

from . import _


class RemoteControlHelper:
	TYPE_PATH = "/proc/stb/ir/rc/type"
	SUPPORTED_MODELS = ("beyonwizt2", "beyonwizt3", "beyonwizt4", "beyonwizu4")

	def __init__(self):
		machineBuild = BoxInfo.getItem("machinebuild")
		self.supported = machineBuild in self.SUPPORTED_MODELS and isfile(self.TYPE_PATH)
		# U4 uses the Xtrend driver numbering, not the INI T-series values.
		self.codes = (
			("506", "T3 (0xABCD)"),
			("507", "0xAE97"),
			("508", "0x02F2"),
			("509", "0x02F3"),
			("510", "0x02F4"),
		) if machineBuild == "beyonwizu4" else (
			("0", "All supported codes"),
			("3", "HDx (0x0933)"),
			("5", "T3 (0xABCD)"),
			("6", "0x02F2"),
			("7", "0x02F3"),
			("8", "0x02F4"),
			("10", "0xAE97"),
		)
		self.values = frozenset(x[0] for x in self.codes)
		self.mode = None
		if machineBuild in self.SUPPORTED_MODELS:
			if not hasattr(config.plugins, "RCSetup"):
				config.plugins.RCSetup = ConfigSubsection()
			# Preserve the configuration path used by the original Beyonwiz plugin.
			config.plugins.RCSetup.mode = ConfigSelection(default="507" if machineBuild == "beyonwizu4" else "0", choices=self.codes)
			self.mode = config.plugins.RCSetup.mode
			self.mode.save_forced = True

	def readCode(self):
		with open(self.TYPE_PATH, encoding="ascii") as codeFile:
			code = str(int(codeFile.read().strip()))
		if code not in self.values:
			raise ValueError(f"Unsupported receiver code: {code}")
		return code

	def writeCode(self, code):
		if not self.supported or code not in self.values:
			raise ValueError("Unsupported receiver or remote control code")
		with open(self.TYPE_PATH, "w", encoding="ascii") as codeFile:
			codeFile.write(code)
		if self.readCode() != code:
			raise ValueError("The driver did not accept the remote control code")

	def applySavedCode(self):
		# Never change a fresh installation to a guessed default code.
		if self.supported and self.mode.saved_value in self.values:
			previousCode = None
			try:
				previousCode = self.readCode()
				if previousCode != self.mode.saved_value:
					self.writeCode(self.mode.saved_value)
			except (OSError, ValueError) as error:
				print(f"[BeyonwizRemote] Unable to apply the saved code: {error}")
				if previousCode is not None:
					try:
						self.writeCode(previousCode)
					except (OSError, ValueError) as restoreError:
						print(f"[BeyonwizRemote] Unable to restore the startup code: {restoreError}")


remoteControlHelper = RemoteControlHelper()


class RemoteControlCode(Setup):
	def __init__(self, session):
		self.previousCode = None
		codes = remoteControlHelper.codes
		self.code = ConfigSelection(default=remoteControlHelper.mode.value if remoteControlHelper.mode else codes[0][0], choices=[(x[0], _("All supported codes") if x[0] == "0" else x[1]) for x in codes])
		Setup.__init__(self, session, setup=None)
		self.onClose.append(self.restoreCode)
		try:
			if not remoteControlHelper.supported:
				raise ValueError("Receiver does not support Beyonwiz remote control codes")
			self.code.value = remoteControlHelper.readCode()
			self.code.save()
		except (OSError, ValueError) as error:
			print(f"[BeyonwizRemote] Unable to read the current code: {error}")
			self.setFootnote(_("The current receiver code could not be read. No change will be made."))

	def createSetup(self):
		self.list = [(_("Remote control code"), self.code, _("Select a code supported by your remote. After saving, change the remote to the same code and confirm within 30 seconds. Otherwise the previous receiver code will be restored."))]
		self["config"].setList(self.list)
		self.setTitle(_("Remote Control Code"))

	def keySave(self):
		if self.previousCode is None:
			try:
				if not remoteControlHelper.supported:
					raise ValueError("Receiver does not support Beyonwiz remote control codes")
				previousCode = remoteControlHelper.readCode()
				if self.code.value != previousCode:
					self.previousCode = previousCode
					remoteControlHelper.writeCode(self.code.value)
			except (OSError, ValueError) as error:
				print(f"[BeyonwizRemote] Unable to change the code: {error}")
				restored = self.restoreCode()
				self.session.open(MessageBox, _("The remote control code could not be changed.") if restored else _("The previous receiver code could not be restored. Restart the receiver to reload the saved code."), type=MessageBox.TYPE_ERROR)
			else:
				if self.previousCode is None:
					self.confirmCode(True)
				else:
					self.session.openWithCallback(self.confirmCode, MessageBox, _("Change your remote to the selected code now.\n\nDoes the remote work with this receiver?\n\nWithout confirmation, the previous receiver code will be restored after 30 seconds."), type=MessageBox.TYPE_YESNO, timeout=30, default=False)

	def confirmCode(self, confirmed):
		if confirmed:
			remoteControlHelper.mode.value = self.code.value
			remoteControlHelper.mode.save()
			configfile.save()
			self.previousCode = None
			self.close()
		elif self.restoreCode():
			self.setFootnote(_("The previous receiver code has been restored. Change your remote back if necessary."))
		else:
			self.session.open(MessageBox, _("The previous receiver code could not be restored. Restart the receiver to reload the saved code."), type=MessageBox.TYPE_ERROR)

	def restoreCode(self):
		restored = True
		if self.previousCode is not None:
			try:
				remoteControlHelper.writeCode(self.previousCode)
				self.code.value = self.previousCode
				self.code.save()
				self.previousCode = None
			except (OSError, ValueError) as error:
				print(f"[BeyonwizRemote] Unable to restore the previous code: {error}")
				restored = False
		return restored


def autostart(reason, **kwargs):
	if reason == 0:
		remoteControlHelper.applySavedCode()


def main(session, **kwargs):
	session.open(RemoteControlCode)


def RemoteControlSetup(menuid, **kwargs):
	# Some images already provide a native menu.xml entry for this class.
	return [(_("Remote Control Code"), main, "remotecontrolcode", 50)] if menuid == "system" and not BoxInfo.getItem("RemoteCode") and remoteControlHelper.supported else []


def Plugins(**kwargs):
	return [
		PluginDescriptor(name=_("Remote Control Code"), where=PluginDescriptor.WHERE_MENU, needsRestart=False, fnc=RemoteControlSetup),
		PluginDescriptor(where=PluginDescriptor.WHERE_AUTOSTART, needsRestart=False, fnc=autostart),
	] if remoteControlHelper.supported else []
