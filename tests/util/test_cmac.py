from pylora.util.cmac import cmac_sign, cmac_verify

EXPECTED_SIGNATURE = b'|\xc2\xab\x06\xe5\xfb\x1f\xbf\xe8s\x83@8\x19\t\xb1'


def test_sign():
    signature = cmac_sign(b"message to authenticate", b"01020304050607080910111213141516")
    assert signature == EXPECTED_SIGNATURE


def test_verify_correct_signature():
    assert cmac_verify(b"message to authenticate", b"01020304050607080910111213141516", EXPECTED_SIGNATURE)


def test_not_verify_incorrect_signature():
    assert not cmac_verify(b"message to authenticate", b"01020304050607080910111213141516", b"an incorrect signature")
