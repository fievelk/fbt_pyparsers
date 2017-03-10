# FBT Python parsers

## Requirements
- python `2.7`, `3.4` or `3.5`
- python packages:
  - [`requests`](http://docs.python-requests.org)
  - [`pyquery`](https://github.com/gawel/pyquery)
  - [`langdetect`](https://github.com/Mimino666/langdetect)

## Run the parser

```bash
python post_language.py
```

## Options

When running `post_language.py` from command line, you can use the following arguments:

- `-h`, `--help`: View help
- `-d`, `--debug`: Activate debug mode
- `-v`, `--verbose`: Activate verbose mode
- `-r`, `--repeat`: Set value for `repeat`
- `-u`, `--url`: Set base URL for API requests
