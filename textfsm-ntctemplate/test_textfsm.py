import pytest
from textfsmlab import queriesDes

@pytest.fixture
def setup_teardown():
    print("\nSetup Testing")
    yield
    print("\nClean Testing")

@pytest.mark.usefixtures("setup_teardown")
def test_description_int_R1(setup_teardown):
    setup_teardown
    dataDes = queriesDes("172.31.18.4")
    for itef in dataDes:
        match itef["port"]:
            case "Gi0/0":
                assert itef["description"] == "Connect to Gig 0/1 of S0.ipa.com"
            case "Gi0/2":
                assert itef["description"] == "Connect to Gig 0/2 of R2.ipa.com"
            case "Gi0/1":
                assert itef["description"] == "Connect to PC"

@pytest.mark.usefixtures("setup_teardown")
def test_description_int_R2(setup_teardown):
    setup_teardown
    dataDes = queriesDes("172.31.18.5")
    for itef in dataDes:
        match itef["port"]:
            case "Gi0/0":
                assert itef["description"] == "Connect to Gig 0/2 of S0.ipa.com"
            case "Gi0/1":
                assert itef["description"] == "Connect to Gig 0/2 of R1.ipa.com"
            case "Gi0/2":
                assert itef["description"] == "Connect to Gig 0/1 of S1.ipa.com"
            case "Gi0/3":
                assert itef["description"] == "Connect to WAN"

@pytest.mark.usefixtures("setup_teardown")
def test_description_int_S1(setup_teardown):
    setup_teardown
    dataDes = queriesDes("172.31.18.3")
    for itef in dataDes:
        match itef["port"]:
            case "Gi0/0":
                assert itef["description"] == "Connect to Gig 0/3 of S0.ipa.com"
            case "Gi0/1":
                assert itef["description"] == "Connect to Gig 0/2 of R2.ipa.com"
            case "Gi1/1":
                assert itef["description"] == "Connect to PC"

if __name__ == "__main__":
    test_description_int_R1()
    test_description_int_R2()