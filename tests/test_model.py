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

    def test_str_shows_all_fields(self):
        # US8: printing a task/contact shows every field.
        t = Task("write SRS", "2026-11-20 20:00", pir_id=1)
        self.assertEqual(str(t), "[1] Task: write SRS (deadline 2026-11-20 20:00)")
        c = Contact("Alice", "1 Hung Hom", "91234567", pir_id=2)
        self.assertEqual(str(c), "[2] Contact: Alice, 1 Hung Hom, mobile 91234567")

    def test_get_unknown_field_raises(self):
        # Reading a field the PIR type does not have raises KeyError.
        with self.assertRaises(KeyError):
            Note("n").get("deadline")


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

    def test_create_unknown_type_raises(self):
        # US1: only note/task/event/contact can be created.
        with self.assertRaises(ValueError):
            self.c.create("meeting", "x")

    def test_modify_time_field(self):
        # US6: modifying a time field parses the new time.
        self.c.modify(self.task.id, "deadline", "2026-12-01 09:00")
        self.assertEqual(self.c.get(self.task.id).deadline.month, 12)

    def test_clear(self):
        # clear() removes every PIR from the collection.
        self.c.clear()
        self.assertEqual(len(self.c), 0)

    def test_modify_field(self):
        # US6: modifying a text field changes the stored value.
        self.c.modify(self.note.id, "text", "buy bread")
        self.assertEqual(self.c.get(self.note.id).text, "buy bread")

    def test_modify_unknown_field_raises(self):
        # US6: modifying a field the PIR type does not have raises KeyError.
        with self.assertRaises(KeyError):
            self.c.modify(self.note.id, "nope", "x")

    def test_delete(self):
        # US9: deleted PIR can no longer be retrieved.
        self.c.delete(self.note.id)
        with self.assertRaises(KeyError):
            self.c.get(self.note.id)

    def test_delete_missing_raises(self):
        # US9: deleting a non-existent id raises KeyError.
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
        # US7: type criterion matches only PIRs of that type.
        self.assertEqual(self.ids("type=task"), {self.task.id})

    def test_contains(self):
        # US7: contains matches any text field, case-insensitive.
        self.assertEqual(self.ids('contains "hw"'), {self.task.id, self.note.id})

    def test_time_before_after_equal(self):
        # US7: time criterion supports <, > and = on time fields.
        self.assertEqual(self.ids('time < "2026-12-01 00:00"'), {self.task.id})
        self.assertEqual(self.ids('time > "2026-12-01 00:00"'), set())
        self.assertEqual(self.ids('time = "2026-10-15 12:00"'), {self.task.id})

    def test_and_or_not(self):
        # US7: &&, || and ! combine criteria.
        self.assertEqual(self.ids('type=task && contains "hw"'), {self.task.id})
        self.assertEqual(self.ids("type=task || type=note"),
                         {self.task.id, self.note.id})
        self.assertEqual(self.ids("! type=note"), {self.task.id, self.contact.id})

    def test_parentheses_and_precedence(self):
        # US7: parentheses group sub-criteria before && is applied.
        self.assertEqual(self.ids('( type=task || type=note ) && contains "ideas"'),
                         {self.note.id})

    def test_spaced_and_glued_syntax(self):
        # US7: "type = task", "!type=note" and "(type=task)" are all accepted.
        self.assertEqual(self.ids("type = task"), {self.task.id})
        self.assertEqual(self.ids("!type=note"), {self.task.id, self.contact.id})
        self.assertEqual(self.ids("(type=task)"), {self.task.id})

    def test_unknown_time_operator_raises(self):
        # US7: only <, > and = are valid time operators.
        with self.assertRaises(ValueError):
            parse_criterion('time <= "2026-12-01 00:00"')

    def test_bad_syntax_raises(self):
        # US7: malformed criteria raise ValueError instead of crashing.
        for bad in ("", "type=task &&", "( type=task", "foo",
                    "( type=task type=note )",   # missing ')' before next atom
                    "type=task type=note",       # two atoms with no connector
                    "type task",                 # missing '=' after type
                    'contains "unclosed'):       # unterminated quote
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

    def test_blank_lines_ignored(self):
        # US11: blank lines in a .pim file are skipped when loading.
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "x.pim")
            with open(path, "w") as f:
                f.write('\n{"type": "note", "id": 1, "text": "n"}\n\n')
            self.assertEqual(len(load_pim(path)), 1)

    def test_wrong_extension(self):
        # US10: only files ending in .pim may be saved.
        with self.assertRaises(ValueError):
            save_pim(PIMCollection(), "x.txt")

    def test_corrupt_file(self):
        # US11: loading a file with invalid content raises ValueError.
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "bad.pim")
            with open(path, "w") as f:
                f.write("not json\n")
            with self.assertRaises(ValueError):
                load_pim(path)


if __name__ == "__main__":
    unittest.main()
