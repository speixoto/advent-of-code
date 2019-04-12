from random import shuffle

from .solver import Record, Guard, Team, build_team_from_record_lines

mock_record_lines = [
    '[1518-11-01 00:00] Guard #10 begins shift',
    '[1518-11-01 00:05] falls asleep',
    '[1518-11-01 00:25] wakes up',
    '[1518-11-01 00:30] falls asleep',
    '[1518-11-01 00:55] wakes up',
    '[1518-11-01 23:58] Guard #99 begins shift',
    '[1518-11-02 00:40] falls asleep',
    '[1518-11-02 00:50] wakes up',
    '[1518-11-03 00:05] Guard #10 begins shift',
    '[1518-11-03 00:24] falls asleep',
    '[1518-11-03 00:29] wakes up',
    '[1518-11-04 00:02] Guard #99 begins shift',
    '[1518-11-04 00:36] falls asleep',
    '[1518-11-04 00:46] wakes up',
    '[1518-11-05 00:03] Guard #99 begins shift',
    '[1518-11-05 00:45] falls asleep',
    '[1518-11-05 00:55] wakes up',
]


def test_sort_records():
    record_lines = mock_record_lines.copy()
    shuffle(record_lines)
    record_lines.sort()
    assert(record_lines == mock_record_lines)


def test_guard_process_records():
    guard = Guard(1234)
    guard.process_record(Record(1999, 11, 1, 0, 12, 'falls asleep'))
    guard.process_record(Record(1999, 11, 1, 0, 16, 'wakes up'))

    for sec in range(60):
        if sec in range(12, 16):
            assert guard.minutes_sleeping[sec] == 1
        else:
            assert guard.minutes_sleeping[sec] == 0

    assert guard.total_minutes_sleeping == 4
    assert guard.most_sleepy_minute == 12


def test_team():
    team = build_team_from_record_lines(mock_record_lines)
    assert team.most_sleepy_guard.id == 10

