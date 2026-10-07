from gettext import bindtextdomain, dgettext, gettext
from Components.Language import language
from Tools.Directories import SCOPE_PLUGINS, resolveFilename

__version__ = "1.1"
PluginLanguageDomain = "RemoteControlCode"


def localeInit():
	bindtextdomain(PluginLanguageDomain, resolveFilename(SCOPE_PLUGINS, "SystemPlugins/RemoteControlCode/locale"))


def _(text):
	translated = dgettext(PluginLanguageDomain, text)
	return gettext(text) if translated == text else translated


localeInit()
language.addCallback(localeInit)
