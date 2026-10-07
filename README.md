

# <p align="center">RemoteControlCode Plugin for Enigma2 (E²) ![GitHub repo size](https://img.shields.io/github/repo-size/oe-alliance-plugins/BeyonwizRemote.svg)</p>

**Select the receiver's IR code on Beyonwiz T2, T3, T4 and U4.**

## Usage

Open **Setup → Usage & GUI → Remote Control Code**. Select a code supported by
your physical remote, press Green, change the remote to that code and confirm
within 30 seconds. No/timeout restores the previous receiver code. A confirmed
choice is restored at GUI startup. Installing the plugin alone does not change
the current code.

T2/T3/T4 and U4 use different driver values:

| Remote code | T2/T3/T4 driver type | U4 driver type |
| --- | --- | --- |
| All supported codes | 0 | Not supported |
| HDx (0x0933) | 3 | Not supported |
| T3 (0xABCD) | 5 | 506 |
| 0x02F2 | 6 | 508 |
| 0x02F3 | 7 | 509 |
| 0x02F4 | 8 | 510 |
| 0xAE97 | 10 | 507 |

These are receiver settings, not remote key programming. A standard T3 remote is
fixed to 0xABCD. T2/T4 remotes support 0x02F2/0x02F3/0x02F4; U4 remotes support
0xAE97/0x02F3. Consult the remote's manual before switching. When using adjacent
receivers, do not use "All supported codes".

The plugin requires `/proc/stb/ir/rc/type`. V2 and non-Beyonwiz receivers are
not enabled. The existing Beyonwiz setting `config.plugins.RCSetup.mode` is
retained. No receiver reboot is required to test a code.

### Reference

Driver values follow the original
[Beyonwiz remote-code documentation](https://bitbucket.org/beyonwiz/easy-ui-4/src/master/doc/REMOTE_CODES)
and [RemoteControlCode plugin](https://bitbucket.org/beyonwiz/easy-ui-4/src/master/lib/python/Plugins/SystemPlugins/RemoteControlCode/plugin.py).

### Build and translations

The repository follows GigaBlueRemote/VuRemote: `src/setup.py`, standard
OE-Alliance workflows, and `__version__` in `src/BeyonwizRemote/__init__.py`.
The recipe uses branch `main` and `gittag`, and installs as
`enigma2-plugin-systemplugins-remotecontrolcode` in
`Plugins/SystemPlugins/RemoteControlCode`. Only one brand variant may be installed.

With Python setuptools and GNU gettext available:

```sh
cd src
python3 setup.py build
```

PO files are compiled before Python package data is copied, including on a clean
first build. To update the POT/PO files, run
`sh src/BeyonwizRemote/locale/updatepot.sh`.

### Skinning and testing

Uses the standard Setup screen; existing skins do not need changing. A skin
may optionally provide `RemoteControlCode`, preserving Setup's widget names.

Run `python3 -m unittest discover -s tests -v` and `ruff check .`.
Before release, test a real T-series receiver and a U4 separately:

1. Check the initial code is unchanged after installation.
2. Switch to a code the remote supports and confirm using that remote.
3. Repeat but wait for the timeout; the previous remote must work again.
4. Cancel without saving; the stored code must remain unchanged.
5. Restart the GUI and cold-boot; the confirmed code must be restored.
6. Check adjacent boxes respond only to their own remote.
7. Check English/German and HD/FHD Setup layouts.

Unit tests mock the driver/GUI; they do not prove physical remote compatibility.
No Beyonwiz receiver was available for hardware testing during implementation.



## Github status
[![Build](https://github.com/oe-alliance-plugins/BeyonwizRemote/actions/workflows/buildbot.yml/badge.svg)](https://github.com/oe-alliance-plugins/BeyonwizRemote/actions/workflows/buildbot.yml)
[![Lint Status](https://github.com/oe-alliance-plugins/BeyonwizRemote/actions/workflows/pylint.yml/badge.svg)](https://github.com/oe-alliance-plugins/BeyonwizRemote/actions/workflows/pylint.yml)
[![Ruff Status](https://github.com/oe-alliance-plugins/BeyonwizRemote/actions/workflows/ruff.yml/badge.svg)](https://github.com/oe-alliance-plugins/BeyonwizRemote/actions/workflows/ruff.yml)
[![Build Status](https://github.com/oe-alliance-plugins/BeyonwizRemote/actions/workflows/compile.yml/badge.svg)](https://github.com/oe-alliance-plugins/BeyonwizRemote/actions/workflows/compile.yml)
[![AUTOTAG](https://github.com/oe-alliance-plugins/BeyonwizRemote/actions/workflows/autotag.yml/badge.svg)](https://github.com/oe-alliance-plugins/BeyonwizRemote/actions/workflows/autotag.yml)


[![Plugin Version](https://img.shields.io/github/v/tag/oe-alliance-plugins/BeyonwizRemote?label=Latest%20Version&color=darkviolet)](https://github.com/oe-alliance-plugins/BeyonwizRemote/tags)
[![Latest Release](https://img.shields.io/github/release-date/oe-alliance-plugins/BeyonwizRemote?label=From&color=darkviolet)](https://github.com/oe-alliance-plugins/BeyonwizRemote/releases/latest)
[![Github last commit](https://img.shields.io/github/last-commit/oe-alliance-plugins/BeyonwizRemote)](https://github.com/oe-alliance-plugins/BeyonwizRemote)
[![GitHub Activity](https://img.shields.io/github/commit-activity/y/oe-alliance-plugins/BeyonwizRemote.svg?label=commits)](https://github.com/oe-alliance-plugins/BeyonwizRemote/commits)
[![GitHub Activity](https://img.shields.io/github/commit-activity/m/oe-alliance-plugins/BeyonwizRemote.svg?label=commits)](https://github.com/oe-alliance-plugins/BeyonwizRemote/commits)


---

### 📜 License Information [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

This is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation

This plugin is released under GPLv3. See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.html#license-text) for full details.

<img width="120" height="58" alt="GPLv3_Logo svg" src="https://github.com/user-attachments/assets/67d32b0a-2a44-4fa9-a972-202daf28808e" />

---

### 🤝 Contributing & Contact

RemoteControlCode is created by users for users and we welcome every contribution. There are no highly paid developers. There are only users who have seen a problem and done their best to fix it. This means BeyonwizRemote will always need the contributions of users like you. How can you get involved?

For questions or feedback, feel free and please open an issue or contribute with a Pull Request!

Pull requests are very welcome for:
- **Coding:** Developers can help by fixing a bug, adding new features, Integration improvements, Feature enhancements
- **Localization:** Translate into your native language.
- **Helping users:** Our support process relies on enthusiastic contributors like you to help others.

Your contribution is very welcome! Follow these steps:

1. 🍴 Fork this repository
2. 🔄 Create a branch for your feature
3. 💻 Make your changes
4. ✅ Commit using conventional messages
5. 📤 Push to your branch
6. 🔍 Open a Pull Request

Enjoy and help us improve it today. :)

### 🚨 Disclaimer

The project author is not responsible for how this software is used by others. It is not intended to be used for accessing or distributing copyrighted materials without authorization.
Users are solely responsible for determining the legality of their actions.

This repository has no control over the streams, links, or the legality of the content provided by the different hosts (including all mirror sites). It is the end user's responsibility to ensure the legal use of these streams, and we strongly recommend verifying that the content complies with all applicable laws, including copyright laws and regulations of your countrys jurisdiction before use.

---

### 🤝 Contributing Details

For detailed contributing guidelines including testing procedures and AI policy, please see [CONTRIBUTING.md](https://github.com/oe-alliance-plugins/.github/blob/main/docs/CONTRIBUTING.md).

---

⭐️ If you find this plugin useful, please give it a star on GitHub!
Thanks! ❤️ 💞 💖 ❤️‍🔥 💗
