# CS 373 - Assignment a1

## Purpose

The first big idea of the course is **how text becomes something a computer can
act on.** A language has *syntax* — the notation you write — and *semantics* —
what that notation means. Getting from one to the other happens in three phases:

1. **Lexical analysis** (scanning) chops the character stream into tokens.
2. **Syntactic analysis** (parsing) assembles those tokens into a structure.
3. **Semantic analysis** walks that structure and does something.

This assignment is entirely about the first phase. That is not a warm-up before
the real material — scanning is where you learn that a language is a thing you
can *specify* rather than a thing you are handed, and everything after it is
built on that idea.

### Reading

From the [course textbook](https://ourplcc.github.io/course-materials-ng/dev/):
[Introduction](https://ourplcc.github.io/course-materials-ng/dev/00-introduction/),
[Overview](https://ourplcc.github.io/course-materials-ng/dev/01-overview/),
[Tokens](https://ourplcc.github.io/course-materials-ng/dev/02-tokens/), and
[PLCC](https://ourplcc.github.io/course-materials-ng/dev/03-plcc/). They are
short.

**Regular expressions.** The Tokens chapter assumes you can read and write them,
and so does question 3 — every rule you write there contains a pattern. You
should be able to look at a simple pattern and say which strings it matches, and
to write one that matches some strings and not others. No question asks for this
directly; it is what the rest of the assignment stands on.

If you are rusty, work [RegexOne](https://regexone.com/) lessons 1 through 9
before starting. It takes under an hour.

### What you will be able to do

1. **Explain how this course works.** What the syllabus commits to, and how
   your homework is scored.

2. **Place lexical analysis in the pipeline.** Distinguish a language's syntax
   from its semantics, say what scanning does, and say what it hands to the
   phase after it.

3. **Predict and construct regular expressions.** Given a pattern, say which
   strings it matches. Given strings that should match and strings that should
   not, write a pattern that separates them.

4. **Read, run, and extend a lexical specification.** Write `token` and `skip`
   rules, run `plcc-scan` in all three invocation modes — a file argument,
   interactively, and with input redirected — read what it prints, and add new
   tokens to a specification that already works.

6. **Explain what the scanner does when more than one rule could match.**

### The core concepts

These are what the Correctness criterion looks at. Details — a clumsy regex, an
awkward token name, a rule you could have written more simply — are worth a
comment from me but cost you nothing. These are what matter:

- **Syntax versus semantics**, and where lexical analysis sits between them.
- **Token versus lexeme.** A token is a category; a lexeme is the actual text
  that matched it. When `plcc-scan` prints `input:6:14 ID 'end99'`, `ID` is the
  token and `'end99'` is the lexeme — one of many different lexemes that same
  token will match.
- **`skip` versus `token`.** Both kinds of rule must *match* the input. The
  difference is only that a `skip` rule does not emit anything. Whitespace does
  not disappear because the scanner ignores it — it disappears because you
  wrote a rule that matches it and throws it away.
- **How ties are resolved.** The longest match wins. When two rules match the
  same longest text, the one written first wins. This is why a rule for a
  specific word has to appear *before* the general rule that would also match
  it.
- **What a lexical error is.** Not "the scanner got confused" — it is the
  specific situation where no rule matches at all, and it is the scanner
  correctly telling you your specification does not describe this input.

If you want to watch the tie-breaking happen rather than take my word for it,
run `plcc-scan -t input`. It prints every rule that matched, how long each match
was, and which one it picked. Question 3 puts this to work.

### Where this leads

A2 picks up the next two phases, on the same toolchain: you will write grammars
that turn tokens into structure, and semantics that walk that structure. The
specifications get longer but the workflow does not change, which is the other
reason this assignment spends its budget on getting the workflow solid.

On exams, this material shows up as questions you can only answer by having
built something — which strings a pattern matches, a pattern that separates two
sets, what a scanner does with an ambiguous input. Not by having memorized the
command names.

## How to do this assignment

**Your answers go in this file.** Every question has one or more `ANSWER`
blocks that look like this:

````
```
Replace this line with your answer.
```
````

Replace that line with your answer and leave the fences around it alone.

Files you write or edit go in the question's own directory — for this
assignment, that means `q3/`.

When you are done with the assignment follow these steps:

1. Go to the parent directory of `a1` (if you are working of a cloned copy of
   the GitHub class repository, it means `assignments`).
2. Zip the content of `a1`.
3. Submit the zip file to Google classroom.

## QUESTION 1 — How this course works

Read [grading.md](../../grading.md) — it is in the GitHub repository at the top
level. Then answer both parts. One or two sentences each.

**(a)** A student attempts every problem. Their work is complete and correct.
They submit their four days after the due date. What is the best score they can
earn out of 9, and which single criterion costs them the most?

### ANSWER

```
Each Criterion is worth 3 points but Criterion 3 seems the hardest since rather than being based on completeness or following formatting. It's built around correctness.
Late assignments after 3 days cannot earn correctness but can earn completeness.
```

**(b)** I leave a comment on your submission suggesting a cleaner way to write
one of your regexes. How many points does that comment cost you?

### ANSWER

```
Writing a unclean regex doesn't cost points.
```


## QUESTION 2 — Where scanning sits

Short answers. One or two sentences each.

**(a)** In your own words, what is a language's *syntax*, and what is its
*semantics*?

### ANSWER

```
Semantics is the meaning of the language, while syntax is the notation rules.
```

**(b)** Lexical analysis is the first of three phases. What does it produce,
and what consumes what it produces?

### ANSWER

```
Lexical analysis produces tokens which are then consumed by syntactic analysis.
```

**(c)** A token is an abstraction; a lexeme is an instance of it.

- Name a token that could have many different lexemes, and give **three**
  different lexemes it could match.
- Name a token that has exactly one possible lexeme, and say what makes it
  that way.

Draw both from the language you are about to build in question 3 — it is
described at the top of that question. The reading's examples do not count
here; the point is to find your own.

### ANSWER

```
A token called word which is defined in regex as [a-z]+ could contain lexeme, cat, dog, or lizard. ^cat$ will only have one lexeme, that being cat. This means this token can only be interpreted as cat with the exact txt cat.
```


## QUESTION 3 — Lab: build a scanner one rule at a time

This is a guided lab. Work the steps **in order** and answer as you go — the
later steps depend on what the earlier ones show you.

`q3/` contains these files.

- `spec.plcc` — empty. You will build it up over the course of this lab.
- `input` — sample input. **Do not modify.**
- `expected` — the output your finished scanner must produce. **Do not modify.**
- `input_extra`, `expected_extra` — used only in step 10. **Do not modify.**

`input` contains:

```
# example input
this that # the other thing
otherwise the thing
that is another thing
other#other#other#other
thisthat the end99 12345xxx _!
```

Position your terminal in `q3/` before you start. There is no compile step:
PLCC rebuilds the scanner whenever `spec.plcc` changes.

Follow the steps in this question to build a lexical specification that:

- skips whitespace,
- skips end-of-line comments that start with `#`,
- recognizes `this`, `that`, `the`, `other`, and `thing` as their own tokens,
- recognizes strings other than those five, containing only letters, digits,
  and underscores, as an `ID` token,
- and treats everything else as an error.

---

### Step 1 — Run it before you write anything

`spec.plcc` is empty. Run:

```bash
plcc-scan input
```

> **Type the filename exactly as `input`, from inside `q3/`.** `plcc-scan`
> labels every line of its output with the source name you handed it, so
> `plcc-scan ./input` prints `./input:` and running it from the directory above
> prints `q3/input:`. Step 9 compares your output against a file that says
> `input:`, so any other spelling will look like a total failure even when your
> specification is perfect. Tab-completion will often give you `./input` — watch
> for it.

**Report** the first three lines of output, and say in one sentence what an
empty specification does to the input.

#### ANSWER

```
input.txt:1:1: error: unrecognized character '#'
input.txt:1:2: error: unrecognized character ' '
input.txt:1:3: error: unrecognized character 'e'

A empty specification causes the program to not know what any of the characters are supposed to represent as tokens, it will spit out a error for each character.
---

### Step 2 — One rule

Put a single line in `spec.plcc`:

```
token ID '\w+'
```

Run it again. Some things are now tokens; a lot of it is still errors.

**Report** what is now recognized and what is not. Then answer: the spaces
between words were never something you wanted, so **why are they errors
rather than simply ignored?**

#### ANSWER

```
The regex is selecting numbers, letters, and underscores while ignoring spaces and hashes. There are errors because we never told the lexical analysis to not analyze certain characters. 
```

---

### Step 3 — Throw something away on purpose

Add a `WS` rule that skips whitespace. Run again.

**Report** what changed, and what is still an error.

#### ANSWER

```
Whitespaces are now being ignored but the hashes are still unrecognized.
```

---

### Step 4 — Comments

Add a `COMMENT` rule that skips a pound character `#` and all the characters
that come after it until the end of the line. Run again.

You should now get through the whole file with no errors except one, at the
very end. Every word should be coming out as an `ID`.

**Report** your two `skip` rules. Then answer: line 5 of the input is
`other#other#other#other` — how many tokens does it produce, and why?

#### ANSWER

```
skip COMMENT '#.*$'
skip WS '\s+'

other is one word, so it's a token, anything after the hash is ignored so the other others are not tokens

```


---

### Step 5 — Three ways to feed it

You have been giving `plcc-scan` a **file argument**. It takes its input two
other ways as well: **interactively** from the keyboard, and by
**redirection**. Try all three:

```bash
plcc-scan input          # file argument — what you have been doing
plcc-scan                # interactive; type a line, then press Ctrl-D
plcc-scan < input        # redirection
```

**Answer:** two of the three agree with each other and one differs, in the
same place on every line. Which one differs, what is different, and why does
that make sense?

#### ANSWER

```
I think the difference you're referring to is that plcc-scan and plcc-scan < input.txt both result in the -: being displayed rather than the file name. plcc-scan filename causes the actual filename to be displayed. 
```

Go back to `plcc-scan input` for the rest of the lab.

---

### Step 6 — Add the keywords in the wrong place first

Add five `token` rules for `this`, `that`, `the`, `other`, and `thing`, using
the token names `THIS`, `THAT`, `THE`, `OTHER`, and `THING`. Put all five
**below** your `token ID` rule.

**Predict before you run.** Write down what you expect the word `this` on line
2 to come out as. Then run it.

#### ANSWER — your prediction, then what actually happened

```
Prediction
The new tokens and old token will contest words, since they contest the same words, they are trying to select the same length of characters. This means that the old token, listed higher in the line of the plcc file will end up winning. Thus causing the tokens to all be IDs.

I was correct, this on line 2 came out as a ID token 

```

---

### Step 7 — Move them, and find out why it mattered

Move the five keyword rules **above** the `token ID` rule. Run again. The
keywords now come out as themselves.

But look at line 3. The word `otherwise` is still an `ID` — it did not become
`OTHER` followed by an `ID`. Two different things are going on, and this step
is about telling them apart.

Run the tracer. It prints a candidate table for **every** token in the file,
which is far more than fits on a screen, so send it somewhere you can scroll:

```bash
plcc-scan -t input > trace.txt
```

Open `trace.txt` and find these two blocks:

- the one beginning `Scanning input:2:1:` — that is the word `this`
- the one beginning `Scanning input:3:1:` — that is the word `otherwise`

Each block lists every rule that matched, how many characters it matched, and
marks the winner with `*`. **Look closely at which column the `*` lands in.**
It is not the same column in the two blocks, and that difference is the whole
point of this step.

**Answer both:**

**(a)** For the word `this`, two rules match and both match four characters.
Which rule wins, and what decides it?

**(b)** For the word `otherwise`, two rules also match. Which wins, and what
decides it *this* time? Would reordering your rules change this one?


#### ANSWER

```
a) Both match 4 characters so it's the order in the plcc file that decides which specification wins

b) Otherwise is longer, thus ID token wins rather than OTHER token, reordering rules would not change this
```

---

### Step 8 — The error at the end

The input ends with `_!`.

**Predict** what your scanner does with those two characters, then run it and
check.

**Answer:** why is `!` an error? Your specification is not broken — say what
an error actually means here, and name one rule you could add that would make
`!` stop being one.

#### ANSWER

```
I predict underscore becomes a ID token, and exclamation mark becomes a error since \+w doesn't select exclamation marks

My solution was to change the regex for ID to   !|\w+   which means either select words or select the exclamation mark, this makes exclamation mark it's own ID token
```

---

### Step 9 — Match the expected output

Your scanner should now reproduce `expected` exactly, error line included.

Rather than reading both files and comparing them yourself, save your
scanner's output to a file and let `diff` do it:

```bash
plcc-scan input > output      # writes the output into a file named output
diff output expected
```

**No output from `diff` means they matched**, and you are done.

If they do not match, `diff` prints the lines that differ. Lines marked `<`
come from the first file you named — your `output`. Lines marked `>` come from
the second — `expected`. So `<` is what you produced and `>` is what you
should have produced.

**Fix the first difference before looking at the rest.** One wrong rule
usually throws off several lines at once, and the later differences often
disappear when the first one is fixed.

One failure is not about your specification at all: if **every** line differs
and the only difference is the text before the first colon, you ran
`plcc-scan` with a different spelling of the filename. See the note in step 1,
and re-run it as `plcc-scan input` from inside `q3/`.

`output` and `trace.txt` are scratch files; delete them or leave them, it does
not matter. `spec.plcc` is the one that gets graded, so leave it in `q3/`.

**Report:** paste your finished `spec.plcc`.

#### ANSWER

```
#In order to get this to match expected I had to comment out my ! mark filter

skip COMMENT '#.*$'
skip WS '\s+'
token THIS 'this'
token THAT 'that'
token THE 'the'
token OTHER 'other'
token THING 'thing'
#token ID '!|\w+'
token ID '\w+'
```

---

### Step 10 — On your own

Everything up to here told you what to do. This step tells you what the result
has to be, and leaves the how to you.

Copy your working specification to a second file so that step 9 keeps passing:

```bash
cp spec.plcc extra.plcc
```

Add one rule to `extra.plcc` — and only to `extra.plcc` — that recognizes a
run of one or more digits as a token named `NUM`.

Test it against the two files provided for this step. The `-s` option points
`plcc-scan` at a specification other than the default `spec.plcc`:

```bash
plcc-scan -s extra.plcc input_extra > output_extra
diff output_extra expected_extra
```

Getting `NUM` to appear at all is only half of it. **Where you put the rule
matters**, and `input_extra` is built to catch the wrong choice.

**Answer both:**

**(a)** Where did you have to put the `NUM` rule for the diff to pass, and
what goes wrong if you put it in the other place? Name the rule it interacts
with and which of the two tie-breaking behaviors from step 7 is responsible.

**(b)** `input_extra` contains `12345xxx`, which begins with five digits, yet
`expected_extra` says it is an `ID`. Explain why — and say whether moving your
`NUM` rule would change that.

#### ANSWER

```
Replace this line with your answer.
```

`output_extra` is scratch, like `output`. Leave `extra.plcc` in `q3/`
alongside `spec.plcc` — both of those are graded.

---

## Before you zip and upload your work

- [ ] Every `ANSWER` block has an answer in it. An unanswered block reads as
      skipped work under **Completeness**.
- [ ] `q3/spec.plcc` — your finished specification from step 9.
- [ ] `q3/extra.plcc` — your step 10 specification, with the `NUM` rule.

`output`, `output_extra`, and `trace.txt` are scratch files. Leaving them in
place costs you nothing.
