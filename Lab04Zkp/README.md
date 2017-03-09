# GA17 Privacy Enhancing Technologies -- Lab 04

## Reminder of basic repository operations and testing

To update your local version in the virtual machine, go to the directory called `PET-Exercises` and type:

    $ git pull

To update your version of `petlib` type:

	$ sudo pip install petlib --upgrade

### Structure of Labs
The structure of all the labs will be similar: two python files will be provided. 

- The first is named `Lab0XCode.py` and contains the structure of the code you need to complete. 
- The second is named `Lab0XTests.py` and contains unit tests (written for the pytest library) that you may execute to partially check your answers. 

Note that the tests passing is a necessary but not sufficient condition to fulfill each task. There are programs that would make the tests pass that would still be invalid (or blatantly insecure) implementations.

The only dependency your Python code should have, besides pytest and the standard library, is the petlib library, which we specifically developed for this course (and also for our own use!). 

The petlib documentation is [available on-line here](http://petlib.readthedocs.org/en/latest/index.html).


### Working with unit tests
Unit tests are run from the command line by executing the command:

```
$ py.test -v Lab04Tests.py
```

Note the `-v` flag toggles a more verbose output. If you wish to inspect the output of the full tests run you may pipe this command to the `less` utility (execute `$ man less` for a full manual of less):

```
$ py.test -v Lab04Tests.py | less
```

You can also run a selection of tests associated with each task, by executing the command. the argument to the `-m` flag may be a task (from task1 to task5 for Lab 1).

```
$ py.test -v Lab04Tests.py -m task1
```

You may also select tests to run based on their name using the `-k` flag. Have a look at the test file to find out the function names of each test. For example the following command executes the very first test of Lab 1, since it matches its name `test_petlib_present`:

```
$ py.test -v Lab04Tests.py -k provekey
```

The full documentation of pytest is [available here](http://pytest.org/latest/).

## Lab 04 -- Zero Knowledge Proofs.

## General Hints:

- The `setup` returns a set of parameters including the group `G`, its order `o` and a number of generators `g` and `hi`, shared by all functions in this exercise.

- The `to_challenge` function takes a number of group elements (EC points in this case), hashes them, and returns a Bn appropriate to be used as a challenge.

- As usual modify the code file in the specified location. (marked by `## YOUR CODE HERE:`)

- Study the unit tests `Lab04Tests.py` to understand how to pass them, as well as how the functions you complete are meant to be used.

## TASK 01 -- Prove knowledge of a DH public key's secret.

- You will need to implement the Schnorr protocol in its non-interactive form to prove knowledge of a private key of a particular public key. 

- The output of `provekey` is a pair `(c, r)`, a `Bn` challenge and a `Bn` response.

- Study the `verifyKey` function to ensure it may verify the proof you generate.

## TASK 02 -- Prove knowledge of a Discrete Log representation.

- You will have to use the extended Schnorr protocol to prove knowledge of all secrets and opening of a commitment. 

- Study the function `commit` to understand the structure of the commitment. Ensure you understand the role of the opening value `r`.

- Study the function `verifyCommitement` to ensure your proof can be verified correctly.

- The `proveCommitment` function is passed the commitment and the secrets (including the opening). It should returns a proof consisting of the challenge and responses (multiple ones). 

## TASK 03 -- Prove Equality of discrete logarithms.

- In this task you need to implement `verifyDLEquality` the verification algorithm of the proof of equality of discrete logarithms of K and L.

- Study carefully `proveDLEquality` to ensure your verification algorithm verifies only correct proofs.

## TASK 4 -- Prove correct encryption and knowledge of a plaintext.

- In this task you need to implement both the zero knowledge proof and verification of validity of a ciphertext under public key pub and knowledge of the encrypted message m.

- In this proof you will need to combine proof of equality (for `k`) as well as proofs of multiple elements (`a` and `b`).

## TASK 5 -- Prove a linear relation

- Study `relation` and understand how it returns a commitment to values `x0` and `x1` with a relation between them (x0 = 10 x1 + 20).

- You need to implement a function that proves knowledge of `x0`, `x1` and `r`, as well as prove that the linear relation between the secrets holds.

- You also need to implement the verification function for knowledge of the commitment's secrets and the linear relation.

## TASK 6 -- (OPTIONAL) Prove that a ciphertext is either 0 or 1

- You have to implement both proof and verification that an encrypted message under `pub` is 0 or 1 without revealing which.

## TASK Q1 and Q2 -- Answer the two questions

- In Q2 you are given a snippet of code, and a test for it. Do not forget to study both before answering the question.