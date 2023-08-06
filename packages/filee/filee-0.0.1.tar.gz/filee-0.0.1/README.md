# filee

A command to save/load files from/to JSON.

```bash
$ filee load | python -m json.tool
{
    "children": [
        {
            "name": "README.md",
            "content": "# filee\n\nREADME\n",
            "too_big": false,
            "binary": false,
            "read_only": false,
            "changed": true,
            "children": null
        }
    ],
    "name": "",
    "content": null,
    "too_big": false,
    "binary": false,
    "read_only": false,
    "changed": true
}
```

## File tree JSON format

### Files

```json
{
    "name": "README.md",
    "content": "# filee\n\nREADME\n",
    "too_big": false,
    "binary": false,
    "read_only": false,
    "changed": true,
    "children": null
}
```

The content will be encoded by `FTREE_ENCODING`.
If files are binary file, they will be encoded by BASE64.

### Directory

```json
{
    "children": [
        { },
        { }
    ],
    "name": "dirname",
    "content": null,
    "too_big": false,
    "binary": false,
    "read_only": false,
    "changed": true
}
```

The `name` of root directory will be empty string (`''`).

## Load Command

`load` command loads data from file system and send it to the stdout as JSON.
The JSON will be formed as above file tree format.

```bash
$ filee load
```

* `--dir`: Target directory to load. default is current directory.
* `--etag`: Load only changed files.

### Etag behavior

By usinig `--etag` option, the command will return only changed files.
It will save hashes of each files in `FTREE_LOAD_FILE_HASHES` setting path,
and recognize files are changed from last loading or not.

```json
{
    "name": "README.md",
    "content": null,
    "too_big": false,
    "binary": false,
    "read_only": false,
    "changed": false,
    "children": null
}
```

This option can reduce the size of JSON output.

## Save Command

`save` command accepts JSON input from stdin, and saves files to your file system.
The JSON should be formed as above file tree format.

```bash
$ filee save
```

## Settings

You can specify settings for filee command by environment variables:

* `FTREE_ENCODING`: Save/Load encoding. default is `"utf-8"`
* `FTREE_MAX_SIZE`: Max file size (bytes) to load. default is 1MB.
* `FTREE_MAX_CHILDREN`Max number of children of directories. default is 50.
* `FTREE_MAX_DEPTH`: Max number of depth of directory tree. default is 20.
* `FTREE_LOAD_FILE_HASHES`: File path to save hashes of loading. default is `~/.fileeloadhashes`.
