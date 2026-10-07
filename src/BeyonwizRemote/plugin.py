from os.path import isfile
from Components.config import ConfigSelection, ConfigSubsection, config, configfile
from Components.SystemInfo import BoxInfo
from Screens.MessageBox import MessageBox
from Screens.Setup import Setup
from Plugins.Plugin import PluginDescriptor

from . import translate

RC_TYPE_PATH = "/proc/stb/ir/rc/type"
MACHINE_BUILD = BoxInfo.getItem("machinebuild")
SUPPORTED_MODELS = ("beyonwizt2", "beyonwizt3", "beyonwizt4", "beyonwizu4")
# U4 uses the Xtrend driver numbering, not the INI T-series values.
RC_CODES = (
	("506", "T3 (0xABCD)"),
	("507", "0xAE97"),
	("508", "0x02F2"),
	("509", "0x02F3"),
	("510", "0x02F4"),
) if MACHINE_BUILD == "beyonwizu4" else (
	("0", "All supported codes"),
	("3", "HDx (0x0933)"),
	("5", "T3 (0xABCD)"),
	("6", "0x02F2"),
	("7", "0x02F3"),
	("8", "0x02F4"),
	("10", "0xAE97"),
)
RC_VALUES = frozenset(x[0] for x in RC_CODES)

rcMode = None
if MACHINE_BUILD in SUPPORTED_MODELS:
	if not hasattr(config.plugins, "RCSetup"):
		config.plugins.RCSetup = ConfigSubsection()
	# Preserve the configuration path used by the original Beyonwiz plugin.
	config.plugins.RCSetup.mode = ConfigSelection(default="507" if MACHINE_BUILD == "beyonwizu4" else "0", choices=RC_CODES)
	rcMode = config.plugins.RCSetup.mode
	rcMode.save_forced = True


def _isSupported():
	return MACHINE_BUILD in SUPPORTED_MODELS and isfile(RC_TYPE_PATH)


def _readCode():
	with open(RC_TYPE_PATH, encoding="ascii") as codeFile:
		code = str(int(codeFile.read().strip()))
	if code not in RC_VALUES:
		raise ValueError(f"Unsupported receiver code: {code}")
	return code


def _writeCode(code):
	if not _isSupported() or code not in RC_VALUES:
		raise ValueError("Unsupported receiver or remote control code")
	with open(RC_TYPE_PATH, "w", encoding="ascii") as codeFile:
		codeFile.write(code)
	if _readCode() != code:
		raise ValueError("The driver did not accept the remote control code")


class RemoteControlCode(Setup):
	def __init__(self, session):
		self._previousCode = None
		self._code = ConfigSelection(default=rcMode.value if rcMode else RC_CODES[0][0], choices=RC_CODES)
		Setup.__init__(self, session, setup=None)
		self.onClose.append(self._restoreCode)
		try:
			if not _isSupported():
				raise ValueError("Receiver does not support Beyonwiz remote control codes")
			self._code.value = _readCode()
			self._code.save()
		except (OSError, ValueError) as error:
			print(f"[BeyonwizRemote] Unable to read the current code: {error}")
			self.setFootnote(translate("The current receiver code could not be read. No change will be made."))

	def createSetup(self):
		choices = [(x[0], translate("All supported codes") if x[0] == "0" else x[1]) for x in RC_CODES]
		self._code.setChoices(choices)
		self.list = [(translate("Remote control code"), self._code, translate("Select a code supported by your remote. After saving, change the remote to the same code and confirm within 30 seconds. Otherwise the previous receiver code will be restored."))]
		self["config"].setList(self.list)
		self.setTitle(translate("Remote Control Code"))

	def keySave(self):
		if self._previousCode is not None:
			return
		try:
			if not _isSupported():
				raise ValueError("Receiver does not support Beyonwiz remote control codes")
			previousCode = _readCode()
			if self._code.value != previousCode:
				self._previousCode = previousCode
				_writeCode(self._code.value)
		except (OSError, ValueError) as error:
			print(f"[BeyonwizRemote] Unable to change the code: {error}")
			restored = self._restoreCode()
			self.session.open(MessageBox, translate("The remote control code could not be changed.") if restored else translate("The previous receiver code could not be restored. Restart the receiver to reload the saved code."), type=MessageBox.TYPE_ERROR)
			return
		if self._previousCode is None:
			self._confirmCode(True)
		else:
			self.session.openWithCallback(self._confirmCode, MessageBox, translate("Change your remote to the selected code now.\n\nDoes the remote work with this receiver?\n\nWithout confirmation, the previous receiver code will be restored after 30 seconds."), type=MessageBox.TYPE_YESNO, timeout=30, default=False)

	def _confirmCode(self, confirmed):
		if confirmed:
			rcMode.value = self._code.value
			rcMode.save()
			configfile.save()
			self._previousCode = None
			self.close()
		elif self._restoreCode():
			self.setFootnote(translate("The previous receiver code has been restored. Change your remote back if necessary."))
		else:
			self.session.open(MessageBox, translate("The previous receiver code could not be restored. Restart the receiver to reload the saved code."), type=MessageBox.TYPE_ERROR)

	def _restoreCode(self):
		restored = True
		if self._previousCode is not None:
			try:
				_writeCode(self._previousCode)
				self._code.value = self._previousCode
				self._code.save()
				self._previousCode = None
			except (OSError, ValueError) as error:
				print(f"[BeyonwizRemote] Unable to restore the previous code: {error}")
				restored = False
		return restored


def _autostart(reason, **kwargs):
	# Never change a fresh installation to a guessed default code.
	if reason == 0 and _isSupported() and rcMode.saved_value in RC_VALUES:
		previousCode = None
		try:
			previousCode = _readCode()
			if previousCode != rcMode.saved_value:
				_writeCode(rcMode.saved_value)
		except (OSError, ValueError) as error:
			print(f"[BeyonwizRemote] Unable to apply the saved code: {error}")
			if previousCode is not None:
				try:
					_writeCode(previousCode)
				except (OSError, ValueError) as restoreError:
					print(f"[BeyonwizRemote] Unable to restore the startup code: {restoreError}")


def main(session, **kwargs):
	session.open(RemoteControlCode)


def RemoteControlSetup(menuid, **kwargs):
	# Some images already provide a native menu.xml entry for this class.
	return [(translate("Remote Control Code"), main, "remotecontrolcode", 50)] if menuid == "system" and not BoxInfo.getItem("RemoteCode") and _isSupported() else []


def Plugins(**kwargs):
	return [
		PluginDescriptor(name=translate("Remote Control Code"), where=PluginDescriptor.WHERE_MENU, needsRestart=False, fnc=RemoteControlSetup),
		PluginDescriptor(where=PluginDescriptor.WHERE_AUTOSTART, needsRestart=False, fnc=_autostart),
	] if _isSupported() else []
