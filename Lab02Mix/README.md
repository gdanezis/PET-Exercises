# GA17 Privacy Enhancing Technologies -- Lab 02

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

## Lab 02 -- Basics of Engineering Mix Systems and Traffic Analysis



