# Task split (4 members)

Deadline: **Fri 20 Nov 2026, 20:00**, one ZIP. All documents in DOC, DOCX or PDF; videos in MP4.
The working code (model, controller, view, 31 tests at 100% coverage) is already in this repo,
so the main remaining work is documents, a few code decisions, and recordings.

## Status (18 Oct 2026)

| Deliverable | Owner | Status |
|---|---|---|
| SRS (`srs/COMP3211_PIM_SRS.docx`, v0.4) | Jiayi | Done; group decisions in SRS 6.14 still open |
| Code + SRS gap fixes (GAP-01–05) | Chompoo | Done |
| Requirements coverage table (`REQUIREMENTS_COVERAGE.md`) | Chompoo | Done, mapped to SRS v0.4 IDs |
| Unit tests + line coverage report (`COVERAGE_REPORT.md`) | Chompoo | Done (31 tests, 100%); re-run before submission |
| Design doc: architecture, class, search-then-update sequence diagrams + text | Juhee | To do |
| Developer manual, user manual | Inha | To do |
| Demo video (≤ 4 min MP4) | — | To do; owner not assigned |
| Presentation (≤ 5 min, PDF + MP4) | All | To do |
| Honour Declaration | All | To do |

| Role | Owns | Points at stake |
|---|---|---|
| A | SRS + requirements coverage report | 6 (+ part of 3e) |
| B | Design document | 5 |
| C | Developer manual, user manual, code fixes, demo video | 6 |
| D | Unit tests, coverage report, slides, final ZIP | 4 + 4 |

Everyone: present at least 1 minute in the recording (face + student ID shown), review one other
member's deliverable, and agree contribution percentages for the Honour Declaration.

---

## A: Software Requirements Specification (Deliverable 1)

**Goal:** a document that describes what the system must do, precisely enough that every
requirement can be tested.

**Structure** (Lecture 04, "The Structure of A Requirements Specification"; leave out
System models, System evolution, Appendix and Index):
1. Preface: version history, intended readers.
2. Introduction: purpose of the PIM, scope, how it fits the user's needs.
3. Glossary: PIR, note, task, event, contact, criterion, `.pim` file, etc.
4. User requirements definition: the 11 user stories in plain language.
5. System architecture: one short paragraph and a box diagram (MVC); B can provide this.
6. System requirements specification: the numbered functional and non-functional requirements (the main part).

**Functional requirements:** give each one an ID (e.g. `FR-CREATE-01`) and link it back to its user story.
They should cover at least:
- **Create (US1–US5):** command syntax for each type, required fields, time format
  `YYYY-MM-DD HH:MM`, how IDs are assigned, what is printed on success.
- **Modify (US6):** syntax `modify <id> <field> "<value>"`, valid field names per type, errors for
  bad ID / field / time.
- **Search (US7):** criterion grammar (`type=`, `contains`, `time < > =`, `&&`, `||`, `!`,
  parentheses, precedence `!` > `&&` > `||`), case-insensitive text matching, time criteria
  matching *any* time field, output when nothing matches.
- **Print (US8), Delete (US9):** syntax, output format, error for unknown ID.
- **Save / Load (US10, US11):** `.pim` extension enforced, load replaces the current records,
  behaviour on missing or corrupt files.
- **General:** `help`, `quit`, unknown commands, bad quoting; the program never crashes on bad
  input.

**Non-functional requirements:** e.g. Python 3 standard library only, runs as a command-line program on Windows,
responds to a command within 1 s for 1,000 PIRs, the model sits in a package named `model`, and every error
message starts with `Error:`.

**Decisions A must make (agree them with C, who changes the code to match):**
- Must an event's alarm be at or before its start time?
- Should mobile numbers be validated (digits only? length?)
- `search type=foo`: show an error, or return no results?
- `load` while there are unsaved records: warn, or replace silently?
- Can text fields be empty?

**Then:** fill in the "SRS req IDs" column in `REQUIREMENTS_COVERAGE.md` and add a row for every
SRS requirement (implemented: yes/no).

**Check before handing in:** every requirement is numbered, testable ("shall … within / when …"), and
consistent with what the program actually does (run it to check).

---

## B: Design document (Deliverable 2)

**Goal:** explain how the code is structured and why.

1. **Architecture (2a):** an MVC diagram. Say *why* MVC was chosen (it keeps logic separate from
   console I/O, so the model can be unit-tested) and how it maps onto the code:
   `model/` = Model, `view/cli.py` = View, `controller/commands.py` = Controller, `main.py` = entry point.
2. **Class diagram (2b):** every class with its fields and public/protected methods, return type,
   argument names and types, and the exceptions it can raise. Classes:
   - `PIR` (abstract) → `Note`, `Task`, `Event`, `Contact`
   - `Criterion` (abstract) → `TypeCriterion`, `ContainsCriterion`, `TimeCriterion`,
     `AndCriterion`, `OrCriterion`, `NotCriterion` (this is the Composite pattern; worth naming)
   - `PIMCollection`, `CommandController`
   - Module functions: `parse_time`, `format_time`, `parse_criterion`, `save_pim`, `load_pim`

   Show relationships: inheritance, `PIMCollection` contains many `PIR`s, the controller uses
   the collection, and criteria are passed into `search`.
3. **Sequence diagram (2c):** the user types `search ...`, then `modify ...`. Trace it through
   `run_cli` → `CommandController.execute` → `parse_criterion` → `PIMCollection.search` →
   `Criterion.matches` → result printed; then `modify` → `PIMCollection.modify` → `PIR.set`
   → `parse_time` (for a time field).
4. **Text for every diagram (2d):** what it shows and why the design is modular and easy to extend
   (e.g. adding a new PIR type means one class plus one entry in `RECORD_TYPES`).

Tools: draw.io, PlantUML or StarUML. Export as images inside the PDF/DOCX.
If C changes method signatures, B updates the class diagram.

---

## C: Implementation docs + code (Deliverable 3a–3d)

1. **Code fixes**
   - Make the code follow A's decisions (see the list under A).
   - Keep everything Python standard library only.
2. **Developer manual (3b):** Python version (3.14), recommended IDE (e.g. PyCharm or VS Code)
   and how to open the project, how to run it (`py -3 main.py`), how to run the tests, how to
   start it in debug mode (IDE run config with a breakpoint, or `py -3 -m pdb main.py`), the
   folder layout, and how to add a new PIR type. Pick one platform (Windows).
3. **User manual (3c):** every command with its syntax and an example, the time format, the search
   criterion grammar with examples, what each kind of error looks like, how to read the output
   (`[id] Type: ...`), and a full example session. Must match the SRS.
4. **Demo video (3d):** MP4, **≤ 4 min**. Show creating all four PIR types, a compound search,
   modify, print, delete, save then load, and one or two error cases. Short on-screen captions
   are fine.

---

## D: Tests, coverage, slides, submission (Deliverables 4, 5, Honour Declaration)

1. **Unit tests (4a):** add tests for every model change made by C (parser fix, new validation).
   Each test needs a comment saying what it exercises and an assertion for the expected result. Keep all tests passing.
2. **Coverage report (4b):** re-run before submission and update `COVERAGE_REPORT.md`:

       py -3 -m coverage run --source=model -m unittest discover -s tests -t .
       py -3 -m coverage report -m

3. **Slides + recording (5):** PDF slides, MP4 recording, **≤ 5 min total**, every member speaks
   for at least 1 min with face visible and student ID shown at the start. Content required:
   - three requirements from A's SRS: one on creating a PIR, one on defining a search criterion,
     one on searching
   - the overall design (B's architecture + class diagram)
   - one lesson learned on requirements engineering, API design or unit testing
   Keep screenshots and clips short.
4. **Honour Declaration:** collect the signed form with contribution %; acknowledge all GenAI use
   (at least: Claude Code fixed the package layout and wrote tests and the coverage report). Missing it costs **up to 30%**.
5. **Final ZIP:** source code (with `REQUIREMENTS_COVERAGE.md` and `COVERAGE_REPORT.md` in the
   root), SRS, design doc, both manuals, both videos, slides, Honour Declaration in the ZIP root.
   Unzip it on a clean folder and run the tests once before submitting.

---

## Suggested timeline

| By | Milestone | Who |
|---|---|---|
| Mon 12 Oct, 09:00 | Last chance for group changes; agree on this split | All |
| Fri 23 Oct | SRS draft + decisions list answered | A |
| Fri 30 Oct | Code changes done; design doc draft | C, B |
| Fri 6 Nov | Manuals draft; tests + coverage updated; slides outline | C, D |
| Fri 13 Nov | All documents final; cross-review done | All |
| Mon 16 – Wed 18 Nov | Record demo video and presentation | C, All |
| Thu 19 Nov | Build and check the ZIP | D |
| Fri 20 Nov, 20:00 | **Submit** | D |

**Dependencies:** A's requirement IDs feed the coverage report, user manual and slides. C's code
changes feed B's class diagram and D's tests. Raise any change in the group chat before merging.
