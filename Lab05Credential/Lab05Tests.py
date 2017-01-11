#####################################################
# GA17 Privacy Enhancing Technologies -- Lab 05
#
# Selective Disclosure (Anonymous) Credentials
#
# Run the tests through:
# $ py.test -v test_file_name.py

import pytest
from pytest import raises

try:
    from Lab05Solution import *
except:
    from Lab05Code import *


@pytest.mark.task1
def test_user_encryption():
    params = credential_setup()
    priv, pub = credential_KeyGenUser(params)
    v, ciphertext, proof = credential_EncryptUserSecret(params, pub, priv)
    assert credential_VerifyUserSecret(params, pub, ciphertext, proof)

@pytest.mark.task2
def test_issue_correct_MAC():
    params = credential_setup()
    priv, pub = credential_KeyGenUser(params)
    v, ciphertext, proof = credential_EncryptUserSecret(params, pub, priv)
    assert credential_VerifyUserSecret(params, pub, ciphertext, proof)

    # Check the MAC is correct
    issuer_params = credential_KeyGenIssuer(params)
    (Cx0, iparams), (sk, x0_bar) = issuer_params
    u, [a, b], proof = credential_Issuing(params, pub, ciphertext, issuer_params)
    u_p = b - priv * a
    assert u_p == (sk[0] + v * sk[1]) * u

@pytest.mark.task2
def test_issue_correct_MAC_proof():
    params = credential_setup()
    priv, pub = credential_KeyGenUser(params)
    v, ciphertext, proof = credential_EncryptUserSecret(params, pub, priv)
    assert credential_VerifyUserSecret(params, pub, ciphertext, proof)

    # Check the MAC is correct
    issuer_params = credential_KeyGenIssuer(params)
    (Cx0, iparams), (sk, x0_bar) = issuer_params
    u, E_u_prime, proof = credential_Issuing(params, pub, ciphertext, issuer_params)

    issuer_public_params = (Cx0, iparams)
    
    assert credential_Verify_Issuing(params, issuer_public_params, pub, u, ciphertext, E_u_prime, proof)

@pytest.mark.task2
def test_issue_correct_MAC_decrypt():
    params = credential_setup()
    priv, pub = credential_KeyGenUser(params)
    v, ciphertext, proof = credential_EncryptUserSecret(params, pub, priv)
    assert credential_VerifyUserSecret(params, pub, ciphertext, proof)

    # Check the MAC is correct
    issuer_params = credential_KeyGenIssuer(params)
    (Cx0, iparams), (sk, x0_bar) = issuer_params
    u, E_u_prime, proof = credential_Issuing(params, pub, ciphertext, issuer_params)

    (u, uprime) =  credential_Decrypt(params, priv, u, E_u_prime)
    assert uprime == (sk[0] + v * sk[1]) * u

@pytest.mark.task3
def test_Show():
    params = credential_setup()
    priv, pub = credential_KeyGenUser(params)
    v, ciphertext, proof = credential_EncryptUserSecret(params, pub, priv)
    assert credential_VerifyUserSecret(params, pub, ciphertext, proof)

    # Check the MAC is correct
    issuer_params = credential_KeyGenIssuer(params)
    (Cx0, iparams), (sk, x0_bar) = issuer_params
    u, E_u_prime, proof = credential_Issuing(params, pub, ciphertext, issuer_params)

    (u, uprime) =  credential_Decrypt(params, priv, u, E_u_prime)
    
    issuer_pub_params = (Cx0, iparams)
    tag, proof = credential_show(params, issuer_pub_params, u, uprime, v)

@pytest.mark.task3
def test_Show_Verify():
    params = credential_setup()
    priv, pub = credential_KeyGenUser(params)
    v, ciphertext, proof = credential_EncryptUserSecret(params, pub, priv)
    assert credential_VerifyUserSecret(params, pub, ciphertext, proof)

    # Check the MAC is correct
    issuer_params = credential_KeyGenIssuer(params)
    (Cx0, iparams), (sk, x0_bar) = issuer_params
    u, E_u_prime, proof = credential_Issuing(params, pub, ciphertext, issuer_params)

    (u, uprime) =  credential_Decrypt(params, priv, u, E_u_prime)
    
    issuer_pub_params = (Cx0, iparams)
    tag, proof = credential_show(params, issuer_pub_params, u, uprime, v)

    assert credential_show_verify(params, issuer_params, tag, proof)

@pytest.mark.task4
def test_Show_Verify_Pseudonym():
    params = credential_setup()
    priv, pub = credential_KeyGenUser(params)
    v, ciphertext, proof = credential_EncryptUserSecret(params, pub, priv)
    assert credential_VerifyUserSecret(params, pub, ciphertext, proof)

    # Check the MAC is correct
    issuer_params = credential_KeyGenIssuer(params)
    (Cx0, iparams), (sk, x0_bar) = issuer_params
    u, E_u_prime, proof = credential_Issuing(params, pub, ciphertext, issuer_params)

    (u, uprime) =  credential_Decrypt(params, priv, u, E_u_prime)
    
    issuer_pub_params = (Cx0, iparams)
    pseudonym, tag, proof = credential_show_pseudonym(params, issuer_pub_params, u, uprime, v, b"Service A")
    assert credential_show_verify_pseudonym(params, issuer_params, pseudonym, tag, proof, b"Service A")

@pytest.mark.task4
def test_Show_Verify_Pseudonym_stability():
    params = credential_setup()
    priv, pub = credential_KeyGenUser(params)
    v, ciphertext, proof = credential_EncryptUserSecret(params, pub, priv)
    assert credential_VerifyUserSecret(params, pub, ciphertext, proof)

    # Check the MAC is correct
    issuer_params = credential_KeyGenIssuer(params)
    (Cx0, iparams), (sk, x0_bar) = issuer_params
    u, E_u_prime, proof = credential_Issuing(params, pub, ciphertext, issuer_params)

    (u, uprime) =  credential_Decrypt(params, priv, u, E_u_prime)
    
    issuer_pub_params = (Cx0, iparams)
    pseudonym, tag, proof = credential_show_pseudonym(params, issuer_pub_params, u, uprime, v, b"Service A")
    assert credential_show_verify_pseudonym(params, issuer_params, pseudonym, tag, proof, b"Service A")

    pseudonym2, tag, proof = credential_show_pseudonym(params, issuer_pub_params, u, uprime, v, b"Service A")
    assert credential_show_verify_pseudonym(params, issuer_params, pseudonym2, tag, proof, b"Service A")

    assert pseudonym == pseudonym2