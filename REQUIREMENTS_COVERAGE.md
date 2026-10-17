# Requirements Coverage Report (Deliverable 3e)

This report maps every user story and every SRS requirement to its implementation status.
Requirement IDs are taken from the SRS (`srs/COMP3211_PIM_SRS.docx`), version 0.4 (18 October 2026). Tests live in `tests/test_model.py`
and `tests/test_controller.py`; "Manual" means the requirement is checked by running the program, with no automated test.

**Summary:** 11 of 11 user stories are implemented. Every requirement in the table below is implemented: 59 functional (FR), 6 non-functional (NFR) and 7 constraints (CON).
Two scope questions are still open in SRS Section 6.14: whether US4 needs active alarm alerts, and whether US7 needs
field-specific search. If either answer is yes, the affected story becomes partially implemented.

## User stories

| User story | Description | Implemented | Where | SRS req IDs |
|---|---|---|---|---|
| US1 | Multiple PIR types in one place | Yes | `model/collection.py` `PIMCollection`; `model/records.py` | UR-01; FR-01–FR-14 |
| US2 | Create note | Yes | `model/records.py` `Note` | UR-02; FR-07, FR-08, FR-12–FR-14 |
| US3 | Create task | Yes | `Task` | UR-03; FR-07, FR-09, FR-12–FR-14 |
| US4 | Create event | Yes (alarm is stored and displayed, no active alert; see SRS 6.14) | `Event` | UR-04; FR-07, FR-10, FR-12–FR-14 |
| US5 | Create contact | Yes | `Contact` | UR-05; FR-07, FR-11–FR-14 |
| US6 | Modify PIR | Yes | `PIMCollection.modify`, `PIR.set` | UR-06; FR-15–FR-20 |
| US7 | Search with and/or/not, text, time, type | Yes (searches every text or time field; no field-specific search, see SRS 6.14) | `model/criteria.py`, `PIMCollection.search` | UR-07–UR-10; FR-21–FR-35 |
| US8 | Print one / all | Yes | controller `_cmd_print`, `PIR.__str__` | UR-11, UR-12; FR-36–FR-38 |
| US9 | Delete PIR | Yes | `PIMCollection.delete` | UR-13; FR-39–FR-41 |
| US10 | Save .pim | Yes | `model/storage.py` `save_pim` | UR-14; FR-42–FR-46 |
| US11 | Load .pim | Yes | `model/storage.py` `load_pim` | UR-15; FR-47–FR-52 |

## Functional requirements

| ID | Requirement (short) | Implemented | Where | Verified by |
|---|---|---|---|---|
| FR-01 | Unique positive integer IDs | Yes | `PIR.__init__`, `load_pim` | `test_bad_ids_rejected`; Manual |
| FR-02 | Text values preserved exactly | Yes | `check_text`, `PIR.to_dict` | `test_round_trip` |
| FR-03 | `YYYY-MM-DD HH:MM` format, invalid dates rejected | Yes | `parse_time` | `test_create_task_parses_deadline`, `test_invalid_time_rejected` |
| FR-04 | Minute-precision local time comparison | Yes | `TimeCriterion` | `test_time_before_after_equal` |
| FR-05 | All fields required; blank text rejected | Yes | `check_text`; `_cmd_create` count check | `test_blank_text_rejected` |
| FR-06 | ID and type not editable | Yes | `PIR.set` (`id`/`type` are not in `FIELDS`) | Manual |
| FR-07 | Four types in one collection | Yes | `PIMCollection.create` | `test_create_all_types` |
| FR-08 | `create note` | Yes | `Note`, `_cmd_create` | `test_create_all_types` |
| FR-09 | `create task` | Yes | `Task`, `_cmd_create` | `test_create_task_parses_deadline` |
| FR-10 | `create event` | Yes | `Event`, `_cmd_create` | `test_create_all_types` |
| FR-11 | `create contact` | Yes | `Contact`, `_cmd_create` | `test_create_all_types` |
| FR-12 | Case-insensitive type; unknown type / wrong count rejected | Yes | `_cmd_create`, `PIMCollection.create` | `test_create_unknown_type_raises`; Manual |
| FR-13 | Rejected creation leaves collection unchanged | Yes | Validation before `PIR.__init__` | `test_blank_text_rejected`; Manual |
| FR-14 | `Created ...` message | Yes | `_cmd_create` | Manual |
| FR-15 | `modify <id> <field> <value>` | Yes | `_cmd_modify` | Manual |
| FR-16 | Editable fields per type | Yes | `PIR.FIELDS`, `PIR.set` | `test_modify_field`, `test_modify_time_field`, `test_modify_unknown_field_raises` |
| FR-17 | Update preserves everything else | Yes | `PIR.set` | Manual |
| FR-18 | Missing ID error on modify | Yes | `PIMCollection.get` | Manual |
| FR-19 | Invalid value rejected, record unchanged | Yes | `PIR.set` | `test_blank_text_rejected` |
| FR-20 | `Updated ...` message | Yes | `_cmd_modify` | Manual |
| FR-21 | `type=` / `type = ` syntax, case-insensitive | Yes | `TypeCriterion`, `_Parser.parse_atom` | `test_type`, `test_spaced_and_glued_syntax` |
| FR-22 | `contains`, case-insensitive, any text field | Yes | `ContainsCriterion` | `test_contains` (case-insensitivity: Manual) |
| FR-23 | `time < > =`, any time field | Yes | `TimeCriterion` | `test_time_before_after_equal` |
| FR-24 | No eligible field means no match | Yes | `ContainsCriterion`, `TimeCriterion` | `test_time_before_after_equal` |
| FR-25 | `&&`, `\|\|`, `!` | Yes | `And/Or/NotCriterion` | `test_and_or_not` |
| FR-26 | Parentheses; precedence `!` > `&&` > `\|\|` | Yes | `_Parser` | `test_parentheses_and_precedence` |
| FR-27 | Lowercase keywords; literal symbols inside quotes | Yes | `_tokenize` | `test_operators_inside_quotes_are_literal` |
| FR-28 | Operator tokens; glued `(` and `!` | Yes | `_tokenize` | `test_spaced_and_glued_syntax` |
| FR-29 | Malformed criteria rejected | Yes | `parse_criterion`, `_Parser` | `test_bad_syntax_raises`, `test_unknown_time_operator_raises` |
| FR-30 | Unknown type name matches nothing | Yes | `TypeCriterion` | Manual |
| FR-31 | `contains ""` matches any record with text | Yes | `ContainsCriterion` | Manual |
| FR-32 | `!` inverts the full result | Yes | `NotCriterion` | `test_and_or_not` |
| FR-33 | Results once each, ascending ID | Yes | `PIMCollection.search`, `all` | Manual (tests compare sets, not order) |
| FR-34 | Newline-separated output; `No matching PIRs.` | Yes | `_cmd_search` | Manual |
| FR-35 | Search does not modify data | Yes | `PIMCollection.search` | Manual |
| FR-36 | `print <id>` shows all fields | Yes | `PIR.__str__` subclasses | `test_str_shows_all_fields` |
| FR-37 | `print all` ascending; `No PIRs stored.` | Yes | `_cmd_print` | Manual |
| FR-38 | Missing ID error on print | Yes | `PIMCollection.get` | Manual |
| FR-39 | `delete <id>` removes only that record | Yes | `PIMCollection.delete` | `test_delete` |
| FR-40 | Missing ID error on delete | Yes | `PIMCollection.delete` | `test_delete_missing_raises` |
| FR-41 | `Deleted PIR <id>` | Yes | `_cmd_delete` | Manual |
| FR-42 | `.pim` extension enforced (case-insensitive) | Yes | `_check_ext` | `test_wrong_extension` |
| FR-43 | Save preserves all records, including an empty collection | Yes | `save_pim` | `test_round_trip` |
| FR-44 | Save leaves collection unchanged | Yes | `save_pim` | Manual |
| FR-45 | `Saved ...` message; file errors reported | Yes | `_cmd_save`, `execute` | Manual |
| FR-46 | Overwrite without confirmation | Yes | `save_pim` (`open(..., "w")`) | Manual |
| FR-47 | Invalid files rejected with an error | Yes | `load_pim` | `test_corrupt_file`, `test_non_object_line_rejected` |
| FR-48 | Whole file validated (types, fields, values, unique IDs) | Yes | `load_pim`, `check_text`, `to_time` | `test_bad_ids_rejected`, `test_non_string_field_values_rejected` |
| FR-49 | Load replaces the collection | Yes | `_cmd_load` | Manual |
| FR-50 | Load preserves values; blank lines ignored | Yes | `load_pim` | `test_round_trip`, `test_blank_lines_ignored` |
| FR-51 | Failed load keeps prior collection | Yes | `_cmd_load` (assigns only on success) | Manual |
| FR-52 | `Loaded ...` message | Yes | `_cmd_load` | Manual |
| FR-53 | Case-insensitive verbs; empty input ignored | Yes | `CommandController.execute` | Manual |
| FR-54 | Unknown command message | Yes | `CommandController.execute` | Manual |
| FR-55 | `help` text | Yes | `HELP`, `_cmd_help` | Manual |
| FR-56 | `quit` / EOF / Ctrl+C end session | Yes | `_cmd_quit`, `run_cli` | Manual |
| FR-57 | Expected errors become `Error: ...` | Yes | `CommandController.execute` | Manual |
| FR-58 | Non-integer / missing ID errors | Yes | `CommandController._id`, `PIMCollection.get` | Manual |
| FR-59 | `Bad quoting` error | Yes | `CommandController._args` | Manual |

## Non-functional requirements and constraints

| ID | Requirement (short) | Implemented | Verified by |
|---|---|---|---|
| NFR-01 | Bad input never ends the session | Yes | Manual probe (SRS [S6]) |
| NFR-02 | Rejected operations preserve data | Yes | `test_blank_text_rejected`; Manual |
| NFR-03 | Save/load round trip preserves values | Yes | `test_round_trip` |
| NFR-04 | Model callable without terminal input | Yes | Whole unit suite (32 tests) |
| NFR-05 | Works offline | Yes | Inspection (no network imports) |
| NFR-06 | Errors give a reason; records show their fields | Yes | `test_str_shows_all_fields`; Manual |
| CON-01 | Command-line interface | Yes | `view/cli.py` |
| CON-02 | Supports US1–US11 | Yes | This report |
| CON-03 | Python | Yes | Inspection |
| CON-04 | Standard library only | Yes | Inspection (shlex, abc, json, datetime) |
| CON-05 | Model code in `model` package | Yes | Inspection |
| CON-06 | Automated model unit tests pass | Yes | 32 tests pass; see `COVERAGE_REPORT.md` |
| CON-07 | Requirements are valid, consistent, complete, realistic, verifiable | Yes | SRS review |

Many controller-level requirements (output messages, ID parsing, `help`, `quit`) are verified only manually, because
the unit suite targets the model package as the brief requires. Controller tests could be added to
`tests/test_controller.py` if the group wants automated evidence for them.
