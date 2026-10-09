# PIM System (COMP3211 project)

Command-line Personal Information Management system, Python 3 standard library only.

## Run
    python3 main.py          # start the CLI (type `help`)

## Test
    python3 -m unittest discover -s tests -t .
    # coverage (optional, third-party tool, not part of the product):
    # pip install coverage && coverage run --source=model -m unittest discover -s tests -t . && coverage report
    # latest results: COVERAGE_REPORT.md

## Layout (MVC)
    model/       PIR classes, search criteria, collection, .pim storage  (unit-tested)
    controller/  CommandController: parses commands, calls the model
    view/        console loop
    tests/       unittest tests for model/
    main.py      entry point

## Example session
    create note "buy milk"
    create task "submit SRS" "2026-11-20 20:00"
    search type=task && time < "2026-12-01 00:00"
    modify 1 text "buy bread"
    print all
    save my.pim
