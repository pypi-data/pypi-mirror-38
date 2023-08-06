# Author: echel0n <echel0n@sickrage.ca>
# URL: https://sickrage.ca
#
# This file is part of SickRage.
#
# SickRage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SickRage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickRage.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import unicode_literals

from sickrage.core.queues import srQueue, srQueueItem


class EventQueue(srQueue):
    def __init__(self):
        srQueue.__init__(self, "EVENTQUEUE")

    def fire_event(self, event, force=False):
        return self.put(EventQueueItem(event))


class EventQueueItem(srQueueItem):
    """
    Represents an event in the queue waiting to be executed
    """

    def __init__(self, event):
        super(EventQueueItem, self).__init__('Firing Event')
        self.event = event

    def run(self):
        self.event()
