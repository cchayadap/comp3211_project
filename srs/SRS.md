# Software Requirements Specification
## Command-Line Personal Information Management System

| Document control | Details |
|---|---|
| Course | COMP3211 Software Engineering |
| Group | 1 |
| Members | HAN Jiayi 24102151D; [remaining members and student IDs] |
| Version | 0.4 |
| Date | 18 October 2026 |

### Table of Contents
1. Preface — 1.1 Purpose and Intended Readership · 1.2 Version History · 1.3 Conventions and Evidence · 1.4 Source Basis
2. Introduction — 2.1 Objectives · 2.2 Scope · 2.3 Users and Operating Context · 2.4 Assumptions and Boundaries
3. Glossary
4. User Requirements Definition — 4.1 Functional · 4.2 Non-Functional · 4.3 Product and Process Constraints
5. System Architecture — 5.1 MVC Organisation · 5.2 Distribution of Responsibilities · 5.3 Rationale and Reuse
6. System Requirements Specification — 6.1 Record Data and Validation · 6.2 Creation · 6.3 Modification · 6.4 Search Criterion Definition · 6.5 Record Display · 6.6 Deletion · 6.7 Saving · 6.8 Loading · 6.9 General Command Behaviour · 6.10 External Interface Specification · 6.11 Detailed Non-Functional Requirements · 6.12 Traceability and Verification · 6.13 Known Implementation Gaps · 6.14 Baseline Review and Unresolved Decisions

---

## 1. Preface

### 1.1 Purpose and Intended Readership
This document specifies the services and constraints of the PIM system. It is intended for users reviewing its capabilities, developers implementing it, testers verifying it, and the instructor and assessors evaluating it. It provides the baseline for the separate design document, implementation, tests, and coverage report. It describes what the system shall do, with only a high-level architecture.

### 1.2 Version History
| Version | Date | Changes and remarks |
|---|---|---|
| 0.1 | 13 October 2026 | Initial lecture-aligned draft with proposed interactions. |
| 0.2 | 14 October 2026 | Revised command names, positional creation, single-field modification, case-insensitive aggregate search, and load replacement using supplied code; separated evidence from unverified rules. |
| 0.3 | 18 October 2026 | Reviewed the full repository (records.py, storage.py, view/cli.py, main.py, tests) and probed edge cases by execution. Updated evidence labels; added the *Tested* and *Gap* labels; revised FR-42 (extension check is case-insensitive); documented the .pim encoding and path handling; added Section 6.13 Known Implementation Gaps; closed review items that only required inspection. |
| 0.4 | 18 October 2026 | Fixed GAP-01 to GAP-05 in the code with a regression test for each (32 tests pass, 100% model line coverage). Updated the affected evidence labels; Section 6.13 now records the fixes. |
| 1.0 | [Approval date] | [Record group-approved changes and resolved decisions.] |

### 1.3 Conventions and Evidence
"Shall" identifies required behaviour in the approved baseline. "Should" identifies desirable behaviour. UR identifies user requirements, FR functional requirements, NFR quality requirements, and CON project constraints. Every detailed requirement has a source, rationale, and verification method. All requirements have mandatory priority after approval unless explicitly noted as pending clarification.

| Evidence label | Meaning |
|---|---|
| Tested | Behaviour confirmed by execution: an automated test in `tests/` or a recorded manual probe [S6]. |
| Reviewed | Behaviour confirmed by source inspection [S4]; not separately executed. |
| Partial | Part of the requirement is satisfied; the unsatisfied part is stated. |
| Gap | The current implementation contradicts the intended rule; tracked in Section 6.13 until fixed. |
| Clarification | An interpretation must be settled before baseline approval (Section 6.14). |

Evidence labels describe the state of the code at the commit cited in [S4]. They are not a substitute for the required implementation coverage report. Missing functionality shall remain a tracked gap rather than being removed solely to match current code.

### 1.4 Source Basis
| Reference | Source |
|---|---|
| [S1] | COMP3211 Course Project Description, Fall 2026: Deliverables 1, 3, and 4; Appendix B US1–US11. |
| [S2] | Lecture 04: Requirements Engineering, especially slides 4, 8–12, 27, 30–33, 35–38. |
| [S3] | Lecture 06: Architectural Design, MVC overview and organisation, slides 10–12. |
| [S4] | Project repository at commit `83554f6` plus the version 0.4 gap fixes: `model/` (records.py, collection.py, criteria.py, storage.py), `controller/commands.py`, `view/cli.py`, `main.py`, `tests/test_model.py`, `tests/test_controller.py`. |
| [S5] | `COVERAGE_REPORT.md` and `REQUIREMENTS_COVERAGE.md` in the repository. |
| [S6] | Manual edge-case probe of the controller and storage, 18 October 2026, Python 3.14 on Windows 11. Re-run after the version 0.4 fixes: all probes return error messages and none terminates the session. The unit suite (32 tests) passed in the same environment. |

## 2. Introduction

### 2.1 Objectives
Users need to capture quick notes, organise tasks and deadlines, record scheduled events, and maintain contact details. Managing these record types in one application reduces fragmentation and supports retrieval. The PIM system provides creation, modification, search, display, deletion, saving, and loading, as specified by US1–US11 [S1].

### 2.2 Scope
The application manages notes, tasks, events, and contacts through a command-line interface. It provides create, modify, search, print, delete, save, load, help, and quit commands. Search supports type filtering, substring matching, time comparison, and Boolean combinations. Records persist in local `.pim` files. Network services, user logins, and graphical interfaces are out of scope.

Events store an alarm timestamp. The current implementation stores and displays it but raises no active alert. Whether US4 requires active alerting remains open (Section 6.14).

### 2.3 Users and Operating Context
The user types terminal commands and supplies local file paths. The operating environment is Python 3 (standard library only) on a desktop operating system, with one user and one running instance. The implementation has been executed on Python 3.14 under Windows 11 [S6]. The minimum supported interpreter version shall be stated in the developer manual. The application interacts only with the local terminal and file system.

### 2.4 Assumptions and Boundaries
- The user has permission to read and write the files they name.
- Active records are held in memory for the duration of a session.
- Data is written to disk only when the user runs `save`; there is no automatic saving.
- Concurrent access to the same file by several instances is out of scope.
- Encryption, access control, background alarm scheduling while the application is closed, and crash recovery are out of scope.

These boundaries do not reduce the obligations on input validation and record integrity.

## 3. Glossary
| Term | Definition |
|---|---|
| PIM | Personal Information Management System. |
| PIR | Personal Information Record: note, task, event, or contact. |
| Active collection | Records currently held by the application. |
| Record ID | Integer identifier used to select a record. New IDs come from a process-wide counter that only increases, so an ID is never reused within a session. |
| Note | A record containing plain text. |
| Task | A record containing a description and deadline. |
| Event | A record containing a description, starting time, and alarm time. |
| Contact | A record containing name, address, and mobile number. |
| Criterion | A Boolean condition evaluated against a record. |
| Text field | Note text; task/event description; contact name, address, or mobile number. |
| Time field | Task deadline or event starting/alarm time. |
| Aggregate search | A condition matches when any eligible field in a record satisfies it. |
| Atomic condition | A type, substring, or time condition before logical combination. |
| CLI | Command-line interface. |
| MVC | Model-View-Controller: separation of data operations, presentation, and interaction. |
| .pim file | A local file used to persist records. The implementation uses UTF-8 JSON Lines (Section 6.10). |
| Round trip | Saving a dataset and loading it again to compare preserved information. |

## 4. User Requirements Definition

### 4.1 Functional User Requirements
| ID | User requirement | Source / rationale |
|---|---|---|
| UR-01 | Users shall be able to manage the four supported record types in one system. | US1 — Centralise personal information. |
| UR-02 | Users shall be able to create plain text notes. | US2 — Capture quick notes. |
| UR-03 | Users shall be able to create tasks with descriptions and deadlines. | US3 — Manage to-do items. |
| UR-04 | Users shall be able to create events with descriptions, starting times, and alarms. | US4 — Manage schedules. |
| UR-05 | Users shall be able to create contacts with names, addresses, and mobile numbers. | US5 — Maintain contact details. |
| UR-06 | Users shall be able to modify information in existing records. | US6 — Keep information current. |
| UR-07 | Users shall be able to search by record type. | US7 — Select categories. |
| UR-08 | Users shall be able to search for a string contained in stored text fields. | US7 — Retrieve remembered information. |
| UR-09 | Users shall be able to search for times before, after, or equal to a supplied time. | US7 — Retrieve time-related information. |
| UR-10 | Users shall be able to combine search conditions using AND, OR, and NOT. | US7 — Express specific retrieval conditions. |
| UR-11 | Users shall be able to display detailed information about a selected record. | US8 — Inspect one item. |
| UR-12 | Users shall be able to display detailed information about all stored records. | US8 — Review the collection. |
| UR-13 | Users shall be able to delete a specified record. | US9 — Remove unwanted information. |
| UR-14 | Users shall be able to save records to a .pim file. | US10 — Preserve records for future sessions. |
| UR-15 | Users shall be able to load records from a previously saved .pim file. | US11 — Resume work on stored records. |

### 4.2 Non-Functional User Requirements
| ID | User-level expectation | Rationale |
|---|---|---|
| UNFR-01 | Rejected commands shall explain the reason for rejection. | Allow users to correct mistakes. |
| UNFR-02 | The session shall remain usable after ordinary invalid input. | Avoid disruption from input mistakes. |
| UNFR-03 | Saving and loading shall preserve stored record information. | Maintain accuracy across sessions. |
| UNFR-04 | Rejected data-changing operations shall preserve the existing collection. | Prevent partial or unintended changes. |
| UNFR-05 | Supported record-management operations shall work without network access. | Support local use. |

These expectations are refined into verifiable requirements in Section 6.11.

### 4.3 Product and Process Constraints
| ID | Constraint | Source | Status |
|---|---|---|---|
| CON-01 | The system shall provide command-line interaction. | S1 | Reviewed (`view/cli.py`) |
| CON-02 | The system shall support US1–US11. | S1 | See Section 6.12 |
| CON-03 | The implementation shall use Java or Python unless the instructor approves another language; this project uses Python. | S1/S4 | Reviewed |
| CON-04 | The application shall use only Python standard libraries. | S1 | Reviewed (imports: shlex, abc, json, datetime) |
| CON-05 | All code belonging to the system model shall be contained in the `model` package. | S1 | Reviewed |
| CON-06 | Model unit tests shall be automatically executable, state exercised functionality, assert expected results, and pass against the submitted implementation. | S1 | Tested (32 tests pass [S6]) |
| CON-07 | Requirements shall be valid, consistent, complete, realistic, and verifiable. | S1/S2 | — |

## 5. System Architecture

### 5.1 MVC Organisation
The project is organised into `model`, `controller`, and `view` packages [S4]. The view (`view/cli.py`) prints a banner, reads lines at the `pim> ` prompt, passes each line to the controller, and prints any non-empty reply. The controller (`controller/commands.py`) parses commands, calls the model, converts expected errors to text, and returns the response string. The model holds record classes, the collection, search criteria, and persistence. `main.py` starts the view loop. MVC is used as a high-level organising pattern [S3].

### 5.2 Distribution of Responsibilities
| Component | Responsibility | Modules |
|---|---|---|
| Model | Record definitions and time parsing; collection operations; search criteria and parser; persistence. | `model/records.py`, `collection.py`, `criteria.py`, `storage.py` |
| Controller | Interpret commands, call the model, convert expected errors to text, and assemble textual responses. | `controller/commands.py` |
| View | Terminal prompt, input and output; session loop; ends on `quit`, end-of-file, or Ctrl+C at the prompt. | `view/cli.py` |
| Entry point | Start the system. | `main.py` |
| Tests | Verify model and controller behaviour without terminal interaction. | `tests/test_model.py` (31 tests), `tests/test_controller.py` (1 test) |

Interaction flows from the user through the view to the controller and the model, with results returned through the controller to the view. Record formatting is done by each record's `__str__` and message assembly by the controller, so formatting is not delegated exclusively to the view. Detailed class interfaces and collaboration diagrams belong in the design document.

### 5.3 Rationale and Reuse
Separating model operations supports independent unit tests and limits coupling between stored data and terminal interaction. Keeping the model in its own package is traceable to CON-05. The implementation reuses only standard-library modules: `shlex` (argument splitting), `abc` (abstract record and criterion bases), `json` (persistence), and `datetime` (time values). No third-party component is used.

## 6. System Requirements Specification

### 6.1 Record Data and Validation
| Type | Required user fields | Search eligibility |
|---|---|---|
| Note | text | Text: text; time: none |
| Task | description, deadline | Text: description; time: deadline |
| Event | description, start, alarm | Text: description; time: start and alarm |
| Contact | name, address, mobile | Text: name, address, mobile; time: none |

Field names are taken from each class's `FIELDS` table in `records.py` and match the controller help text. Mobile numbers are stored as text to preserve leading zeros and formatting symbols.

#### 6.1.1 Common Data Rules
Source: US1–US6. Rationale: Unambiguous fields and identifiers support safe record selection.

| ID | Requirement | Evidence | Verification |
|---|---|---|---|
| FR-01 | The system shall assign each record a unique positive integer ID within the active collection. IDs shall be retained by modification. | Tested — newly created records receive unique positive IDs that are never reused; duplicate, non-positive, and non-integer IDs in a file are rejected. | Create several records; compare IDs and edit one. |
| FR-02 | The system shall preserve supplied text and mobile values after command decoding, including spaces, case, leading zeros, and supported symbols. | Tested | Create, save, and reload representative text values. |
| FR-03 | The system shall accept date/time input in YYYY-MM-DD HH:MM format and reject nonexistent calendar dates or times. | Tested — non-zero-padded input such as `2026-1-5 9:5` is also accepted and displayed normalised (Clarification, Section 6.14). | Test valid values, invalid dates, and invalid hours. |
| FR-04 | Time comparisons shall use local wall-clock values at minute precision; timezone offsets are not part of the accepted input. | Reviewed | Test earlier, later, and identical minute values. |
| FR-05 | Every required field shall be supplied; blank or whitespace-only required text shall be rejected. | Tested — field count is enforced; blank and whitespace-only text is rejected on create, modify, and load. | Test omitted values and blank strings. |
| FR-06 | Record IDs and types shall not be editable through modification. | Reviewed — `id` and `type` are rejected as unknown fields. | Attempt modification of id and type. |

### 6.2 Creation
Source: US1–US5. Rationale: Capture every required record type with predictable argument handling.

| ID | Requirement | Evidence | Verification |
|---|---|---|---|
| FR-07 | The system shall support creation of notes, tasks, events, and contacts in the same collection. | Tested | Create and retrieve one of each. |
| FR-08 | `create note` shall accept one positional text value and create a note containing it. | Tested | Create notes and inspect fields. |
| FR-09 | `create task` shall accept description followed by deadline and create a task containing both. | Tested | Create and inspect a task. |
| FR-10 | `create event` shall accept description, starting time, and alarm time in that order. | Tested | Create and inspect an event. |
| FR-11 | `create contact` shall accept name, address, and mobile number in that order. | Tested | Create and inspect a contact. |
| FR-12 | Creation type names shall be case-insensitive; unsupported names and incorrect field counts shall produce errors. | Tested | Test uppercase types, unknown type, and wrong counts. |
| FR-13 | Rejected creation requests shall leave the active collection unchanged. | Reviewed — counts are checked before construction, and all field values are validated before an ID is assigned. | Compare before and after invalid creation. |
| FR-14 | Successful creation shall return a message beginning with `Created` followed by the record representation. | Reviewed | Inspect successful controller output. |

### 6.3 Modification
Source: US6. Rationale: Keep stored information current without affecting unrelated data.

| ID | Requirement | Evidence | Verification |
|---|---|---|---|
| FR-15 | `modify` shall accept a record ID, one field name, and one replacement value. | Reviewed | Test exact and incorrect argument counts. |
| FR-16 | The system shall allow modification of the fields listed for the selected type in Section 6.1. Field names are case-sensitive. | Tested | Test every editable field and an unknown field. |
| FR-17 | An update shall preserve the ID, record type, other fields, and other records. | Reviewed | Compare full collection before and after update. |
| FR-18 | A nonexistent modification ID shall produce an error without changing the collection. | Tested | Modify a missing ID and compare records. |
| FR-19 | An invalid replacement value shall be rejected without changing the record. | Tested — invalid times and blank text are rejected before assignment. | Attempt an invalid time and re-read the record. |
| FR-20 | Successful modification shall return a message beginning with `Updated` followed by the record representation. | Reviewed | Inspect successful output. |

### 6.4 Search Criterion Definition
Source: US7. Rationale: Allow users to express type, text, time, and combined conditions.

| ID | Requirement | Evidence | Verification |
|---|---|---|---|
| FR-21 | The system shall accept `type=<name>` and `type = <name>` as equivalent type conditions. Type values shall be case-insensitive. Mixed spacing such as `type= note` or `type =note` is rejected. | Tested | Compare both syntax forms and uppercase values. |
| FR-22 | `contains <string>` shall match a record when at least one text field contains the string, ignoring case. | Tested | Test every eligible text field and mixed case. |
| FR-23 | `time < <value>`, `time > <value>`, and `time = <value>` shall match when at least one time field satisfies the chronological comparison. | Tested | Test task deadlines and both event time fields. |
| FR-24 | A record with no eligible fields shall not satisfy the corresponding atomic text/time condition. | Reviewed | Evaluate criteria on records with no fields of that kind. |
| FR-25 | The system shall support `&&`, `\|\|`, and `!` for Boolean AND, OR, and NOT. | Tested | Test truth-table cases and nested NOT. |
| FR-26 | Parentheses shall control grouping; otherwise precedence shall be NOT, AND, then OR. Repeated AND/OR operations shall group left to right. | Tested | Test mixed and grouped expressions. |
| FR-27 | The search keywords `type`, `contains`, and `time` shall be lowercase; quoted substrings may contain literal parentheses and logical-operator characters. | Tested | Test keyword case and quoted symbols. |
| FR-28 | The operators `&&` and `\|\|` shall be separate tokens; parentheses and a leading `!` may adjoin neighbouring expression tokens. | Tested | Test spaced operators, grouped expressions, and `!type=note`. |
| FR-29 | The parser shall reject an empty criterion, unclosed quotation, invalid time operator, missing operand, unmatched grouping, or unexpected trailing token. | Tested — an unquoted operator token is accepted as an operand, e.g. `contains &&` (Clarification, Section 6.14). | Test malformed expressions. |
| FR-30 | For a syntactically accepted but unsupported type name, type matching shall return false; NOT shall invert that result. | Reviewed | Test `type=banana` and `!type=banana`. |
| FR-31 | An empty quoted substring shall match any record with at least one text field. | Reviewed | Evaluate `contains ""`. |
| FR-32 | Negation shall invert the complete Boolean result, including false due to no eligible fields. | Reviewed | Test `! time < "2026-11-01 09:00"` on a note. |

The grammar cannot select individual fields, so it cannot isolate deadlines from start or alarm times, or names from other text fields. For events, a match in any time field is sufficient. This limitation must be confirmed against the instructor's reading of US7 (Section 6.14). Keyword handling is not uniform: `SEARCH` is accepted as a command verb, but `CONTAINS` is not accepted as a criterion keyword.

#### 6.4.1 Search Execution
Source: US7. Rationale: Return an inspectable and consistently ordered result set.

| ID | Requirement | Evidence | Verification |
|---|---|---|---|
| FR-33 | The system shall evaluate the parsed criterion against every active record and return each matching record once in ascending ID order. | Reviewed | Search an out-of-order collection. |
| FR-34 | The search command shall return record representations separated by newlines; zero matches shall return `No matching PIRs.` | Tested | Test multiple and zero matches. |
| FR-35 | Searching shall not change stored records or the active collection. | Reviewed | Compare dataset before and after compound searches. |

### 6.5 Record Display
Source: US8. Rationale: Allow inspection of one or all records.

| ID | Requirement | Evidence | Verification |
|---|---|---|---|
| FR-36 | `print <id>` shall display the selected record ID, type, and all type-specific stored fields. | Tested | Inspect representation of every record type. |
| FR-37 | `print all` shall display all records in ascending ID order. An empty collection shall return `No PIRs stored.` | Reviewed | Test nonempty and empty collections. |
| FR-38 | A nonexistent print ID shall return an error without changing records. | Reviewed | Print a missing ID. |

Record formats: `[id] Note: <text>`; `[id] Task: <description> (deadline <time>)`; `[id] Event: <description> (start <time>, alarm <time>)`; `[id] Contact: <name>, <address>, mobile <mobile>`.

### 6.6 Deletion
Source: US9. Rationale: Remove a selected item without affecting other records.

| ID | Requirement | Evidence | Verification |
|---|---|---|---|
| FR-39 | `delete <id>` shall remove only the record identified by an existing ID. | Tested | Delete one of several records. |
| FR-40 | A nonexistent deletion ID shall return an error and preserve the collection. | Tested | Delete a missing ID. |
| FR-41 | Successful deletion shall return `Deleted PIR <id>`. | Reviewed | Check the successful output. |

### 6.7 Saving
Source: US10. Rationale: Preserve the active dataset for future sessions.

| ID | Requirement | Evidence | Verification |
|---|---|---|---|
| FR-42 | `save <path>` shall save the complete collection to a file whose name ends in `.pim`, compared case-insensitively (`.PIM` is accepted). Other extensions shall be rejected. *(Revised in 0.3; previously lowercase only.)* | Tested | Save valid, uppercase, and invalid extensions. |
| FR-43 | Saving shall preserve every record ID, type, and field value, and shall support an empty collection. | Tested | Round-trip all types and an empty collection. |
| FR-44 | Saving shall leave the active collection unchanged on success and failure. | Reviewed | Compare collection around save operations. |
| FR-45 | Successful saving shall return `Saved <count> PIR(s) to <path>`; file-operation errors shall produce an error message. | Reviewed | Save to valid and unwritable paths. |
| FR-46 | An existing destination shall be replaced on a successful save without interactive confirmation. | Reviewed | Save twice to the same path and inspect data. |

The destination is truncated before records are written, so an interrupted save can leave a partial file. Atomic replacement is not currently required (Section 6.14).

### 6.8 Loading
Source: US11. Rationale: Restore records without partially corrupting the active collection.

| ID | Requirement | Evidence | Verification |
|---|---|---|---|
| FR-47 | `load <path>` shall read a valid `.pim` file and reject unsupported extensions, unreadable files, and invalid content with an error message. | Tested — wrong extension, missing files, non-JSON lines, non-object JSON lines, unknown types, and missing or extra fields are rejected with an error message. | Test valid, missing, malformed, non-object, and wrong-extension files. |
| FR-48 | The complete file shall be validated for supported types, required fields, valid values, and unique IDs before active records are replaced. | Tested — types, field names, ID type, positivity, and uniqueness, text values (string, non-blank), and time values (string, valid format) are validated. The file is parsed into a new collection, which replaces the active one only if every line is valid. | Load files with a late invalid record, a duplicate ID, a negative ID, and a numeric field value. |
| FR-49 | A successful load shall replace, not merge with, the current collection; no interactive confirmation is required. | Reviewed | Load a disjoint dataset and verify replacement. |
| FR-50 | Loading shall preserve stored record IDs, types, and field values and accept a valid representation of an empty collection. Blank lines are ignored. | Tested | Compare loaded data with saved data. |
| FR-51 | A failed load shall preserve the prior active collection. | Reviewed — the file is parsed into a new collection before replacement, and every load failure is reported as an error message. | Fail a load and inspect the retained collection. |
| FR-52 | Successful loading shall return `Loaded <count> PIR(s) from <path>`. | Reviewed | Inspect successful output. |

The implementation's empty-collection file is a zero-byte file. Loading a file advances the ID counter past the highest loaded ID, so later creations do not collide with loaded records.

### 6.9 General Command Behaviour
Source: controller and view. Rationale: Make interactions predictable and errors recoverable.

| ID | Requirement | Evidence | Verification |
|---|---|---|---|
| FR-53 | Command verbs shall be case-insensitive. Empty or whitespace-only input shall return no message and perform no operation. | Reviewed | Test uppercase verbs and empty input. |
| FR-54 | An unknown command shall return `Error: unknown command '<verb>'. Type 'help'.` | Tested | Submit an unsupported command. |
| FR-55 | `help` shall display supported commands, their formats, editable fields, and a search example. | Reviewed | Compare help text to Section 6.10. |
| FR-56 | `quit` shall stop the session and return `Bye.` End-of-file or Ctrl+C at the prompt shall also end the session. No automatic save or unsaved-change confirmation is specified. | Reviewed | Quit after a change; verify the loop ends. |
| FR-57 | Expected `ValueError`, `KeyError`, and `OSError` failures shall be converted to messages beginning with `Error:`. | Reviewed — other exception types are not converted. No known input path raises one after the version 0.4 fixes. | Inject each expected error through model operations. |
| FR-58 | Record commands shall reject IDs that cannot be converted to integers. Nonexistent integer IDs shall report `No PIR with id <id>`. | Tested | Test non-integer and missing integer IDs. |
| FR-59 | Malformed quoting in `create` and `modify` shall produce a `Bad quoting` error. | Reviewed | Submit an unclosed quoted argument. |

### 6.10 External Interface Specification
| Operation | Accepted example |
|---|---|
| Create note | `create note "Revise Lecture 4"` |
| Create task | `create task "Finish SRS" "2026-11-01 18:00"` |
| Create event | `create event "Group meeting" "2026-10-20 15:00" "2026-10-20 14:45"` |
| Create contact | `create contact "Alex Chan" "Hong Kong" "+852 9123 4567"` |
| Modify | `modify 1 text "Revise Lecture 5"` |
| Search type | `search type=task` |
| Search text | `search contains "meeting"` |
| Search time | `search time < "2026-11-01 09:00"` |
| Search combined | `search (type=task && contains "hw") \|\| !type=note` |
| Display | `print 1` / `print all` |
| Delete | `delete 1` |
| Save/load | `save records.pim` / `load records.pim` |
| Help/quit | `help` / `quit` |

- **Tokenization and search.** `create` and `modify` use `shlex` splitting, so values containing spaces must be quoted. The criterion tokenizer accepts single and double quotes and decodes `\"` and `\\` inside double quotes. The whole search expression must not be wrapped in quotes, and field-specific syntax such as `deadline < ...` is not supported.
- **Paths.** `save` and `load` use the rest of the line, trimmed, as the path. Quotation marks are not stripped, so `save "my records.pim"` is rejected because the name ends in `.pim"`. Unquoted paths containing spaces work: `save my records.pim`.
- **File format.** A `.pim` file is UTF-8 JSON Lines: one JSON object per record, holding `type`, `id`, and that type's fields. Time values are written as `"YYYY-MM-DD HH:MM"`. Records are written in ascending ID order.
- **Command processing.** The verb is separated from its arguments by the first literal space, so a tab after the verb is not recognised as a separator. `print all` is case-insensitive. `modify` field names are case-sensitive. `help` and `quit` ignore extra arguments.

### 6.11 Detailed Non-Functional Requirements
| ID | Requirement | Category / verification | Evidence |
|---|---|---|---|
| NFR-01 | Invalid commands, invalid field values, invalid IDs, malformed search input, and ordinary file errors shall not terminate the session. | Reliability — test each category, then run a valid command. | Tested — re-probed after the version 0.4 fixes [S6]. |
| NFR-02 | Rejected create, modify, delete, and load operations shall preserve all previously active record values. | Data integrity — snapshot and compare the full dataset around failed operations. | Reviewed |
| NFR-03 | Saving and reloading valid data shall preserve all IDs, types, text, and time values. | Persistence accuracy — round-trip all record types with representative values. | Tested |
| NFR-04 | Collection, criterion, record-validation, and persistence operations shall be callable without interactive terminal input. | Testability — run automated model tests without user input. | Tested (32 tests) |
| NFR-05 | All required user operations shall function with network access disabled. | Offline operation — run an end-to-end local session with networking disabled. | Reviewed (no network modules imported) |
| NFR-06 | Error messages shall identify a rejection reason; displayed records shall identify their fields. | Usability — inspect representative invalid inputs and each record type. | Reviewed |

These requirements are testable without inventing response-time, capacity, availability, or coverage targets. No numeric performance requirement is committed until the group specifies a realistic workload and test environment. Measured results belong in the test and coverage deliverables [S5].

### 6.12 Traceability and Verification
| User story | User requirement IDs | System requirement coverage | Status |
|---|---|---|---|
| US1 | UR-01 | FR-01–FR-06; FR-07–FR-14 | Implemented |
| US2 | UR-02 | FR-07–FR-14 (note creation) | Implemented |
| US3 | UR-03 | FR-07–FR-14 (task creation) | Implemented |
| US4 | UR-04 | FR-07–FR-14 (event creation) | Implemented as storage; alarm clarification open |
| US5 | UR-05 | FR-07–FR-14 (contact creation) | Implemented |
| US6 | UR-06 | FR-15–FR-20 | Implemented |
| US7 | UR-07–UR-10 | FR-21–FR-32; FR-33–FR-35 | Implemented; field-specific scope open |
| US8 | UR-11–UR-12 | FR-36–FR-38 | Implemented |
| US9 | UR-13 | FR-39–FR-41 | Implemented |
| US10 | UR-14 | FR-42–FR-46 | Implemented |
| US11 | UR-15 | FR-47–FR-52 | Implemented |

Each FR includes a verification approach. Add test-case identifiers during test development. Traceability shows which obligations are covered, not that tests have passed. The final implementation coverage report shall map every user story and every approved requirement to implemented or not-implemented status [S1].

#### 6.12.1 Example Acceptance Scenarios
| Scenario | Action | Expected outcome |
|---|---|---|
| Creation/display | Create one of each supported type; `print all`. | Four records; all fields displayed; ascending IDs. |
| Case-insensitive text | Create a note containing `Meeting`; `search contains "meeting"`. | The note matches. |
| Aggregate event time | Create an event starting `2026-10-20 10:00` with alarm `2026-10-20 08:00`; `search time < "2026-10-20 09:00"`. | The event matches because of its alarm time. |
| Boolean precedence | With tasks and events containing different text, `search type=task \|\| type=event && contains "meeting"`. | All tasks plus only the matching events. |
| Missing ID | Modify, print, and delete an ID that is not present. | Errors; original dataset unchanged. |
| Persistence | Save all types; load the file into a different active collection. | Replacement collection preserves saved values. |
| Invalid load | Load malformed, non-object, or duplicate-ID data. | Error message; session continues; prior collection unchanged. |

### 6.13 Known Implementation Gaps
Version 0.3 found these gaps by inspection and confirmed them by execution [S6]. All were fixed in version 0.4. A regression test for each is listed below. No open implementation gaps remain.

| ID | Requirement(s) | Behaviour before the fix | Resolution (version 0.4) | Regression test | Status |
|---|---|---|---|---|---|
| GAP-01 | FR-05, FR-19 | `create note ""`, `create note "   "`, and blank replacement values were accepted. | `check_text` in `records.py` rejects blank and non-string text in every constructor and in `PIR.set`. Values are checked before an ID is assigned. | `TestRecords.test_blank_text_rejected` | Fixed |
| GAP-02 | FR-47, FR-51, FR-57, NFR-01 | A `.pim` line that was valid JSON but not an object (e.g. `"hello"`, `null`) raised an uncaught `AttributeError` and ended the session. | `load_pim` requires each line to be a JSON object and reports `Corrupt .pim file at line <n>` otherwise. | `TestStorage.test_non_object_line_rejected` | Fixed |
| GAP-03 | FR-01, FR-48 | Duplicate IDs in a file were accepted silently, with the later record winning. Negative, zero, or non-integer IDs were accepted. | `load_pim` rejects duplicate IDs and any ID that is not a positive integer (booleans are rejected). | `TestStorage.test_bad_ids_rejected` | Fixed |
| GAP-04 | FR-48, NFR-01 | Non-string field values (e.g. `"text": 5`, `"deadline": 5`) loaded, and a later `search` or `print` crashed the session. | `to_time` accepts only a `datetime` or a valid time string; `check_text` requires strings. Both are applied when loading. | `TestRecords.test_non_string_values_rejected`, `TestStorage.test_non_string_field_values_rejected` | Fixed |
| GAP-05 | Controller constructor | `CommandController(collection)` replaced a supplied empty collection, because an empty `PIMCollection` is falsy. | Uses an explicit `is not None` check. | `TestController.test_supplied_empty_collection_is_kept` | Fixed |

### 6.14 Baseline Review and Unresolved Decisions
| Issue | Required resolution before approval |
|---|---|
| Alarm behaviour / US4 | Confirm whether storing and displaying alarm times is enough. If active notifications are required, specify trigger precision, presentation, behaviour while the app is closed, and missed alarms. Also decide whether an alarm later than the event start should be rejected; it is currently accepted. |
| Aggregate search / US7 | Confirm that any-text-field and any-time-field criteria satisfy the expected scope. If field-specific selection is required, add grammar and requirements. |
| Date/time strictness | Decide whether non-zero-padded input (e.g. `2026-1-5 9:5`) remains accepted or is rejected. |
| Search operand strictness | The parser accepts unquoted operator tokens as operands (`contains &&`). Decide whether to keep or reject this, then document and test the rule. |
| Quoted file paths and whitespace | Decide whether to keep raw-path handling or strip quotes / use `shlex` for paths. Settle tab separators and extra-argument handling consistently. |
| Save atomicity | Decide whether `save` must write to a temporary file and replace the destination, so a failed save cannot leave a partial file. |
| Metadata and environment | Fill in member and group details and the minimum supported interpreter version; record group approval. |

*Closed in 0.3:* inspection of records.py (field accessors and `__str__` verified), storage.py (extension, overwrite, and encoding documented), and view/cli.py and main.py (session loop and exit paths verified).
