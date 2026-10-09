"""Controller: parses user commands, calls the model, returns text for the view."""
import shlex
from model import (PIMCollection, parse_criterion, save_pim, load_pim)
from model.records import RECORD_TYPES

HELP = """Commands:
  create note "<text>"
  create task "<description>" "<YYYY-MM-DD HH:MM>"
  create event "<description>" "<start>" "<alarm>"
  create contact "<name>" "<address>" "<mobile>"
  modify <id> <field> "<new value>"
  search <criterion>        e.g. search type=task && time < "2026-12-01 00:00"
  print <id> | print all
  delete <id>
  save <file.pim>
  load <file.pim>
  help
  quit"""


class CommandController:
    def __init__(self, collection: PIMCollection = None):
        self.collection = collection or PIMCollection()
        self.running = True

    def execute(self, line: str) -> str:
        """Run one command line; always returns a message (never raises)."""
        line = line.strip()
        if not line:
            return ""
        verb, _, rest = line.partition(" ")
        verb = verb.lower()
        try:
            handler = getattr(self, f"_cmd_{verb}", None)
            if handler is None:
                return f"Error: unknown command '{verb}'. Type 'help'."
            return handler(rest.strip())
        except (ValueError, KeyError, OSError) as e:
            return f"Error: {e.args[0] if isinstance(e, KeyError) else e}"

    @staticmethod
    def _args(rest: str) -> list:
        try:
            return shlex.split(rest)
        except ValueError as e:
            raise ValueError(f"Bad quoting: {e}")

    def _cmd_help(self, rest):
        return HELP

    def _cmd_quit(self, rest):
        self.running = False
        return "Bye."

    def _cmd_create(self, rest):
        args = self._args(rest)
        if not args:
            raise ValueError("Usage: create <note|task|event|contact> ...")
        type_name, fields = args[0].lower(), args[1:]
        cls = RECORD_TYPES.get(type_name)
        if cls is None:
            raise ValueError(f"Unknown type '{type_name}'")
        if len(fields) != len(cls.FIELDS):
            raise ValueError(f"'{type_name}' needs {len(cls.FIELDS)} value(s): "
                             f"{', '.join(cls.FIELDS)}")
        pir = self.collection.create(type_name, *fields)
        return f"Created {pir}"

    def _cmd_modify(self, rest):
        args = self._args(rest)
        if len(args) != 3:
            raise ValueError('Usage: modify <id> <field> "<new value>"')
        pir = self.collection.modify(self._id(args[0]), args[1], args[2])
        return f"Updated {pir}"

    def _cmd_search(self, rest):
        results = self.collection.search(parse_criterion(rest))
        if not results:
            return "No matching PIRs."
        return "\n".join(str(p) for p in results)

    def _cmd_print(self, rest):
        if rest.lower() == "all":
            items = self.collection.all()
            return "\n".join(str(p) for p in items) or "No PIRs stored."
        return str(self.collection.get(self._id(rest)))

    def _cmd_delete(self, rest):
        pir_id = self._id(rest)
        self.collection.delete(pir_id)
        return f"Deleted PIR {pir_id}"

    def _cmd_save(self, rest):
        save_pim(self.collection, rest)
        return f"Saved {len(self.collection)} PIR(s) to {rest}"

    def _cmd_load(self, rest):
        self.collection = load_pim(rest)
        return f"Loaded {len(self.collection)} PIR(s) from {rest}"

    @staticmethod
    def _id(text: str) -> int:
        try:
            return int(text)
        except ValueError:
            raise ValueError(f"'{text}' is not a valid PIR id")
