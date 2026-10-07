#!/bin/sh
set -eu
cd "$(dirname "$0")"
xgettext --language=Python --from-code=UTF-8 --keyword=translate --sort-output --no-wrap \
    --package-name=BeyonwizRemote --package-version=1.0 \
    --msgid-bugs-address=https://github.com/oe-alliance-plugins/BeyonwizRemote/issues \
    -o RemoteControlCode.pot ../plugin.py
for catalog in ./*.po; do
    [ -f "$catalog" ] || continue
    msgmerge --update --backup=none --no-wrap "$catalog" RemoteControlCode.pot
    msgfmt --check "$catalog" -o /dev/null
done
