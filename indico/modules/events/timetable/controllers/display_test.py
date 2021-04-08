# This file is part of Indico.
# Copyright (C) 2002 - 2021 CERN
#
# Indico is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see the
# LICENSE file for more details.

import pytest
from mock import MagicMock
from werkzeug.exceptions import Forbidden

from indico.core.db.sqlalchemy.protection import ProtectionMode
from indico.modules.events.timetable.controllers.display import RHTimetableEntryInfo


@pytest.mark.usefixtures('request_context')
@pytest.mark.parametrize('event_allowed', (False, True))
@pytest.mark.parametrize('allowed', (False, True))
def test_timetable_entry_info_access(dummy_event, dummy_user, allowed, event_allowed):
    dummy_event.protection_mode = ProtectionMode.public if event_allowed else ProtectionMode.protected
    rh = RHTimetableEntryInfo()
    rh.event = dummy_event
    rh.entry = MagicMock()
    rh.entry.can_view.return_value = allowed
    # event access should not matter for the RH access check as having access e.g.
    # to a specific session lets users view the timetabel for that session
    assert dummy_event.can_access(dummy_user) == event_allowed
    if allowed:
        rh._check_access()
    else:
        with pytest.raises(Forbidden):
            rh._check_access()
