import pytest


@pytest.fixture
def acmd(mycmd):
    adr = "a@autocrypt.org"
    mycmd.run_ok(["add-account", "--email-regex={}".format(adr)])
    mycmd.bot_adr = adr
    return mycmd


def test_ccstatus(acmd):
    acmd.run_ok(["cc-status"])
    acmd.run_ok(["cc-status", "-a", "default"], """
    found account 'default'
    Head Imprint: *
    Remote Url: 'http://*
    CC data stored in *account/default/muacryptcc*
    1 entries.
    """)


def test_ccsync(acmd):
    acmd.run_ok(["cc-send"])
