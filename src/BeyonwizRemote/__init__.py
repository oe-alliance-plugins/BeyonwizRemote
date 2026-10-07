from gettext import bindtextdomain, dgettext, gettext
from Components.Language import language
from Tools.Directories import SCOPE_PLUGINS, resolveFilename

__version__ = "1.0"
PLUGIN_LANGUAGE_DOMAIN = "RemoteControlCode"


def localeInit():
	bindtextdomain(PLUGIN_LANGUAGE_DOMAIN, resolveFilename(SCOPE_PLUGINS, "SystemPlugins/RemoteControlCode/locale"))


def translate(text):
	translated = dgettext(PLUGIN_LANGUAGE_DOMAIN, text)
	return gettext(text) if translated == text else translated


localeInit()
language.addCallback(localeInit)
