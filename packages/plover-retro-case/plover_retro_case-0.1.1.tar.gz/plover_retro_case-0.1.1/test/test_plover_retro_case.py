from plover_retro_case.change_case import (
    change_case
)
def test_change_case():
    assert change_case(['dev', 'environment'], False, False, '_') == 'dev_environment'
    assert change_case(['dev ', 'environment'], False, True, '') == 'devEnvironment'
    assert change_case(['test ', 'engine'], True, True, '') == 'TestEngine'
    assert change_case(['test', 'thisTest'], True, True, '') == 'TestThisTest'
