#####################################################
# GA17 Privacy Enhancing Technologies -- Lab 01
#
# Basics of Petlib, encryption, signatures and
# an end-to-end encryption system.
#
# Run the tests through:
# $ py.test test_file_name.py

###########################
# Group Members: TODO
###########################


#####################################################
# TASK 1 -- Ensure petlib is installed on the System
#           and also pytest. Ensure the Lab Code can 
#           be imported.

import pytest

try:
    from Lab01Solutions import *
except:
    from Lab01Code import *

@pytest.mark.task1
def test_petlib_present():
    """
    Try to import Petlib and pytest to ensure they are 
    present on the system, and accessible to the python 
    environment
    """
    import petlib 
    import pytest
    assert True

@pytest.mark.task1
def test_code_present():
    """
    Try to import the code file. 
    This is where the lab answers will be.
    """
    assert True


#####################################################
# TASK 2 -- Symmetric encryption using AES-GCM 
#           (Galois Counter Mode)

@pytest.mark.task2
def test_gcm_encrypt():
    """ Tests encryption with AES-GCM """
    from os import urandom
    K = urandom(16)
    message = u"Hello World!"
    iv, ciphertext, tag = encrypt_message(K, message)

    assert len(iv) == 16
    assert len(ciphertext) == len(message)
    assert len(tag) == 16

@pytest.mark.task2
def test_gcm_decrypt():
    """ Tests decryption with AES-GCM """
    from os import urandom
    K = urandom(16)
    message = u"Hello World!"
    iv, ciphertext, tag = encrypt_message(K, message)

    assert len(iv) == 16
    assert len(ciphertext) == len(message)
    assert len(tag) == 16

    m = decrypt_message(K, iv, ciphertext, tag)
    assert m == message

@pytest.mark.task2
def test_gcm_fails():
    from pytest import raises

    from os import urandom
    K = urandom(16)
    message = u"Hello World!"
    iv, ciphertext, tag = encrypt_message(K, message)

    with raises(Exception) as excinfo:
        decrypt_message(K, iv, urandom(len(ciphertext)), tag)
    assert 'decryption failed' in str(excinfo.value)

    with raises(Exception) as excinfo:
        decrypt_message(K, iv, ciphertext, urandom(len(tag)))
    assert 'decryption failed' in str(excinfo.value)

    with raises(Exception) as excinfo:
        decrypt_message(K, urandom(len(iv)), ciphertext, tag)
    assert 'decryption failed' in str(excinfo.value)

    with raises(Exception) as excinfo:
        decrypt_message(urandom(len(K)), iv, ciphertext, tag)
    assert 'decryption failed' in str(excinfo.value)


#####################################################
# TASK 3 -- Understand Elliptic Curve Arithmetic
#           - Test if a point is on a curve.
#           - Implement Point addition.
#           - Implement Point doubling.
#           - Implement Scalar multiplication (double & add).
#           - Implement Scalar multiplication (Montgomery ladder).

@pytest.mark.task3
def test_on_curve():
    """
    Test the procedues that tests whether a point is on a curve.

    """

    ## Example on how to define a curve
    from petlib.ec import EcGroup, EcPt
    G = EcGroup(713) # NIST curve
    d = G.parameters()
    a, b, p = d["a"], d["b"], d["p"]
    g = G.generator()
    gx, gy = g.get_affine()

    from Lab01Code import is_point_on_curve
    assert is_point_on_curve(a, b, p, gx, gy)

    assert is_point_on_curve(a, b, p, None, None)

@pytest.mark.task3
def test_Point_addition():
    """
    Test whether the EC point addition is correct.
    """
    from pytest import raises
    from petlib.ec import EcGroup, EcPt
    G = EcGroup(713) # NIST curve
    d = G.parameters()
    a, b, p = d["a"], d["b"], d["p"]
    g = G.generator()
    gx0, gy0 = g.get_affine()

    r = G.order().random()
    gx1, gy1 = (r*g).get_affine()

    assert is_point_on_curve(a, b, p, gx0, gy0)
    assert is_point_on_curve(a, b, p, gx1, gy1)

    ## Test a simple addition
    h = (r + 1) * g
    hx1, hy1 = h.get_affine()

    x, y = point_add(a, b, p, gx0, gy0, gx1, gy1)
    assert is_point_on_curve(a, b, p, x, y)
    assert x == hx1
    assert y == hy1

    ## Ensure commutativity
    xp, yp = point_add(a, b, p, gx1, gy1, gx0, gy0)
    assert is_point_on_curve(a, b, p, xp, yp)
    assert x == xp
    assert y == yp

    ## Ensure addition with neutral returns the element
    xp, yp = point_add(a, b, p, gx1, gy1, None, None)
    assert is_point_on_curve(a, b, p, xp, yp)
    assert xp == gx1
    assert yp == gy1
    
    xp, yp = point_add(a, b, p, None, None, gx0, gy0)
    assert is_point_on_curve(a, b, p, xp, yp)
    assert gx0 == xp
    assert gy0 == yp

    ## An error is raised in case the points are equal
    with raises(Exception) as excinfo:
        point_add(a, b, p, gx0, gy0, gx0, gy0)
    assert 'EC Points must not be equal' in str(excinfo.value)

@pytest.mark.task3
def test_Point_addition_check_inf_result():
    """
    Test whether the EC point addition is correct for pt - pt = inf
    """
    from pytest import raises
    from petlib.ec import EcGroup, EcPt
    G = EcGroup(713) # NIST curve
    d = G.parameters()
    a, b, p = d["a"], d["b"], d["p"]
    g = G.generator()
    gx0, gy0 = g.get_affine()
    gx1, gy1 = gx0, p - gy0


    assert is_point_on_curve(a, b, p, gx0, gy0)
    assert is_point_on_curve(a, b, p, gx1, gy1)

    x, y = point_add(a, b, p, gx0, gy0, gx1, gy1)
    assert is_point_on_curve(a, b, p, x, y)
    assert (x,y) == (None, None)



@pytest.mark.task3
def test_Point_doubling():
    """
    Test whether the EC point doubling is correct.
    """

    from pytest import raises
    from petlib.ec import EcGroup, EcPt
    G = EcGroup(713) # NIST curve
    d = G.parameters()
    a, b, p = d["a"], d["b"], d["p"]
    g = G.generator()
    gx0, gy0 = g.get_affine()

    gx2, gy2 = (2*g).get_affine()


    x2, y2 = point_double(a, b, p, gx0, gy0)
    assert is_point_on_curve(a, b, p, x2, y2)
    assert x2 == gx2 and y2 == gy2

    x2, y2 = point_double(a, b, p, None, None)
    assert is_point_on_curve(a, b, p, x2, y2)
    assert x2 == None and y2 == None

@pytest.mark.task3
def test_Point_scalar_mult_double_and_add():
    """
    Test the scalar multiplication using double and add.
    """

    from pytest import raises
    from petlib.ec import EcGroup, EcPt
    G = EcGroup(713) # NIST curve
    d = G.parameters()
    a, b, p = d["a"], d["b"], d["p"]
    g = G.generator()
    gx0, gy0 = g.get_affine()
    r = G.order().random()

    gx2, gy2 = (r*g).get_affine()


    x2, y2 = point_scalar_multiplication_double_and_add(a, b, p, gx0, gy0, r)
    assert is_point_on_curve(a, b, p, x2, y2)
    assert gx2 == x2
    assert gy2 == y2

@pytest.mark.task3
def test_Point_scalar_mult_montgomerry_ladder():
    """
    Test the scalar multiplication using double and add.
    """

    from pytest import raises
    from petlib.ec import EcGroup, EcPt
    G = EcGroup(713) # NIST curve
    d = G.parameters()
    a, b, p = d["a"], d["b"], d["p"]
    g = G.generator()
    gx0, gy0 = g.get_affine()

    r = G.order().random()

    gx2, gy2 = (r*g).get_affine()


    x2, y2 = point_scalar_multiplication_montgomerry_ladder(a, b, p, gx0, gy0, r)
    assert is_point_on_curve(a, b, p, x2, y2)
    assert gx2 == x2
    assert gy2 == y2

#####################################################
# TASK 4 -- Standard ECDSA signatures
#
#          - Implement a key / param generation 
#          - Implement ECDSA signature using petlib.ecdsa
#          - Implement ECDSA signature verification 
#            using petlib.ecdsa

@pytest.mark.task4
def test_key_gen():
    """ Tests the key generation of ECDSA"""
    from Lab01Code import ecdsa_key_gen
    G, priv, pub = ecdsa_key_gen()

@pytest.mark.task4
def test_produce_signature():
    """ Tests signature function """
    msg = u"Test" * 1000
    from Lab01Code import ecdsa_key_gen, ecdsa_sign

    G, priv, pub = ecdsa_key_gen()
    sig = ecdsa_sign(G, priv, msg)
    assert True

@pytest.mark.task4
def test_check_signature():
    """ Tests signature and verification function """
    msg = u"Test" * 1000

    G, priv, pub = ecdsa_key_gen()

    sig = ecdsa_sign(G, priv, msg)
    assert ecdsa_verify(G, pub, msg, sig)

@pytest.mark.task4
def test_check_fail():
    """ Ensures verification fails when it should """
    msg = u"Test" * 1000
    msg2 = u"Text" * 1000

    G, priv, pub = ecdsa_key_gen()

    sig = ecdsa_sign(G, priv, msg)

    assert not ecdsa_verify(G, pub, msg2, sig)


#####################################################
# TASK 5 -- Diffie-Hellman Key Exchange and Derivation
#           - use Bob's public key to derive a shared key.
#           - Use Bob's public key to encrypt a message.
#           - Use Bob's private key to decrypt the message.

@pytest.mark.task5
def test_key_gen():
    G, priv, pub = dh_get_key()
