"""Named loggers; never print; never log secrets."""

from __future__ import annotations

import logging

log = logging.getLogger("docsdesk.examples")
assert log.name == "docsdesk.examples"
print("1.6 examples ok")
