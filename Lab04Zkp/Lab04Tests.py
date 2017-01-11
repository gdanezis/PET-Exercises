#####################################################
# GA17 Privacy Enhancing Technologies -- Lab 04
#
# Zero Knowledge Proofs
#
# Run the tests through:
# $ py.test -v test_file_name.py

import pytest
from pytest import raises

try:
    from Lab04Solution import *
except:
    from Lab04Code import *

#####################################################
# TASK 1 -- Prove knowledge of a DH public key's 
#           secret.

@pytest.mark.task1
def test_provekey_correct():
    params = setup()

    ## Correct proof
    priv, pub = keyGen(params)
    proof = proveKey(params, priv, pub)
    assert verifyKey(params, pub, proof)


@pytest.mark.task1
def test_provekey_incorrect():
    params = setup()

    priv, pub = keyGen(params)
    proof = proveKey(params, priv, pub)

    # Incorrect proof
    priv2, pub2 = keyGen(params)
    proof2 = proveKey(params, priv2, pub2)
    assert not verifyKey(params, pub, proof2)

#####################################################
# TASK 2 -- Prove knowledge of a Discrete Log 
#           representation.

@pytest.mark.task2
def test_proveCommit_correct():
    params = setup()

    ## Correct proof
    secrets = [10, 20, 30, 40]
    C, r = commit(params, secrets)
    proof = proveCommitment(params, C, r, secrets)
    assert verifyCommitments(params, C, proof)

@pytest.mark.task2
def test_proveCommit_incorrect():
    params = setup()

    ## Correct proof
    secrets = [10, 20, 30, 40]
    C, r = commit(params, secrets)
    proof = proveCommitment(params, C, r, secrets)

    ## Incorrect proof
    secrets2 = [1, 20, 30, 40]
    C2, r2 = commit(params, secrets2)
    proof2 = proveCommitment(params, C2, r2, secrets2)
    assert not verifyCommitments(params, C, proof2)
    assert not verifyCommitments(params, C2, proof)

#####################################################
# TASK 3 -- Prove Equality of discrete logarithms.
#

@pytest.mark.task3
def test_proveEquality_correct():
    params = setup()

    x, K, L = gen2Keys(params)
    proof = proveDLEquality(params, x, K, L)

    assert verifyDLEquality(params, K, L, proof)

@pytest.mark.task3
def test_proveEquality_incorrect():
    params = setup()

    x, K, L = gen2Keys(params)
    _, _, L2 = gen2Keys(params)

    proof = proveDLEquality(params, x, K, L)

    assert not verifyDLEquality(params, K, L2, proof)

#####################################################
# TASK 4 -- Prove correct encryption and knowledge of 
#           a plaintext.

@pytest.mark.task4
def test_proveEnc_correct():
    params = setup()

    priv, pub = keyGen(params)

    k, ciphertext = encrypt(params, pub, 10)
    proof = proveEnc(params, pub, ciphertext, k, 10)
    assert verifyEnc(params, pub, ciphertext, proof)


@pytest.mark.task4
def test_proveEnc_incorrect():
    params = setup()

    priv, pub = keyGen(params)

    k, ciphertext = encrypt(params, pub, 10)
    _, ciphertext2 = encrypt(params, pub, 20)

    proof = proveEnc(params, pub, ciphertext, k, 10)
    assert not verifyEnc(params, pub, ciphertext2, proof)

#####################################################
# TASK 5 -- Prove a linear relation
#

@pytest.mark.task5
def test_proveRel_correct():
    params = setup()
    C, x0, x1, r = relation(params, 20)
    proof = prove_x0eq10x1plus20(params, C, x0, x1, r)
    assert verify_x0eq10x1plus20(params, C, proof)


@pytest.mark.task5
def test_proveRel_incorrect():
    params = setup()
    C, x0, x1, r = relation(params, 20)
    proof = prove_x0eq10x1plus20(params, C, x1, x0, r)
    assert not verify_x0eq10x1plus20(params, C, proof)
