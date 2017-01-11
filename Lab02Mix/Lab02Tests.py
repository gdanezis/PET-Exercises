#####################################################
# GA17 Privacy Enhancing Technologies -- Lab 02
#
# Basics of Mix networks and Traffic Analysis
#
# Run the tests through:
# $ py.test -v test_file_name.py

#####################################################
# TASK 1 -- Ensure petlib is installed on the System
#           and also pytest. Ensure the Lab Code can 
#           be imported.

import pytest
from pytest import raises

try:
    from Lab02Solution import *
except:
    from Lab02Code import *


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
    import Lab02Code 
    assert True

#####################################################
# TASK 2 -- Build a 1-hop mix client.
#
#

from petlib.ec import EcGroup

## What is a test fixture?
#  http://pytest.org/latest/fixture.html

@pytest.fixture
def encode_Alice_message():
    """
    Encode a single message
    """

    G = EcGroup()
    g = G.generator()
    o = G.order()

    private_key = o.random()
    public_key  = private_key * g

    m1 = mix_client_one_hop(public_key, b"Alice", b"Dear Alice,\nHello!\nBob")
    return private_key, m1

@pytest.mark.task2
def test_Alice_message_overlong():
    """
    Test overlong address or message
    """

    from os import urandom

    G = EcGroup()
    g = G.generator()
    o = G.order()

    private_key = o.random()
    public_key  = private_key * g

    with raises(Exception) as excinfo:
        mix_client_one_hop(public_key, urandom(1000), b"Dear Alice,\nHello!\nBob")
    
    with raises(Exception) as excinfo:
        mix_client_one_hop(public_key, b"Alice", urandom(10000))


@pytest.mark.task2
def test_simple_client_part_type(encode_Alice_message):
    private_key, Alice_message = encode_Alice_message
    
    # Ensure the client encodes a NamedTuple of type "OneHopMixMessage"
    assert isinstance(Alice_message, tuple)
    assert len(Alice_message) == 4
    assert Alice_message.ec_public_key
    assert Alice_message.hmac
    assert Alice_message.address
    assert Alice_message.message

@pytest.mark.task2
def test_simple_client_decode(encode_Alice_message):
    private_key, Alice_message = encode_Alice_message

    # Ensure the mix can decode the message correctly    
    res1 = mix_server_one_hop(private_key, [Alice_message])

    assert len(res1) == 1
    assert res1[0][0] == b"Alice"
    assert res1[0][1] == b"Dear Alice,\nHello!\nBob"

@pytest.mark.task2
def test_simple_client_decode_many():
    
    from os import urandom

    G = EcGroup()
    g = G.generator()
    o = G.order()

    private_key = o.random()
    public_key  = private_key * g

    messages = []
    for _ in range(100):
        m = mix_client_one_hop(public_key, urandom(256), urandom(1000))
        messages += [m]

    # Ensure the mix can decode the message correctly    
    res1 = mix_server_one_hop(private_key, messages)

    assert len(res1) == 100

###################################
# TASK 3 -- A multi-hop mix

@pytest.mark.task3
def test_Alice_encode_1_hop():
    """
    Test sending a multi-hop message through 1-hop
    """

    from os import urandom

    G = EcGroup()
    g = G.generator()
    o = G.order()

    private_key = o.random()
    public_key  = private_key * g

    address = b"Alice"
    message = b"Dear Alice,\nHello!\nBob"

    m1 = mix_client_n_hop([public_key], address, message)
    out = mix_server_n_hop(private_key, [m1], final=True)

    assert len(out) == 1
    assert out[0][0] == address
    assert out[0][1] == message

@pytest.mark.task3
def test_Alice_encode_3_hop():
    """
    Test sending a multi-hop message through 1-hop
    """

    from os import urandom

    G = EcGroup()
    g = G.generator()
    o = G.order()

    private_keys = [o.random() for _ in range(3)]
    public_keys  = [pk * g for pk in private_keys]

    address = b"Alice"
    message = b"Dear Alice,\nHello!\nBob"

    m1 = mix_client_n_hop(public_keys, address, message)
    out = mix_server_n_hop(private_keys[0], [m1])
    out = mix_server_n_hop(private_keys[1], out)
    out = mix_server_n_hop(private_keys[2], out, final=True)

    assert len(out) == 1
    assert out[0][0] == address
    assert out[0][1] == message

###########################################
## TASK 4 -- Simple traffic analysis / SDA

import random

@pytest.mark.task4
def test_trace_static():
    # A fixed set and number of friends
    trace = generate_trace(100, 10, 1000, [1,2,3])
    friends = analyze_trace(trace, 3)
    assert len(friends) == 3
    assert sorted(friends) == [1,2,3]

@pytest.mark.task4
def test_trace_variable():
    # A random number of friends and random contacts
    friend_number = random.choice(range(1,10))
    friends = random.sample(range(100), friend_number)

    trace = generate_trace(100, 10, 1000, friends)
    TA_friends = analyze_trace(trace, len(friends))
    assert len(TA_friends) == len(friends)
    assert sorted(TA_friends) == sorted(friends)

