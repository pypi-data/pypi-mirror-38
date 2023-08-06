# parapy
An automatic handling of parameter passing to python programs

## Usage
Import the script. Then in the top of your own document, define a list of tuples of all your parameters of the form ('name', 'prefix'/position, type), and then call the library using `params.params(Your_Parameters)`. This will return a dictionary of all the parameters of the form {'name' : value}.

The library supports prefixed parameters (i.e. whatever comes after '-i'), boolean parameters (i.e. if '-a' is passed) and positional parameters (i.e. the second parameter without a prefix).

Currently supported types are str, int, float and bool. Multi-word parameters _must_ be enclosed in quotes.

## Example
```
import params

parameters = [('output', '-o', str),   # A string parameter with prefix '-o'
              ('amount', '-n', int),   # An integer parameter with prefix '-n'
              ('verbose', '-v', bool), # A boolean parameter with name '-v'
              ('eggs', '-e', float),   # A float parameter with prefix '-e'
              ('input', 0, str),       # A string parameter position 0
              ('spam', 1, int),        # An integer parameter position 1
              ('message', '-m', str)]  # A string parameter with prefix '-m'


p = (params.params(parameters))

print(p)
```
Then calling the program with the parameters as such: ` python program.py -v gov_secrets.db -o elvis.mp3 4 -n 10 -m "Listen to this cool track!"`, will result in the following output:
```
{'output': 'elvis.mp3',
 'amount': 10,
 'verbose': True,
 'eggs': None,
 'input': 'gov_secrets.db',
 'spam': 4,
 'message': 'Listen to this cool track!'}
```

## TODO
- Add default values
