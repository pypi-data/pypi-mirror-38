from plover_retro_case.change_case import (
    change_case
)
def test_change_case():
    assert change_case(['environment', 'dev'], False, False, '_') == 'dev_environment'
    assert change_case(['environment', 'dev '], False, True, '') == 'devEnvironment'
    assert change_case(['engine', 'test'], True, True, '') == 'TestEngine'
    assert change_case(['testTest', 'test'], True, True, '') == 'TestTestTest'
