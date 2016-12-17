#!/bin/ash
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

set -e

# Add openssl as command if needed
if [ "${1:0:1}" = '-' ]; then
	set -- openssl "$@"
fi

# As argument is not related to openssl,
# then assume that user wants to run their own process,
# for example a `bash` shell to explore this image
exec "$@"
