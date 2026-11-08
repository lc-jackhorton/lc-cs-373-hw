# CS373 - Assignment a4

## Purpose

A3 ended with `V4`, where a binding names a value and nothing ever changes
one. This assignment covers the languages that come next. `V5` and `V6` change
*how* bindings get added: `V5`'s `letrec` lets a procedure find its own name,
and `V6`'s `define` adds to the top-level environment between programs. `SET`
and `REF` let a binding change: `SET` lets any program change a variable, and
`REF` changes what a procedure receives when you hand it a variable.

The skill is the same as in A3, which is tracing. What is new is that the
drawing now has to show *when* things happen. That means when a name is looked
up, when a binding is added, and which **ref** a `set` changes. When the answer
surprises you, point at the line of the interpreter responsible.

### Reading

From the [course textbook](https://ourplcc.github.io/course-materials-ng/dev/):
[V5](https://ourplcc.github.io/course-materials-ng/dev/12-v5/),
[V6](https://ourplcc.github.io/course-materials-ng/dev/13-v6/),
[SET](https://ourplcc.github.io/course-materials-ng/dev/14-set/), and
[REF](https://ourplcc.github.io/course-materials-ng/dev/15-ref/).

As in the previous assignment, questions here use languages in defined in the
language repository. You can clone this repository with the command:

```
git clone https://github.com/ourPLCC/languages-ng.git
```

### What you will be able to do

1. **Draw a recursive environment.** For `letrec` and `define`, draw the
   chain, including a `ProcVal` that saves the very node it is added to. Say
   why `let` cannot recurse, and point to the line that makes the difference.

2. **Draw refs and trace side effects.** Draw each binding as a name, a ref,
   and the value in the ref. Predict what a program prints when a `set`
   changes a ref that something else can also reach. Say which construct made
   each ref.

3. **Contrast call by value and call by reference.** Run one program in `SET`
   and in `REF`, predict both results, and explain the difference from the
   drawing. Point to the method `VarExp` overrides in `REF`, `evalRef`, and say
   why only a variable overrides it.

### The core concepts

These are what the Correctness criterion looks at. Details, such as how your
diagram is laid out, are worth a comment from me but cost you nothing. These
are what matter:

- **`letrec` evaluates its declarations in order, in the new node.** It makes
  the node empty, then evaluates each right-hand side *in that node* and adds
  its binding before going on to the next. A right-hand side can see the
  bindings before it, but not the ones after it. A `ProcVal` made there saves
  that node, so its body can find its own name. `let` evaluates every
  right-hand side in the *old* node, which is why it cannot recurse.

- **A `proc` delays its body.** Evaluating a `proc` makes a `ProcVal` and looks
  up nothing in its body. A name in the body is looked up when the procedure
  is **called**, in the environment as it is at that moment.

- **Together:** a `proc` in a `letrec` can name a variable bound by a *later*
  declaration, as long as nothing calls it before that binding is added.

- **`define` adds to `Program.env`, or replaces a binding already there.** A
  closure that saved `Program.env` sees a later `define`. A closure that saved
  some other node does not.

- **A binding holds a ref, and the ref holds the value.** Reading a variable
  looks up its ref and takes the value out of it.

- **`set` changes the value in an existing ref**, and returns the new value.
  It never makes a ref.

- **In `SET`, `let`, application, `letrec`, and `define` each make a new
  ref.** So `let y = x` copies `x`'s value into a new ref for `y`, and a later
  `set x` does not reach `y`. `REF` changes only application, as the last
  concept says.

- **A closure saves a node, not values.** It sees every later change to a ref
  on its chain. That is how a procedure can remember something from one call
  to the next.

- **Call by value** (`SET`): each formal gets a new ref holding a copy of the
  argument's value. **Call by reference** (`REF`): when an argument is a
  variable, the formal gets *that variable's* ref. Any other argument still
  gets a new ref, and `let` still makes new refs, even in `REF`.

### Where this leads

Every language from here on is a variation on one question: when a procedure
is called, what does its formal get bound to? `SET` and `REF` are the first two
answers. Later languages give others, and you will compare them the same way
you compare these two here: by drawing which ref each name ends up with.

On Exam 2, this material shows up as the same things you do here: draw the
environment with its refs, trace a program, say what prints and why.

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
the learning is; the run is only the check. A wrong prediction followed by an
honest correction is a complete answer.

To run a program in a language from the cloned language repository:

```bash
cd .../languages-ng/src/SET/python
echo 'let x = 42 in { set x = add1(x) ; x }' | plcc-rep
```

or run `plcc-rep` with no input and type or paste programs. Ctrl-D ends it.
Each question says which language to use. Running a program in the wrong one
is the most common way to get a surprising answer: `set` does not exist before
`SET`, and `SET` and `REF` disagree on purpose.

### Drawings

Questions 1, 2, and 3 ask you to **draw** environments, four in all. Draw
them by hand and hand them in as images, as in A3. **[How to Hand In a
Drawing](../../drawings.md)** says how to name the files and where to put
them.

From `SET` on, draw each binding the way we did in class:

- **name → ref → value.** The ref is a small square between the name and its
  value. A `ProcVal`'s arrow starts inside the ref.
- **`set` changes the value in the ref.** Cross out the old value and write
  the new one in the same square. Do not draw a new ref.
- **Two names sharing one ref** are two arrows into the same square.

For `V5`, draw bindings as in A3, with no refs.

Every drawing question asks for **the environment some expression is
evaluated in**. Draw that environment's whole chain. The empty node a program
starts in is optional.

How this is scored is the same as A1 to A3: [grading.md](../../grading.md),
three criteria, nine points. The **core concepts** listed above are what
Correctness looks at.

## QUESTION 1 — Recursion

**(a)** Use `V5` (`.../languages-ng/src/V5/python`). This is A3 Question 4(d)'s
`sumto`, with `let` changed to `letrec` and no passing the procedure to
itself:

```
letrec
  sumto = proc(n) if zero?(n) then 0 else +(n, .sumto(sub1(n)))
in
  .sumto(4)
```

Predict, then run. Draw the environment the body of `.sumto(4)` is evaluated
in, as `q1a`, and write the file name in the answer block.

Then compare `LetDecls.addLetrecBindings` with `LetDecls.addBindings` in
`.../languages-ng/src/V5/python/spec.plcc`. Both evaluate each right-hand side with
`e.eval(env)`. In which node is that done in each method? Quote the line in
`addLetrecBindings` that decides which node `env` is when `e.eval(env)` runs,
and say why that lets `sumto`'s body find `sumto`.

### ANSWER — (a)

````
```
Run using V5

q1a.jpg

Prediction
10

Result
10

LetrecExp is the node which calls addLetrecBindings
LetExp is the node which calls addBindings

Line which determines which environment letrec bindings are put in "    env = env.extendEnv(Bindings())"
env = env.extendEnv means that inside a new environment is the previous environment and its bindings
Letrec creates environment then adds bindings to that environment
Let prepares the bindings then places those bindings in a created environment
```
````


**(b)** Use `V5`. Predict each, then run each:

```
(1)  letrec x = 3  y = x  in y
(2)  letrec y = x  x = 3  in y
(3)  letrec a = proc() b  b = 7  in .a()
(4)  letrec a = proc() b  c = .a()  b = 7  in c
```

For each one, say which core concept explains the output: that `letrec`
works in order, that a `proc` delays its body, or both together. Be specific
about **when** each name is looked up, and whether its binding has been added
by then.

### ANSWER — (b)

````
```
Run in V5

(1)  letrec x = 3  y = x  in y

Prediction : 3
Result : 3
letrec reads left to right. letrec creates an environment and sets x within the environment to be a reference leading to 3, x binding is added to environment, then it sets the y in that environment to lead to the x reference which leads to 3, y now has a binding in the enviroment, then it evaluates y which calls the x reference thus returning 3 as the value.

(2)  letrec y = x  x = 3  in y

Prediction : No reference for x
Result : No binding for x
letrec reads left to right so it initializes an environment and tries to set y to lead to the x reference however, x has no binding reference yet.

(3)  letrec a = proc() b  b = 7  in .a()

Prediction : 7
Result : 7
letrec reads left to right. First it initializes an environment, then it sets a to equal a procedural expression that takes no input and returns b as an output. a now has a binding in the enviroment to the procedural expression. This is okay as b doesn't need to be defined until the function is evaluated. b reference is set to lead to 7 so b now has a binding in the environment. Once .a() is evaluated it returns b thus resulting in 7.


(4)  letrec a = proc() b  c = .a()  b = 7  in c


Prediction : No binding for b
Result : No binding for b
letrec reads left to right. First it initializes an environment, then it sets a to equal a procedural expression that takes no input and returns b as an output. a now has a binding in the environment to b. c reference is set to the function, thus forcing the function to be evaluated before b reference has been defined. Since the function is supposed to return b, it can't return anything so this will result in an error.
```
````

**(c)** Use `V6` (`.../languages-ng/src/V6/python`). Enter these in **one**
`plcc-rep`, in this order:

```
define n = 1
define f = proc() n
define g = let n = n in proc() n
define n = 2
.f()
.g()
```

Predict what the last two print, then run. Explain both from **which node
each `ProcVal` saved**. No drawing is required.

### ANSWER — (c)

````
```
Run in V6

Prediction
.f() prints 2
.g() prints 1

Result
n
f
g
n
2
1

Reasoning
define n = 1
define f = proc() n
define g = let n = n in proc() n
define n = 2
.f()
.g()

f is defined as n, this relies on the global definition of n. When .f() is called, this global definition is 2.
This is defined as a node which is type ProcExp

ProcExp
def eval(self, env):
    return self.proc.makeClosure(env)
Where the procedural is enclosed within the environment (in this case the global environment) 


When g is defined, the let expression creates an environment, inside that environment a local n is created using the global n which is currently defined as n = 1. When g is called it will rely on local n and evaluate as 1.
This is evaluated with
def eval(self, env):
    nenv = self.letDecls.addBindings(env)
    return self.exp.eval(nenv)
Where the self.exp is evaluated using the new environment, the self.exp node is a proc expression node that relies on the nenv
```
````


## QUESTION 2 — Refs and side effects

Use `SET` (`.../languages-ng/src/SET/python`) for this whole question.

**(a)**

```
let
  x = 1
in
  let
    y = x
    f = proc() x
  in
    { set x = 10 ; +(y, .f()) }
```

Predict, then run. Draw the environment `+(y, .f())` is evaluated in, as
`q2a`, with every ref, and with `set`'s change crossed out and rewritten.
Label each ref with the construct that made it. Then explain the output: why
does `y` not see the `set`, when `.f()` does?

### ANSWER — (a)

````
```
Run in SET
q2a.jpg

Predicted result : 11
Actual Result : 11

x is assigned reference 1   in an environment
y is assigned reference x in the environment thus y = 1
f is a procedural which outputs nenv x
nenv x is mutated by set locally to 10
+(y, .f()) evaluates .f() to produce local x of 10 and add that to y which is 1
10 + 1 = 11
```
````

**(b)**

```
let
  count = 0
in
  let
    inc = proc() set count = add1(count)
  in
    { .inc() ; .inc() ; count }
```

Predict, then run. Draw the environment the body of the **second** `.inc()`
is evaluated in, at the moment that body starts, as `q2b`. `inc` has no
formals, so the node the call makes has no bindings. Draw it anyway, with an
empty table, and label it `.inc()`.

Each call makes a **new** node. So why does the second call see the first
call's change? Answer from your drawing.

### ANSWER — (b)

````
```
Run in SET
q2b.jpg

let
  count = 0
in
  let
    inc = proc() set count = add1(count)
  in
    { .inc() ; .inc() ; count }


Creates an environment where count is 0
A nenv is created captured by the existing enviroment where inc is a procedural that when evaluated takes count from the environment, adds 1 to count thus mutating count from the environment

In the sequence
When .inc is evaluated it mutates count to 1
When .inc is evaluated against it mutates the count to 2
The count is the last thing listed in the sequence so the count is outputted as 2
```
````

**(c)** Run `set z = 1` on its own. Read `SetExp.eval` in
`.../languages-ng/src/SET/python/spec.plcc`. Quote the line of `SetExp.eval` whose
call fails, and say why `set` can never make a new variable.

### ANSWER — (c)

````
```
Run in SET

   def eval(self, env):
        v = self.exp.eval(env)
        ref = env.applyEnvRef(self.symbol.lexeme)
        return ref.setRef(v)


set z = 1   is an expression that can be evaluated in global environment so "v = self.exp.eval(env)" is fine
The line that fails is    "ref = env.applyEnvRef(self.symbol.lexeme)" since there's no reference for z
set can't make a new variable because set can only apply references, it cannot create new references
```
````


## QUESTION 3 — Call by value, call by reference

**(a)** Run this in **both** `SET` and `REF` (`.../languages-ng/src/REF/python`):

```
let
  x = 3
  y = 5
  swap = proc(a, b) let t = a in { set a = b ; set b = t }
in
  { .swap(x, y) ; -(x, y) }
```

Predict both, then run both. For `REF`, draw the environment the body of
`swap`'s `let` is evaluated in, at the moment it starts, as `q3a`. That is
before either `set` runs, so nothing is crossed out yet. Also draw the node
that holds `x` and `y`, even though it is not on that chain, so your drawing
shows where `a`'s and `b`'s arrows go. Label each ref with the construct that
made it. Then explain the two outputs: what is different about the refs `a`
and `b` get in each language?

### ANSWER — (a)

````
```
SET & REF
q3a.jpg

let
  x = 3
  y = 5
  swap = proc(a, b) let t = a in { set a = b ; set b = t }
in
  { .swap(x, y) ; -(x, y) }


For SET it's pass by value
x = 3
y = 5

When swap is evaluated it takes x = 3 and y = 5 then does a = 3, b = 5 inside the procedural. It creates an environment, in that environment 3 is stored in t, then 5 is stored in a, then 3 is stored in b. The result is a = 5 b = 3. After swap, the modified x and y are used in -(x,y) resulting in 2.

For REF it's pass by reference
x = reference to 3
y = reference to 5

When swap is evaluated it takes the x and y then does a = x reference, b = y reference inside the procedural. It creates an environment, in that environment t is set to the reference of a. Then a is set to the reference of b (which is y), then b is set to the reference of t (which is ref a which is x).  After the swap, the modified x and y are used in -(x,y) resulting in -2.

The reason this swapping doesn't work in REF is because REF isn't changing what x and y fundamentally are referencing, just the things that reference to x and y.
```
````

**(b)** Change the call to `.swap(add1(x), y)` and change nothing else.
Predict and run in both languages. Explain the `REF` output: what did `a` and
`b` each get bound to, and which of `x` and `y` changed?

### ANSWER — (b)

````
```
SET & REF

SET results in -2
REF results in -1

SET takes a = add1(x) and evaluates that as 4. Then takes t = 4. Then takes a = b = 5. Then takes b = t = 4. So b = 4 and a = 5. Then because the x and y weren't changed we take x-y=-2 since 3-5=-2.

REF takes a = add1(x), add1(x) is assigned to t, b is assigned to a so a is now 5. t is assigned to b so b is now add1(x). Since a = 5 that means global x is now 5, since b = global y then global y is now add1(x) which is 4. Then -(x,y) takes 4-5=-1  
```
````

**(c)** In A3 you rewrote a `let` as an applied `proc`. Run both of these in
**both** `SET` and `REF`:

```
let x = 3 in let y = x in { set y = add1(y) ; x }
let x = 3 in .proc(y) { set y = add1(y) ; x } (x)
```

In one of the two languages they disagree. Explain why. Then, in
`.../languages-ng/src/REF/python/spec.plcc`, find the two `evalRef` methods: the
default one in `Exp`, and the one `VarExp` overrides it with. Quote both
bodies, and say why only a variable gets its own ref passed while every other
expression gets a new one.

### ANSWER — (c)

````
```
SET & REF

SET causes both of these to yield 3
let x = 3 in let y = x in { set y = add1(y) ; x }
let x = 3 in .proc(y) { set y = add1(y) ; x } (x)

REF causes first one to yield 3 and second one to yield 4.
The reason ref reads the second language differently is because ; x in the sequence doesn't evaluate x instead it assigns x reference which is then put into add1(x) thus becoming 4.

Exp
%%%
def evalRef(self, env):
    return ValRef(self.eval(env))
%%%

VarExp
%%%
def eval(self, env):
    return env.applyEnv(self.symbol.lexeme)

def evalRef(self, env):
    return env.applyEnvRef(self.symbol.lexeme)

def __str__(self):
    return self.symbol.lexeme
%%%

General expressions are by default evaluated and assigned to a value reference. Variables are evaluated using a environments reference of its own lexeme which will be the same for all variables using that lexeme
```
````

## Before you zip and upload your work

- [X] Every `ANSWER` block has an answer in it. An unanswered block reads as
      skipped work under **Completeness**.
- [X] Each answer says which language you ran it in, wherever the question
      used more than one.
- [X] Your drawings, `q1a`, `q2a`, `q2b`, and `q3a`, are in this directory,
      and each answer block names its file.

`plcc-ng/` directories are build caches. Leaving them in place costs you
nothing.
