# GA17 Privacy Enhancing Technologies -- Lab 03

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
$ py.test -v Lab01Tests.py
```

Note the `-v` flag toggles a more verbose output. If you wish to inspect the output of the full tests run you may pipe this command to the `less` utility (execute `$ man less` for a full manual of less):

```
$ py.test -v Lab01Tests.py | less
```

You can also run a selection of tests associated with each task, by executing the command. the argument to the `-m` flag may be a task (from task1 to task5 for Lab 1).

```
$ py.test -v Lab01Tests.py -m task1
```

You may also select tests to run based on their name using the `-k` flag. Have a look at the test file to find out the function names of each test. For example the following command executes the very first test of Lab 1, since it matches its name `test_petlib_present`:

```
$ py.test -v Lab01Tests.py -k petlib
```

The full documentation of pytest is [available here](http://pytest.org/latest/).

## Lab 03 -- Basics of Privacy Friendly Computations through Additive Homomorphic Encryption.

## TASK 1 -- Additively Homomorphic Encryption

> Implement the key generation, encryption and decryption procedures for an additively homomorphic encryption scheme.

## Hints:

- You can run the tests just for this task by executing:

	py.test -v Lab03Tests.py -m task1

- The encryption scheme is the one described in the lectures on private computations.

- Key generation selects a private key between 1 and the order of the group; the public keys is x * g, where is a generator.

- A ciphertext is composed of two elements: (k *g, k * pub + m * h), where k is a random number mod the order of the group.

- Do use the table based discrete logarithm function to help implement the decryption operation.

- The `isCiphertext` function should return True for valid ciphertexts.

## TASK 2 -- Define homomorphic operations on ciphertexts

> Implement addition and multiplication by a constant over encrypted data.

## Hints:

- You can run the tests just for this task by executing:

	py.test -v Lab03Tests.py -m task2

- The objective of this task is to perform operations on ciphertext(s) without the knowledge of the secret keys in order to generate new ciphertexts that are functions of the original ones.

- The `add` function takes two ciphertexts and should return a ciphertext of the sum of their plaintexts.

- The `mul` function takes a single ciphertext, and returns a fresh ciphertext encrypting a multiple of its plaintext by a constant `alpha`.

- Both operations return a ciphertext.

## TASK 3 -- Threshold decryption

> Define key derivation and partial decryption to facilitate threshold decryption.

## Hints:

- The `GroupKey` operation aggregates a list of public keys from a number of authorities, without using any private keys, to generate a group public key. Encryption under this group key requires all authorities to help with decryption.

- The `partialDecrypt` function takes a ciphertext encypted under a group public key, and returns a partially decrypted ciphertext. 

- The `final` flag signifies that an authority is the last in a decryption chain, and should return a plaintext rather than a partially decrypted ciphertext.

## TASK 4 -- Corrupt threshold decryption authority

> Simulate the operation of a corrupt decryption authority.

## Hints:

- The objective of the function `corruptPubKey` is to return a public key that, when combines with other authority keys provided, returns a group key that the corrupt authority can decrypt on its own.

- The private key that should decrypt the corrupted group key is provided as an input to the function.

- Have a look at the tests to see an example of the corrupt authority code in action!

## TASK 5 -- A simple polling example

> Implement operations to support a simple private poll.

## Hints:

- The `encode_vote` procedure takes a vote (0 or 1) and returns a pair of ciphertexts representing whether it is a vote for 0 and whether it is a vote for 1.

- The `process_votes` takes a number of individual pairs of votes and returns a pairs of ciphertexts encrypting the total number of votes to 0 and the total number of votes to 1.

- Look at the function `simulate_poll` as a full example of a simulated distributed private poll.

## TASK Qx -- Answer the questions on the basis of your code.

> Please include the answers in the comment section provided, and make sure you code file can run correctly.
