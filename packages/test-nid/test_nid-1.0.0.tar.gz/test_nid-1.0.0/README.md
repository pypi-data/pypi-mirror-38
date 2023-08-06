# Nano ID

A tiny, secure, URL-friendly, unique string ID generator for Python. Original implementation's repository: github.com/ai/nanoid

```python
import nanoid

nanoid.generate() # => NDzkGoTCdRcaRyt7GOepg
```

## Usage

### Normal

The main module uses URL-friendly symbols (A-Za-z0-9_-) and returns an ID with 21 characters (to have a collision probability similar to UUID v4).

```python
import nanoid

nanoid.generate() # => NDzkGoTCdRcaRyt7GOepg
```

Symbols -,.() are not encoded in the URL. If used at the end of a link they could be identified as a punctuation symbol.

If you want to reduce ID length (and increase collisions probability), you can pass the length as an argument.

```python
nanoid.generate(size=10) # => "IRFa-VaY2b"
```
Don’t forget to check the safety of your ID length in our ID collision probability calculator.

## Custom Alphabet or Length

If you want to change the ID's alphabet or length you can use the low-level generate module.

```python
from nanoid import generate

generate('1234567890abcdef', 10) # => "4f90d13a42"
```

Non-secure API is also available:

```python
from nanoid import fast_generate

fast_generate('1234567890abcdef', 10)
```

## Other Programming Languages

* [C#](https://github.com/codeyu/nanoid-net)
* [Clojure and ClojureScript](https://github.com/zelark/nano-id)
* [Crystal](https://github.com/mamantoha/nanoid.cr)
* [Dart](https://github.com/pd4d10/nanoid)
* [Go](https://github.com/matoous/go-nanoid)
* [Elixir](https://github.com/railsmechanic/nanoid)
* [Haskell](https://github.com/4e6/nanoid-hs)
* [Java](https://github.com/aventrix/jnanoid)
* [Nim](https://github.com/icyphox/nanoid.nim)
* [PHP](https://github.com/hidehalo/nanoid-php)
* [Python](https://github.com/puyuan/py-nanoid). Alternative Python implementation.
* [Ruby](https://github.com/radeno/nanoid.rb)
* [Rust](https://github.com/nikolay-govorov/nanoid)
* [Swift](https://github.com/antiflasher/NanoID)
