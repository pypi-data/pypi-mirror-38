# Ernest

## What Ernest is
1. A CLI-based tool for making bulk changes to files via Python, partly achieved through syntax trees (for .py files, using [redbaron](https://github.com/PyCQA/redbaron)) and partly through regular expressions.
2. Useful if you're making a load of really boring changes that you can't really do with regexes alone (or only with regexes the length of War and Peace).
2. Named after the [Nitpicker](http://theadventurezone.wikia.com/wiki/Nitpicker) from The Adventure Zone.

It was made as part of a refactoring effort for a specific project and as such is pretty limited at the moment - it currently only contains methods for refactoring Python files but it is intended to be extensible.

## What Ernest isn't
1. A tool that will fix all your syntax problems. 
2. Pulling from any set of code standards - any new refactorings have to defined _manually_ (though you can pick and choose which ones to apply).
3. Particularly reliable.

## Installation

```sh
pip install ernest
```

## Configuration
You can override the defaults by making a JSON config file. By default Ernest looks in `~/.config/ernest/ernest.json` but you can specify a different json file using the `--config` option.

```json
{
  "name": "",  // the name of the project - used in headers
  "header": [  // added at the top of python files
    "#!/usr/bin/env python",
    "# encoding: utf-8",
    "This file is part of the {} project",  // example of how the name is used
    ""
  ],
  "imports": {  // checks python imports
    "exclude": [],  // do not allow these ever
    "conditional_exclude": {},  // do not allow these submodules from the main module, e.g. {'ernest': 'models'} excludes 'ernest.models' but allows 'ernest.helpers'
    "conditional_include": {}  // allow only these submodules from the main module, e.g. {'ernest': 'models'} allows 'ernest.models' but not 'ernest.helpers'
  }
}
```

You can find an example of the config file in the [data](data/ernest.json) folder.

## Usage
### Quickstart
```bash
ernest /project/path fix py
```

### General Options
```sh
--config /path/to/config
--name "My Project"
```

### Subcommands
#### `stats`
```bash
ernest [--config /path/to/config] [--name "My Project"] [/path/to/dir] stats [filetypes]
```

Show statistics for all files:
```bash
ernest /path/to/dir stats
```

Stats for just (e.g.) `txt` and `md` files:
```bash
ernest /path/to/dir stats txt md
```

#### `fix`
```bash
ernest [--config /path/to/config] [--name "My Project"] [/path/to/dir] fix [filetype] [fix(es)]
```

Run all fixes for `.py` files:
```bash
ernest /path/to/dir fix py all
```

Run the _literal string quote_ and _docstring quote_ fixes for `.py` files:
```bash
ernest /path/to/dir fix py literal docstring
```

## Contributing
Please feel free to fork, submit pull requests, etc.! It doesn't have to be limited to Python files - that's just how Ernest processes the text.
