# CS737 - Assignment a5

## Purpose

A4 ended with two answers to one question: when a procedure is called, what does
its formal get bound to? `SET` gives every formal a new ref holding a copy.
`REF` gives a variable argument's formal that variable's own ref. This
assignment adds three more answers. `NAME` and `NEED` delay an argument: the
formal gets the expression itself, evaluated later, when the body reads it. The
third, **copy-in, copy-out** (`CICO`), is not in the textbook or the
`language-ng` repository. You build it yourself, starting from `REF`, following
the steps in Question 2.

The main skill is still tracing. One skill is new: changing an interpreter so
that it has a semantics you can state in one sentence. When a run surprises you,
point to the line of the interpreter that caused it. In `CICO`, you wrote that
line.

### Reading

From the [course textbook](https://ourplcc.github.io/course-materials-ng/dev/):
[NAME](https://ourplcc.github.io/course-materials-ng/dev/16-name/) and
[NEED](https://ourplcc.github.io/course-materials-ng/dev/17-need/).
Copy-in, copy-out is not in the textbook. Question 2 teaches it.

To answer questions related to Languages `SET`, `REF`, `NAME`, and `NEED` you
will need to clone the languages repository with the command:

```
git clone https://github.com/ourPLCC/languages-ng.git
```

This assignment also comes with a copy of Language `REF` with the name `CICO`.
You will build `CICO` with *that* copy (i.e., don't modify `REF` in your clone
of the languages repository).

### What you will be able to do

1. **Trace a delayed argument.** Predict what a program prints in `NAME` and in
   `NEED`, and say when, and how often, each thunk is evaluated. Draw a thunk
   with the environment it keeps.

2. **Build a parameter-passing semantics.** Change `REF` into `CICO` and test it
   against programs whose output you predicted first.

3. **Compare five semantics.** For one program, classify each argument, predict
   the result in `SET`, `REF`, `NAME`, `NEED`, and `CICO`, and explain every
   difference.

### The core concepts

The Correctness criterion looks at these concepts. Details, such as the layout
of your diagram, may get a comment from me but cost you no points.

- **In `NAME`, an argument that is not a variable, a literal, or a `proc`
  becomes a thunk.** A thunk holds the unevaluated expression and the
  **caller's** environment. It is not text pasted into the body: a name in it is
  looked up where the call was made.

- **A thunk is evaluated every time its formal is read**, and never if the
  formal is never read.

- **In `NEED`, a thunk is evaluated at most once.** The first read evaluates it
  and saves the value. Every later read returns the saved value. So the value is
  fixed at the first read, not at the call.

- **In `NEED`, a formal bound to a literal or a `proc` is read-only too.** A
  formal can be `set` only if the caller passed a variable.

- **In `CICO`, a variable argument is copied in at the call and copied out at
  the return.** The formal gets a new ref holding a copy of the variable's
  value, taken when that argument is evaluated. Arguments are evaluated left to
  right, so a later argument that changes the variable does not change the copy.
  When the body finishes, the formal's final value is copied back into the
  variable's ref, one argument at a time, left to right. Any other argument is
  passed by value, and nothing is copied back.

- **During a `CICO` call, the variable and the formal are separate refs.** A
  change through one is not seen through the other until the return, and the
  copy-out then overwrites whatever the variable holds.

- **Aliasing is one ref reachable by two names.** For example, `.p(x, x)`, or a
  body that changes `x` directly while `x` is also an argument. In `REF` the two
  names share one ref, so each sees the other's changes at once. In `CICO` each
  name has its own copy, and the last copy-out wins.

- **Each semantics is a row of one table.** The columns are the kinds of
  argument: a variable, a literal, a `proc`, and anything else. In `REF`,
  `NAME`, and `NEED`, a variable is passed by reference and a literal or `proc`
  by value. `NAME` and `NEED` make anything else a thunk, which cannot be `set`.
  `CICO` is a fifth row. To predict a program, put each argument in its column
  and read the cell. In all five, `let` still makes a new ref holding a copy,
  and the arguments of a primitive like `+` are only read.

### Where this leads

Exam 2 asks you to do the same things you do here: classify each argument,
trace the program in more than one language, and say what prints and why.

## How to do this assignment

**Your answers go in this file.** Every question has one or more `ANSWER`
blocks that look like this:

````
```
Replace this line with your answer.
```
````

Replace that line with your answer and leave the fences around it alone.

**Predict first, then run.** Write the prediction down before you run
anything. Then run it and say whether you were right. The prediction is where
the learning is. The run is only the check. A wrong prediction followed by an
honest correction is a complete answer.

**Paths in this handout are either relative to your cloned languages repository
`.../languages-ng/src/...` or relative to the directory in which this
`README.md` is located.** To run a program with the former:

```bash
cd .../languages-ng/src/NAME/python
echo 'let x = 3 f = proc(t) { t ; t ; t } in .f(set x = add1(x))' | plcc-rep
```

To run a program with the latter:

```bash
cd CICO/python
echo 'let x = 3 f = proc(t) { t ; t ; t } in .f(set x = add1(x))' | plcc-rep
```

In both cases, you can also run `plcc-rep` with no input and type or paste
programs. Ctrl-D ends it. Each question says which language to use. Running a
program in the wrong one is the most common way to get a surprising answer.

### Drawings

Question 1 asks for **one** drawing. Draw it by hand and submit it as an
image, as in A3 and A4. **[How to Hand In a Drawing](../../drawings.md)** says
how to name the file and where to put it.

Draw bindings as in A4: **name → ref → value**. Draw a **thunk** as we did
in class: a ref box holding the unevaluated expression, with an arrow from the
box to the node where the call was made.

Scoring is the same as in A1 to A4: [grading.md](../../grading.md), three
criteria, nine points. Correctness looks at the **core concepts** listed
above.

## QUESTION 1 — Call by name, call by need

**(a)** Run this in `SET`, `NAME`, and `NEED` (`.../languages-ng/src/SET/python`,
`.../languages-ng/src/NAME/python`, `.../languages-ng/src/NEED/python`):

```
let
  x = 0
in
  let
    f = proc(a, b) { a ; a ; +(a, x) }
  in
    .f(set x = add1(x), set x = 100)
```

Predict all three, then run all three. For `NAME` and `NEED`, say how many
times each argument's expression is evaluated, and what `x` holds just after
each read of `a`. For `SET`, say when the two `set`s run.

### ANSWER — (a)

```
Run with SET, NAME, NEED
let x = 0 in let f = proc(a, b) { a ; a ; +(a, x) } in .f(set x = add1(x), set x = 100)


SET result
101

SET does call by value
x = 0 then .f is called which takes 
set x = add1(x) so x becomes 1 then feeds that into the value of a so a=1,
Then does set x = 100 and puts that into b = 100, x is now 100
Then evaluates each item in the sequence { a ; a ; +(a,x) } with the last sequence term being what’s returned that being +(a,x) so 1+100 = 101


NAME result
6

NAME does call by name
x = 0
.f is run so when a is called it will run  x is set to add1(x), then that’s set to a.  a = set x = add1(x)
When b is called it will run  x is set to 100, then that’s set to b.  b = set x = 100

Then for the sequence { a ; a ; +(a, x) }, each time a is called it does add1 to x which connects to a. This results in a = x = 3 by the time when +(a,x) is going to be run, so 3 + 3 = 6.

NEED result
2

NAME does call by need
x = 0
.f is run so when a is called it will run  x is set to add1(x), then that’s set to a.  a = set x = add1(x)
When b is called it will run  x is set to 100, then that’s set to b.  b = set x = 100

Then for the sequence { a ; a ; +(a, x) }, a is only called once and stored. This results in a = x = 1 by the time when +(a,x) is going to be run, so 1 + 1 = 2.
```

**(b)** Use `NAME`:

```
let
  y = 2
in
  let
    g = proc(t) let y = 100 in +(t, y)
  in
    let
      y = 5
    in
      .g(*(y, 3))
```

There are three `y`s. Predict, then run. Draw the environment `+(t, y)` is
evaluated in, as `q1b`, and write the file name in the answer block. Also draw
the node that holds `y = 5` and the nodes it links to, even though they are
not on that chain, so your thunk's arrow has somewhere to go.

Then explain the output: when `t` is read, which `y` does `*(y, 3)` use, and
why not either of the other two?

### ANSWER — (b)

```
q1b.png

Run with NAME


let y = 2 in let g = proc(t) let y = 100 in +(t, y) in let y = 5 in .g(*(y, 3))
Predicted 115

This does global y = 2
Then sub global y = 5
.g is run
Then t = *(sub global y, 3)
Then sub sub global y = 100
So when +(t,sub global y sub sub global y) is run that evaluates t so then 5*3=15 so t = 15, that means 15 + 100 is evaluated as 115.

The reason *(y, 3) is sub global y is because *(y,3) unlike Int, Proc, Var returns a thunk and that thunk is evaluated in the sub global y ‘s environment. 
```

**(c)** Run both of these in `NAME` and in `NEED`:

```
let p = proc(n) { set n = *(n, 2) ; n } in .p(21)
let x = 21 p = proc(n) { set n = *(n, 2) ; n } in { .p(x) ; x }
```

Predict all four, then run all four. One of the four runs is an error. In
`.../languages-ng/src/NEED/python/spec.plcc`, find the class whose `setRef` raises
it, and quote that method. Then explain why the other program, which also
runs `set n`, works in `NEED`.

### ANSWER — (c)

```
Run with NEED and NAME 

let p = proc(n) { set n = *(n, 2) ; n } in .p(21)
Predicted result for NAME, 42, NEED fails
NEED cannot modify read only reference
NAME results in 42

So NAME will set n = 21 then evaluates the first term in the sequence so set n = *(n,2) so that 21*2=42 now n = 42, then the sequence will output the last term n so 42 is outputted.
NEED set n = 21, then because n is already set it cannot be modified.


let x = 21 p = proc(n) { set n = *(n, 2) ; n } in { .p(x) ; x }
Predicted result for NAME, 42, NEED fails
NEED results in 42
NAME results in 42

So NAME and NEED will do x = 21 then runs .p(x) with x so then n = x is used. 
Each term in sequence is evaluated so n is set to *(x, 2) and then n is returned since the last term of the sequence is returned so x * 2 is 42.
```


## QUESTION 2 — Build copy-in, copy-out

**Copy-in, copy-out** (`CICO`; also called *call by value-result*) works like
this. When an argument is a variable, the formal gets a **new** ref holding a
copy of the variable's value. That is the copy in, and it is the same as call
by value. The body then runs, and any `set` on the formal changes only that
copy. When the body finishes, the formal's final value is **copied back** into
the variable's ref. That is the copy out. When there is more than one
argument, the copies go back one at a time, left to right. An argument that is
not a variable is passed by value, and nothing is copied back for it.

The copy is taken when that argument is evaluated. Arguments are evaluated
left to right, so a later argument that changes the variable does not change
the copy.

Your starting point is `CICO/`, in this directory. It is a copy of `REF`, and
it runs as `REF` until you change it. **All your changes go in
`CICO/python/spec.plcc`.** Do not change `CICO/grammar.plcc` or `Env/`.
`CICO` uses `REF`'s grammar: the syntax is the same, only the behavior is
new.

To run it:

```bash
cd CICO/python
echo 'let x = 42 in { set x = add1(x) ; x }' | plcc-rep
```

The program used in (a) to (c) is:

```
let
  x = 5
in
  let
    p = proc(t) { set x = add1(x) ; set t = +(t, t) }
  in
    { .p(x) ; x }
```

**(a)** Before you change anything, predict what this program prints in `SET`
and in `REF`, then run both. Then, from the description above, predict what it
will print in `CICO`. Trace `x` and `t` through the call and the copy out.

### ANSWER — (a)

```
Run with CICO, SET, REF

let x = 5 in let p = proc(t) { set x = add1(x) ; set t = +(t, t) } in { .p(x) ; x }

Prediction for REF, 12
Prediction for SET, 6
12 in REF
6 in SET

In SET x is set to 5 then .p is run, t is assigned the value of x so t = 5,  1 is added to x so x = 6, then operation t = +(t,t) is performed on t which was assigned the value of x, so t = 12 and the x returned is 6 since x is last entry in the sequence.

In REF x is set to 5 then .p is run, t is assigned the reference of x, and 1 is added to x, then operations are performed on t which has been assigned the reference of x, so modifying t modifies x, thus t = 6, thus we get 12 because t = +(t,t) so x = 12 and x is the last entry in the sequence.

CICO is a copy of REF
Prediction for CICO, 12
Mine for some reason returned 6, is there a typo in the question, was CICO a copy of SET?
```

Now build it, in four steps. Run the Question 2 program after every step.

**Step 1. Every ref can be copied out.** In the `Ref` section, add this
method to class `Ref`, after `setRef`:

```python
    def copyOut(self):
        pass
```

By default, copying out does nothing. `ValRef` inherits this, so an argument
that gets a plain `ValRef` is never copied back. Nothing has changed yet:
the program still prints what `REF` printed.

**Step 2. A ref for a variable argument.** Paste this between `ValRef`'s
closing `%%%` and the `ProcVal` line, with `VarRef` and both `%%%` lines at
the left margin. Then fill in the body of `copyOut`: one line, under the
comment, indented to match it (8 spaces).

```python
VarRef
%%%
from ValRef import ValRef


class VarRef(ValRef):

    def __init__(self, ref):
        super().__init__(ref.deRef())   # copy in: a new ref holding a copy
        self.ref = ref                  # the variable's own ref, kept for later

    def copyOut(self):
        # Put this ref's value back into the variable's own ref.
%%%
```

A `VarRef` *is* a `ValRef`: `deRef` and `setRef` work on its own copy, so a
`set` in the body never touches the variable. It also remembers the
variable's ref, so that `copyOut` can write to it.

**Step 3. Variable arguments get a `VarRef`.** In the `VarExp` section,
change `evalRef` so that it returns a `VarRef` built from the variable's ref,
instead of the variable's ref itself:

```python
def evalRef(self, env):
    return VarRef(env.applyEnvRef(self.symbol.lexeme))
```

and add an import section for it, just before the `VarExp` section:

```
VarExp:import
%%%
from VarRef import VarRef
%%%
```

**(b)** Run the program. It should print what `SET` printed. Why? You have
done the copy in. What has not happened yet, and so what does the variable
never see?

### ANSWER — (b)

```
Run with CICO
x never sees that t has been changed

Returns 6
```

**Step 4. Copy out at the return.** In `ProcVal.apply`, the last line
returns the body's value immediately. Change it so that `apply` saves the
body's value, then calls `copyOut()` on every ref in `args`, in order, and
then returns the saved value.

**(c)** First check your build: `let x = 1 p = proc(t) set t = 7 in { .p(x) ; x }`
must print `7`. If it does not, compare your code with steps 1 to 4. Then run
the Question 2 program and compare its output with your prediction in (a).
Explain the output step by step: what `x` and `t` each hold after each `set`,
and what the copy out does to `x`.

### ANSWER — (c)

```
Run with CICO

let x = 1 p = proc(t) set t = 7 in { .p(x) ; x }
Returns 7

let x = 5 in let p = proc(t) { set x = add1(x) ; set t = +(t, t) } in { .p(x) ; x }
Prediction 10
Returns 10	

x is set to 5, .p is run, t is set to 5 which is copied from x, x is changed to 6 due to x = add1(x), t is changed to 10 due to +(t,t), t’s result is then copied back into x so x returns 10 due to being the last entry in the sequence.
```

**(d)** Change the call to `.p(+(x, 0))` and change nothing else. Predict,
then run in `CICO`. Explain the output: what kind of ref does `t` get, which
method made it, and what does its `copyOut` do?

### ANSWER — (d)

```
let x = 5 in let p = proc(t) { set x = add1(x) ; set t = +(t, t) } in { .p(+(x, 0)) ; x }

Prediction 6
Result 6

X is set to 5, then when .p is evaluated, since +(x,0) is an expression so copy out doesn’t apply, this just runs like set where t is assigned value +(5,0) and that just means t = 5, then x isn’t tied to t, so x gets 1 added, the result is x is returned at the end of the sequence as 6.
```


## QUESTION 3 — Five ways to pass an argument

Use your `CICO` and languages's `SET`, `REF`, `NAME`, and `NEED`.

**(a)** Here one variable is passed twice. Run both in `REF` and in `CICO`:

```
let x = 1 p = proc(a, b) { set a = 10 ; set b = 20 ; a } in .p(x, x)
let x = 1 p = proc(a, b) { set a = 10 ; set b = 20 ; a } in { .p(x, x) ; x }
```

Predict all four, then run all four. Explain each output from the refs: how
many refs do `a` and `b` have between them in each language? In `CICO`, what
does `x` hold after each copy out?

Then, without running anything: if `CICO` copied out right to left instead of
left to right, what would the second program print?

### ANSWER — (a)

```
Run in REF, CICO, SET, NAME


(a) Here one variable is passed twice. Run both in REF and in CICO:

let x = 1 p = proc(a, b) { set a = 10 ; set b = 20 ; a } in .p(x, x)

Predictions
REF : 20
SET : 10
NAME : 20
CICO : 10

Result
REF : 20
SET : 10
NAME : 20
CICO : 10

Explained
REF means that both a, b refer to x. That means set b = 20 modifies a thus modifying x. The result will be 20.

SET means that a is set to value 10 and then returned at end of sequence as the value that should be returned by .p

NAME makes it so a = x , b = x but doesn’t evaluate. Then a is changed to 10 which means a = x = 10. Then b is changed to 20 so b = x = 20, then a is returned and since x = 20 that means when a is evaluated a = 20.

CICO makes it so x is copied into a and b. So a = 1, b = 1. Then a is set to 10, b is set to 20. Then a is returned after sequence, then b is copied back into x. Then a is returned by proc.



let x = 1 p = proc(a, b) { set a = 10 ; set b = 20 ; a } in { .p(x, x) ; x }

Predictions
REF : 20
SET : 1
NAME : 20
CICO : 20

Result
REF : 20
SET : 1
NAME : 20
CICO : 20

Explained
REF means a and b both refer to x. set a = 10 makes x = 10 then set b = 20 makes x = 20. The result is x returns as 20 since x is the last term in the sequence.

SET means that let x = 1. Then a and b are set to 1 and have stuff done to them. Then since x is the last term in the sequence x is what gets returned not a or b.

NAME makes it so a = x , b = x but doesn’t evaluate. Then a is changed to 10 which means a = x = 10. Then b is changed to 20 so b = x = 20, since x = 20 that means x gets returned as 20 since it’s the last term in the sequence.

CICO makes it so x is copied into a and b. So a = 1, b = 1. Then a is set to 10, b is set to 20. Then a is returned after sequence and b is copied back into x. Then since x is the last term in the sequence x is what is returned. 
```

**(b)** In class we built a table: one row per language, one column per kind
of argument. Fill in the row for `CICO`. Where a word from the other rows
fits, use it. Where none fits, write the correct term.

|           | variable `x` | literal `5`      | `proc(y) y`      | anything else: `add1(x)` |
| ---       | ---          | ---              | ---              | --- |
| **SET**   | value        | value            | value            | value |
| **REF**   | reference    | value            | value            | value |
| **NAME**  | reference    | value            | value            | thunk (evaluated on every read) |
| **NEED**  | reference    | value, read-only | value, read-only | thunk, cached (evaluated on first read only) |

Then run this in all five languages:

```
let
  x = 0
in
  let
    f = proc(a, b) { b ; set a = +(a, 100) ; +(b, x) }
  in
    { .f(x, set x = add1(x)) }
```

Predict all five first. For each argument, say which column it is in, then
read your answer off that language's row. Then add `; x` after the call and
run it again in all five. Compare `CICO`'s call value and its final `x` with
`SET`'s and `REF`'s, and explain each difference from the refs.

### ANSWER — (b)

```
|           | variable `x` | literal `5`      | `proc(y) y`      | anything else: `add1(x)` |
| ---       | ---          | ---              | ---              | --- |
| **CICO**  | Copied in then out | rest of these are just copied in

let x = 0 in let f = proc(a, b) { b ; set a = +(a, 100) ; +(b, x) } in { .f(x, set x = add1(x)) }

Prediction
REF : 102
SET : 2
NAME : 102
CICO : 2

Result
REF : 102
SET : 2
NAME : 204
CICO : 2

Explained
REF means a refers to x, b does call by value since  set x = add1(x) is “anything else” thus b = 1. set x = add1(x) changes x to 1. So now a = 1. This means adding a to 100 and making that the new a makes it so a = 101. Which also means x = 101. So adding x to b makes it so the returned value is 102.

SET means that let x = 0. Then a is set to the value of x so a = 0. Then b is set to the value of set x = add1(x) so b = 1 and x = 1. Then the last term in the sequence returned is +(b,x) which means 1 + 1 = 2. 

NAME makes it so a refers to x but isn’t evaluated thus a = x. b refers to set x = add1(x) which is a thunk. This thunk is evaluated anytime b is called so at the start of .f   x = 1 and b = 1. b is called in sequence so x = 2 and b = 2. a is then set to a = a + 100 requires that a be evaluated so a = 101. Now since a = x this means x = 101. Thus b gets evaluated again, this time set x = add1(x) results in b = 102 and x = 102. That means when the end of the sequence adds b and x it returns 204.

CICO makes it so x is copied into a and b. So a = 0, b = 0. Then b is evaluated so set x = add1(x) makes x = 1 and b = 1 . Then set a = a + 100 makes a = 100. Then b + x returns as 2. a is copied out to x which doesn’t matter because this returns b + x due to that being last in the sequence.
```

## Before you zip and upload your work

- [X] Every `ANSWER` block has an answer in it. An unanswered block reads as
      skipped work under **Completeness**.
- [X] Each answer says which language you ran it in, wherever the question
      used more than one.
- [X] Your drawing, `q1b`, is in this directory, and its answer block names
      the file.
- [X] `CICO/python/spec.plcc` has all four steps, and the Question 2 program
      prints what you said it would.

`plcc-ng/` directories are build caches. Leaving them in place costs you
nothing.
