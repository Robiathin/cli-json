# CLI-JSON

A CLI tool for formatting JSON.

Example:

```
$ curl http://api.example.net/
{"hello":"world","a":["b","c", "d"],"e":{"f":"g"},"i":[{"j":"k"},{"l":"m"}]}
$ curl http://api.example.net/ | ./cli-json.py
{
    "a": [
        "b",
        "c",
        "d"
    ],
    "i": [
        {
            "j": "k"
        },
        {
            "l": "m"
        }
    ],
    "e": {
        "f": "g"
    },
    "hello": "world"
}
```

JSON can be read from a file using `./cli-json.py -f file`

The default indent is 4 spaces. This can be changed by adding the `-i` option. For example:

```
$ curl http://api.example.net/ | ./cli-json.py -i 3
...
```

The output can also be colored by adding the `-c` flag.

## Requirements

 - Python 2.X or 3.X
