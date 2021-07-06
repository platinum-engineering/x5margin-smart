import pytest
from test_pool_service import _prepare_open_position, _open_position


def _open_position_for_testing(amount, accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice, contract_poolservice, contract_positionrepository):
    _prepare_open_position(contract_positionrepository, contract_poolservice)
    _open_position(amount, accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice, contract_poolservice)


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_position(accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice, contract_poolservice, contract_positionrepository):
    amount = 1e18
    _open_position_for_testing(amount, accounts, contract_gtoken, contract_underlyingtoken, contract_vaultservice, contract_poolservice, contract_positionrepository)
    amountCurrent, leveragedAmount, _ = contract_positionrepository.getPositionDetails(contract_poolservice, accounts[0])
    addrToken, amountTokenCurrent = contract_positionrepository.getTokenById(contract_poolservice, accounts[0], 0)
    assert (contract_positionrepository.hasOpenPosition(contract_poolservice, accounts[0])) & \
           (contract_positionrepository.tradersCount(contract_poolservice) == 1) & \
           (contract_positionrepository.getTraderById(contract_poolservice, 0) == accounts[0]) & \
           (amountCurrent == amount) & \
           (leveragedAmount == amount*4) & \
           (contract_positionrepository.getTokenListCount(contract_poolservice, accounts[0]) == 1) & \
           (amountTokenCurrent == amount*4) & \
           (addrToken == contract_underlyingtoken)
