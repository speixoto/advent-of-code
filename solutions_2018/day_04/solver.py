from dataclasses import dataclass, field
from re import match
from typing import Dict, List
from collections import defaultdict

from ..common.common import get_input


@dataclass
class Record(object):
    year: int = 0
    month: int = 0
    day: int = 0
    hour: int = 0
    minute: int = 0
    action: str = ''

    @property
    def guard_id(self) -> int:
        match_result = match('Guard #(?P<guard_id>.+) begins shift', self.action)
        if match_result:
            return int(match_result.group('guard_id'))
        return 0

    @property
    def is_begin_of_shift(self) -> bool:
        return 'begins shift' in self.action

    @property
    def is_start_sleeping(self) -> bool:
        return 'falls asleep' in self.action

    @property
    def is_waked_up(self) -> bool:
        return 'wakes up' in self.action


@dataclass
class Guard(object):
    id: int = 0
    records: List[Record] = field(default_factory=lambda: [])
    minutes_sleeping: List[int] = field(default_factory=lambda: [0] * 60, init=False)
    _minute_started_sleeping: int = 0

    def process_record(self, record: Record) -> None:
        if record.is_start_sleeping:
            self._minute_started_sleeping = record.minute
        if record.is_waked_up:
            for x in range(record.minute - self._minute_started_sleeping):
                self.minutes_sleeping[self._minute_started_sleeping + x] += 1
        self.records.append(record)

    @property
    def total_minutes_sleeping(self):
        return sum(self.minutes_sleeping)

    @property
    def most_sleepy_minute(self):
        return self.minutes_sleeping.index(self.max_times_slept_on_same_minute)

    @property
    def max_times_slept_on_same_minute(self):
        return max(self.minutes_sleeping)


@dataclass
class Team(object):
    guards: Dict[int, Guard] = field(default_factory=lambda: defaultdict(Guard))

    def process_record(self, guard_id: int, record: Record) -> None:
        guard = self.guards[guard_id]
        if guard.id == 0:
            guard.id = guard_id
        guard.process_record(record)

    @property
    def most_sleepy_guard(self):
        guards = list(self.guards.values())
        guards.sort(key=lambda x: x.total_minutes_sleeping, reverse=True)
        return guards[0]

    @property
    def most_sleepy_guard_on_same_minute(self):
        guards = list(self.guards.values())
        guards.sort(key=lambda x: x.max_times_slept_on_same_minute, reverse=True)
        return guards[0]


def parse_record(record_string: str) -> Record:
    """Build a record from a record string"""
    match_result = match(r'\[(?P<year>.+)\-(?P<month>.+)\-(?P<day>.+) (?P<hour>.+):(?P<minute>.+)\] (?P<action>.+)',
                         record_string)
    if match_result:
        return Record(
            int(match_result.group('year')),
            int(match_result.group('month')),
            int(match_result.group('day')),
            int(match_result.group('hour')),
            int(match_result.group('minute')),
            str(match_result.group('action'))
        )
    return Record()


def build_team_from_record_lines(input_lines) -> Team:
    input_lines.sort()
    team = Team()
    guard_id = 0
    for line in input_lines:
        record = parse_record(line)
        if record.guard_id > 0:
            guard_id = record.guard_id
        team.process_record(guard_id, record)
    return team


def run():
    input_lines = get_input('day_04')
    team = build_team_from_record_lines(input_lines)
    sleepiest_guard = team.most_sleepy_guard
    print(f'The sleepiest guard is {sleepiest_guard.id} ({sleepiest_guard.id *sleepiest_guard.most_sleepy_minute})')

    sleepiest_guard = team.most_sleepy_guard_on_same_minute
    print(f'The sleepiest guard is {sleepiest_guard.id} ({sleepiest_guard.id * sleepiest_guard.most_sleepy_minute})')

