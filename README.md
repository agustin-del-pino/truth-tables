# Logic Interpreter

Write a logic preposition and get its truth table.

# Overview

Let a `p & q` as logic preposition, tokenize and parse it, then interpret it and result with its Truth Table:

```shell
$ logic "p & q"

| p | q | p & q |
|---|---|-------|
| T | T |   T   |
| T | F |   F   |
| F | T |   F   |
| F | F |   F   |

```

# Process

There are three stages for interpret a logic preposition.

## Lexing the chars | Tokenization

The first stage is on charge of the Lexer. Takes the chars and convert into tokens.

The algorithm to use is the `Is contained in`. There are three kind of **containers**: Letters, Singles and Multiple.

The `Token-Types` and their containers are:

```yaml
WORD: "[aA-zZ]" # Letters
AND: "&" # Singles
OR: "|" # Singles
XOR: "#" # Singles
NOT: "~" # Singles
CONDITION-LEFT: "->" # Multiple
CONDITION-RIGHT: "<-" # Multiple
BI-CONDITION: "<->" # Multiple
```

So, for example, the preposition `p & q` it will tokenize as:

```ruby
(WORD:p)(AND:&)(WORD:q)
```

## Parsing the tokens | AST Construction

The second stage is on charge of the Parser. Takes the resulted tokens from the tokenization process and constructs an
Abstract Syntax Tree.

The algorithm to use for create the AST is the `E:T:F` _(Expression : Term : Factor)_. Very common for parse
mathematical expression.

The `Node-Types` based on the `Token-Type` and their delegations are:

```yaml
ATOM: # Factor
  - WORD
MOLECULE: # Term
  - AND
  - OR
  - XOR
PREPOSITION: # Expression
  - CONDITION-LEFT
  - CONDITION-RIGHT
  - BI-CONDITION
```

So, for example, the tokens: `(WORD:p)(AND:&)(WORD:q)` will be parse as:

```ruby
{
  type: MOLECULE
  token: (AND:&)
  children: [
    {
      type: ATOM
      token: (WORD:p)
    }
    {
      type: ATOM
      token: (WORD:q)
    }
  ]
}
```

## Creating the Logic Table | Interpretation

The third and final stage is on charge of the interpreter. Takes the AST and reads it, based on the Node-Type it will
create the logic table correspondent to that node.

The algorithm to use is the **Recursive Reading**. So, until the node is not a **primitive one** _(ATOM)_ the algorithm
it will called again. Because a table itself is the combinations of two _primitive tables_.

So, for example, AST of an AND it will interpret as:

```
NODE=AST-AND
INVERT=FALSE

T(N): The type of N

L[t](T1, T2): The logic table of kind 't' based on T1 and T2, both primitive logic tables

L'(N, INVERT): The primitive logic table of N inverted or not depending on INVERT

O(NODE, INVERT):
  ty=T(NODE)

  IF ty EQUALS TO 'AND':
    RETURN L[ty](
      O(NODE[0], INVERT),
      O(NODE[1], TRUE)
    )
  ...
  DEFAULT:
    RETURN L'(N, INVERT)
```

