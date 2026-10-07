#!/bin/sh
set -e
sh "$(dirname "$0")/../src/BeyonwizRemote/locale/updatepot.sh"
git add src/BeyonwizRemote/locale
git diff --cached --quiet || git commit -m "PO/POT update"
