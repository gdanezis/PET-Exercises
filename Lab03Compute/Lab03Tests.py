#####################################################
# GA17 Privacy Enhancing Technologies -- Lab 03
#
# Basics of Privacy Friendly Computations through
#         Additive Homomorphic Encryption.
#
# Run the tests through:
# $ py.test -v test_file_name.py

#####################################################
# TASK 1 -- Setup, key derivation, log
#           Encryption and Decryption

import pytest
from pytest import raises

try:
    from Lab03Solution import *
except:
    from Lab03Code import *

@pytest.mark.task1
def test_encrypt():
    params = setup()
    priv, pub = keyGen(params)
    assert encrypt(params, pub, 0)
    assert encrypt(params, pub, 10)
    assert encrypt(params, pub, -10)
    with raises(Exception) as excinfo:
        encrypt(params, pub, -1000)
    with raises(Exception) as excinfo:
        encrypt(params, pub, 1000)

@pytest.mark.task1
def test_decrypt():
    params = setup()
    priv, pub = keyGen(params)
    assert decrypt(params, priv, encrypt(params, pub, 0)) == 0
    assert decrypt(params, priv, encrypt(params, pub, 2)) == 2
    assert decrypt(params, priv, encrypt(params, pub, -2)) == -2
    assert decrypt(params, priv, encrypt(params, pub, 99)) == 99

#####################################################
# TASK 2 -- Define homomorphic addition and
#           multiplication with a public value

@pytest.mark.task2
def test_add():
    params = setup()
    priv, pub = keyGen(params)
    one = encrypt(params, pub, 1)
    two = encrypt(params, pub, 2)
    three = add(params, pub, one, two)
    assert decrypt(params, priv, three) == 3

    # Try it for a range of numbers
    for x in range(-10, 10):
        Ex = encrypt(params, pub, x)
        E2x = add(params, pub, Ex, Ex)
        assert decrypt(params, priv, E2x) == 2*x

@pytest.mark.task2
def test_mul():
    params = setup()
    priv, pub = keyGen(params)
    two = encrypt(params, pub, 2)
    three = mul(params, pub, two, 2)
    assert decrypt(params, priv, three) == 4

    # Try it for a range of numbers
    for x in range(-10, 10):
        Ex = encrypt(params, pub, x)
        E2x = mul(params, pub, Ex, 20)
        assert decrypt(params, priv, E2x) == 20*x

#####################################################
# TASK 3 -- Define Group key derivation & Threshold
#           decryption.

@pytest.mark.task3
def test_groupKey():
    params = setup()
    (G, g, h, o) = params

    # Generate a group key
    priv1, pub1 = keyGen(params)
    priv2, pub2 = keyGen(params)
    pub = groupKey(params, [pub1, pub2])

    # Check it is valid
    priv = (priv1 + priv2) % o
    assert decrypt(params, priv, encrypt(params, pub, 0)) == 0

@pytest.mark.task3
def test_partial():
    params = setup()
    (G, g, h, o) = params

    # Generate a group key
    priv1, pub1 = keyGen(params)
    priv2, pub2 = keyGen(params)
    pub = groupKey(params, [pub1, pub2])

    # Each authority decrypts in turn
    c = encrypt(params, pub, 0)
    cprime = partialDecrypt(params, priv1, c)
    m = partialDecrypt(params, priv2, cprime, True)
    assert m == 0

#####################################################
# TASK 4 -- Actively corrupt final authority, derives
#           a public key with a known private key.
#

@pytest.mark.task4
def test_badpub():
    params = setup()
    (G, g, h, o) = params

    # Four authorities generate keys
    priv1, pub1 = keyGen(params)
    priv2, pub2 = keyGen(params)
    priv3, pub3 = keyGen(params)
    priv4, pub4 = keyGen(params)

    # Derive a bad key
    x = o.random()
    badpub = corruptPubKey(params, x, [pub1, pub2, pub3, pub4])

    # Derive the group key including the bad public key
    pub = groupKey(params, [pub1, pub2, pub3, pub4, badpub])

    # Check that the corrupt authority can decrypt a message
    # encrypted under the group key with its secret only.
    assert decrypt(params, x, encrypt(params, pub, 0)) == 0

#####################################################
# TASK 5 -- Implement operations to support a simple
#           private poll.
#

@pytest.mark.task5
def test_poll():
    votes = [1, 0, 1, 0, 1, 1, 0, 1, 1, 1]
    v0, v1 = simulate_poll(votes)
    assert v0 == 3
    assert v1 == 7