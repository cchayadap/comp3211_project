"""Unit tests for the model package. Run: python -m unittest discover -s tests -t ."""
import os
import tempfile
import unittest

from model import (PIMCollection, Note, Task, Event, Contact, parse_criterion,
                   TypeCriterion, save_pim, load_pim)


class TestRecords(unittest.TestCase):
    def test_create_task_parses_deadline(self):
        # Exercises US3: a task keeps its description and parsed deadline.
        t = Task("write SRS", "2026-11-20 20:00")
        self.assertEqual(t.deadline.day, 20)

    def test_invalid_time_rejected(self):
        # Expect ValueError for malformed time strings.
        with self.assertRaises(ValueError):
            Task("x", "tomorrow")


class TestCollection(unittest.TestCase):
    def setUp(self):
        self.c = PIMCollection()
        self.note = self.c.create("note", "buy milk")
        self.task = self.c.create("task", "submit hw", "2026-10-15 12:00")
        self.event = self.c.create("event", "lecture", "2026-10-12 09:00",
                                   "2026-10-12 08:30")
        self.contact = self.c.create("contact", "Alice", "1 Hung Hom", "91234567")

    def test_create_all_types(self):
        # US1: four PIR types coexist in one collection.
        self.assertEqual(len(self.c), 4)

    def test_modify_field(self):
        # US6: modifying a text field changes the stored value.
        self.c.modify(self.note.id, "text", "buy bread")
        self.assertEqual(self.c.get(self.note.id).text, "buy bread")

    def test_modify_unknown_field_raises(self):
        with self.assertRaises(KeyError):
            self.c.modify(self.note.id, "nope", "x")

    def test_delete(self):
        # US9: deleted PIR can no longer be retrieved.
        self.c.delete(self.note.id)
        with self.assertRaises(KeyError):
            self.c.get(self.note.id)

    def test_delete_missing_raises(self):
        with self.assertRaises(KeyError):
            self.c.delete(99999)


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.c = PIMCollection()
        self.task = self.c.create("task", "submit hw", "2026-10-15 12:00")
        self.note = self.c.create("note", "hw ideas")
        self.contact = self.c.create("contact", "Alice", "HK", "91234567")

    def ids(self, text):
        return {p.id for p in self.c.search(parse_criterion(text))}

    def test_type(self):
        self.assertEqual(self.ids("type=task"), {self.task.id})

    def test_contains(self):
        self.assertEqual(self.ids('contains "hw"'), {self.task.id, self.note.id})

    def test_time_before_after_equal(self):
        self.assertEqual(self.ids('time < "2026-12-01 00:00"'), {self.task.id})
        self.assertEqual(self.ids('time > "2026-12-01 00:00"'), set())
        self.assertEqual(self.ids('time = "2026-10-15 12:00"'), {self.task.id})

    def test_and_or_not(self):
        self.assertEqual(self.ids('type=task && contains "hw"'), {self.task.id})
        self.assertEqual(self.ids("type=task || type=note"),
                         {self.task.id, self.note.id})
        self.assertEqual(self.ids("! type=note"), {self.task.id, self.contact.id})

    def test_parentheses_and_precedence(self):
        self.assertEqual(self.ids('( type=task || type=note ) && contains "ideas"'),
                         {self.note.id})

    def test_bad_syntax_raises(self):
        for bad in ("", "type=task &&", "( type=task", "foo"):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                parse_criterion(bad)


class TestStorage(unittest.TestCase):
    def test_round_trip(self):
        # US10 + US11: saving then loading preserves all records.
        c = PIMCollection()
        c.create("note", "n")
        c.create("event", "e", "2026-10-12 09:00", "2026-10-12 08:30")
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "x.pim")
            save_pim(c, path)
            loaded = load_pim(path)
        self.assertEqual([str(p) for p in c.all()], [str(p) for p in loaded.all()])

    def test_wrong_extension(self):
        with self.assertRaises(ValueError):
            save_pim(PIMCollection(), "x.txt")

    def test_corrupt_file(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "bad.pim")
            with open(path, "w") as f:
                f.write("not json\n")
            with self.assertRaises(ValueError):
                load_pim(path)


if __name__ == "__main__":
    unittest.main()
