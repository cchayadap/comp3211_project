# SRS changes: version 0.2 (Word file) → version 0.4 (`srs/SRS.md`)

The shared Word file `COMP3211_PIM_SRS.docx` is still version 0.2. This list gives every change needed to bring it up to
version 0.4. The full updated text of each section is in `srs/SRS.md`; copy from there when a change says "replace".

**Why it changed:** version 0.2 had reviewed only three code files. Version 0.3 checked the whole repository and ran
edge cases. That turned up five bugs (GAP-01 to GAP-05), which version 0.4 fixed in the code, with tests.

Changes are marked **[Must]** (content: wrong or missing in 0.2) or **[Wording]** (clearer text with the same meaning;
optional).

---

## Cover and Preface

1. **[Must] Document control:** Version `0.2` → `0.4`. Date `1 November 2026` → `18 October 2026` (0.2 had a date
   later than its own version history). Members: add the other members and student IDs.
2. **[Must] 1.2 Version History:** add two rows before the `1.0` row:
   - `0.3 | 18 October 2026 | Reviewed the full repository (records.py, storage.py, view/cli.py, main.py, tests) and probed edge cases by execution. Updated evidence labels; added the Tested and Gap labels; revised FR-42 (extension check is case-insensitive); documented the .pim encoding and path handling; added Section 6.13 Known Implementation Gaps; closed review items that only required inspection.`
   - `0.4 | 18 October 2026 | Fixed GAP-01 to GAP-05 in the code with a regression test for each (32 tests pass, 100% model line coverage). Updated the affected evidence labels; Section 6.13 now records the fixes.`
3. **[Must] 1.3 Evidence label table:** replace all four rows with:

   | Evidence label | Meaning |
   |---|---|
   | Tested | Behaviour confirmed by execution: an automated test in `tests/` or a recorded manual probe [S6]. |
   | Reviewed | Behaviour confirmed by source inspection [S4]; not separately executed. |
   | Partial | Part of the requirement is satisfied; the unsatisfied part is stated. |
   | Gap | The current implementation contradicts the intended rule; tracked in Section 6.13 until fixed. |
   | Clarification | An interpretation must be settled before baseline approval (Section 6.14). |

   *Proposed* is removed: no requirement uses it any more.
4. **[Wording] 1.3 first paragraph:** '"Should" identify desirable behaviour' → '"Should" identifies desirable behaviour'. In the paragraph under the table, drop the
   sentence "Source references [S1]–[S5] are defined in Section 1.4." (there is now an [S6]).
5. **[Must] 1.4 Source Basis:** replace [S4] and [S5], and add [S6]:
   - [S4] `Project repository at commit 83554f6 plus the version 0.4 gap fixes: model/ (records.py, collection.py, criteria.py, storage.py), controller/commands.py, view/cli.py, main.py, tests/test_model.py, tests/test_controller.py.`
   - [S5] `COVERAGE_REPORT.md and REQUIREMENTS_COVERAGE.md in the repository.`
   - [S6] `Manual edge-case probe of the controller and storage, 18 October 2026, Python 3.14 on Windows 11. Re-run after the version 0.4 fixes: all probes return error messages and none terminates the session. The unit suite (32 tests) passed in the same environment.`

## 2. Introduction

6. **[Must] 2.2 Scope, second paragraph:** say what the code does now and fix the section number:
   "Events store an alarm timestamp. The current implementation stores and displays it but raises no active alert.
   Whether US4 requires active alerting remains open (Section **6.14**)."
7. **[Must] 2.3:** add "The implementation has been executed on Python 3.14 under Windows 11 [S6]." Replace
   "Specific interpreter version … developer manual" with "The minimum supported interpreter version shall be stated
   in the developer manual."
8. **[Wording] 2.2 first paragraph and 2.4:** shortened. 2.4 is now a bullet list with the same content.

## 3. Glossary

9. **[Must] Record ID:** "Integer identifier used to select a record. New IDs come from a process-wide counter that
   only increases, so an ID is never reused within a session."
10. **[Must] .pim file:** "A local file used to persist records. The implementation uses UTF-8 JSON Lines (Section 6.10)."

## 4. User Requirements

11. **[Must] 4.3 Constraints:** add a **Status** column:
    CON-01 Reviewed (`view/cli.py`); CON-02 See Section 6.12; CON-03 Reviewed;
    CON-04 Reviewed (imports: shlex, abc, json, datetime); CON-05 Reviewed; CON-06 Tested (32 tests pass [S6]); CON-07 —.
    CON-03 wording: "this project anticipates Python" → "this project uses Python".
12. **[Wording] 4.2:** the paragraph under the table is reduced to "These expectations are refined into verifiable
    requirements in Section 6.11."

## 5. System Architecture

13. **[Must] 5.1:** heading "Anticipated MVC Organisation" → "MVC Organisation". Replace the paragraph: the view and
    startup code are now verified (banner, `pim> ` prompt, prints non-empty replies; `main.py` starts the loop).
    Remove "View and startup behaviour have not been verified."
14. **[Must] 5.2 table:** remove every "unreviewed"/"reviewed" note from the Modules column. View row: add "ends on
    `quit`, end-of-file, or Ctrl+C at the prompt". Tests row: "Verify model and controller behaviour without terminal
    interaction. | `tests/test_model.py` (31 tests), `tests/test_controller.py` (1 test)".
15. **[Must] 5.3:** the standard-library list becomes shlex, abc, json, and datetime (0.2 listed only shlex and abc).
    Remove "intentionally avoids prescribing internal storage encoding".

## 6. System Requirements

16. **[Must] 6.1:** replace the paragraph under the type table with: "Field names are taken from each class's
    `FIELDS` table in `records.py` and match the controller help text. Mobile numbers are stored as text to preserve
    leading zeros and formatting symbols."

### Requirement text changes (the "shall" sentence itself)
17. **[Must]** Replace the requirement text for these rows (copy it from `srs/SRS.md`):

| ID | Change |
|---|---|
| FR-16 | Add: "Field names are case-sensitive." |
| FR-21 | Add: "Mixed spacing such as `type= note` or `type =note` is rejected." |
| FR-27 | Fix the missing comma: "keywords `type`, `contains`, and `time`". |
| FR-34 | Message is `No matching PIRs.` (with a full stop). |
| FR-37 | Was missing its verb: "`print all` shall display all records in ascending ID order. An empty collection shall return `No PIRs stored.`" |
| FR-42 | **Revised:** "…to a file whose name ends in `.pim`, compared case-insensitively (`.PIM` is accepted). Other extensions shall be rejected." (0.2 said lowercase only; the code accepts either case.) |
| FR-47 | Add "with an error message" at the end. |
| FR-50 | Add: "Blank lines are ignored." |
| FR-54 | Exact message: `Error: unknown command '<verb>'. Type 'help'.` |
| FR-56 | "`quit` shall stop the session and return `Bye.` End-of-file or Ctrl+C at the prompt shall also end the session. …" |
| FR-59 | Error text is `Bad quoting`. |

### Evidence column
18. **[Must]** Update the Evidence column of every FR/NFR. Where the new label has an explanation, copy it from
    `srs/SRS.md`.

| ID | 0.2 | 0.4 |
|---|---|---|
| FR-01 | Proposed | Tested (+ note) |
| FR-02, FR-03 | Proposed | Tested (FR-03 + note) |
| FR-04 | Proposed | Reviewed |
| FR-05 | Proposed | Tested (+ note) |
| FR-06 | Proposed | Reviewed (+ note) |
| FR-07–FR-11 | Partial | Tested |
| FR-12 | Reviewed | Tested |
| FR-13 | Proposed | Reviewed (+ note) |
| FR-16 | Partial | Tested |
| FR-17 | Proposed | Reviewed |
| FR-18 | Reviewed | Tested |
| FR-19 | Proposed | Tested (+ note) |
| FR-21, FR-25–FR-28 | Reviewed | Tested |
| FR-22, FR-23 | Partial | Tested |
| FR-29 | Reviewed | Tested (+ note) |
| FR-34 | Reviewed | Tested |
| FR-35 | Partial | Reviewed |
| FR-36 | Partial | Tested |
| FR-39, FR-40 | Reviewed | Tested |
| FR-42, FR-43 | Proposed | Tested |
| FR-44, FR-46 | Proposed | Reviewed |
| FR-45 | Partial | Reviewed |
| FR-47, FR-48 | Proposed | Tested (+ note) |
| FR-50 | Proposed | Tested |
| FR-51 | Partial | Reviewed (+ note) |
| FR-54, FR-58 | Reviewed | Tested |
| FR-57 | Reviewed | Reviewed (+ note) |
| NFR-01 | Partial | Tested |
| NFR-02 | Proposed | Reviewed |
| NFR-03 | Proposed | Tested |
| NFR-04 | Partial | Tested (32 tests) |
| NFR-05 | Proposed | Reviewed (no network modules imported) |
| NFR-06 | Partial | Reviewed |

All other rows keep their 0.2 label.

### Notes under the tables
19. **[Must] 6.5:** add the record formats under the table: `[id] Note: <text>`; `[id] Task: <description> (deadline <time>)`;
    `[id] Event: <description> (start <time>, alarm <time>)`; `[id] Contact: <name>, <address>, mobile <mobile>`.
20. **[Must] 6.7:** add: "The destination is truncated before records are written, so an interrupted save can leave a
    partial file. Atomic replacement is not currently required (Section 6.14)."
21. **[Must] 6.8:** replace the note under the table. The empty-collection file is a zero-byte file, and loading
    advances the ID counter past the highest loaded ID. Delete the sentence about duplicate IDs and `collection.add`,
    because duplicates are now rejected.
22. **[Wording] 6.4:** the paragraph under the table is reworded; same content.

### 6.10 External Interface
23. **[Must] Replace the three bullets with the four in `srs/SRS.md`:**
    - **Paths:** quotes are not stripped, so `save "my records.pim"` is rejected. Unquoted paths with spaces work: `save my records.pim`.
    - **File format** (new): UTF-8 JSON Lines, one object per record with `type`, `id`, and the type's fields; times as `"YYYY-MM-DD HH:MM"`; written in ascending ID order.
    - **Command processing:** modify field names are case-sensitive (0.2 said "passed unmodified").

### 6.11 Non-Functional
24. **[Must]** Evidence column per the table in item 18. Replace the last paragraph's final sentence with "Measured
    results belong in the test and coverage deliverables [S5]."

### 6.12 Traceability
25. **[Must] 6.12 table:** add a **Status** column. Every story is "Implemented", except:
    US4 "Implemented as storage; alarm clarification open"; US7 "Implemented; field-specific scope open".
26. **[Must] 6.12.1:** in the "Aggregate event time" scenario, use full timestamps: start `2026-10-20 10:00`, alarm
    `2026-10-20 08:00`, `search time < "2026-10-20 09:00"`. In "Invalid load", the expected outcome becomes
    "Error message; session continues; prior collection unchanged."

### New section 6.13, and old 6.13 renumbered
27. **[Must] Insert a new section 6.13 "Known Implementation Gaps"** before the old 6.13. Copy the table from
    `srs/SRS.md`. It lists GAP-01 to GAP-05, each with the behaviour before the fix, the fix, the regression test, and
    status "Fixed".
28. **[Must] Renumber the old 6.13 to 6.14** and update the Table of Contents. Replace its table:
    - **Remove** "Record validation and IDs", "Storage", "Session behaviour", "Controller constructor": done or fixed.
    - **Keep** "Alarm behaviour / US4" (add: decide whether an alarm later than the start time should be rejected),
      "Aggregate search / US7", "Search operand strictness", "Quoted file paths and whitespace", "Metadata and environment".
    - **Add** "Date/time strictness": decide whether `2026-1-5 9:5` (no zero padding) stays accepted.
    - **Add** "Save atomicity": decide whether `save` must write to a temp file first.
    - Add the line under the table: "*Closed in 0.3:* inspection of records.py, storage.py, view/cli.py and main.py."
29. **[Must] Cross-references:** every "Section 6.13" in 0.2 (in 2.2 and the paragraph under the 6.4 table) that means the open
    decisions now points to **6.14**.
