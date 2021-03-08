# CS 555 Agile Development

## Running

The main project source file is `project.py` which accepts the GED file to parse as an argument.

```shell
usage: project.py [-h] file
```

## Testing

Individual story tests can be run by executing unittest on them from the *project root directory*. For example:

```bash
python -m unittest tests.US01_TestDatesBeforeCurrent -v
```

To test an entire Sprint's suite of tests, you can use the included scripts directly. For example:

```bash
python Sprint01_Test.py
```

These scripts can be run from either within the tests directory or from the project root directory.