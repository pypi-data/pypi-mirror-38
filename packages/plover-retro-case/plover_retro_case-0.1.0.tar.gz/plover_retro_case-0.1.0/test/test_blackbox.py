from plover_build_utils.testing import BlackboxTester
from plover.registry import registry
from plover import system

class TestsBlackbox(BlackboxTester):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        registry.update()
        system.setup('English Stenotype')

    def test_camel_case(self):
        r'''
        "TEFT": "test",
        "KAPL": "{:retro_case:false:true}",

        TEFT " test"
        TEFT " test test"
        TEFT " test test test"
        KAPL " test testTest"
        KAPL " testTestTest"
        KAPL " testTestTest"
        '''

    def test_pascal_case(self):
        r'''
        "TEFT": "test",
        "PAFBG": "{:retro_case:true:true}"

        TEFT " test"
        TEFT " test test"
        TEFT " test test test"
        PAFBG " test TestTest"
        PAFBG " TestTestTest"
        '''

    def test_snake_case(self):
        r'''
        "TEFT": "test",
        "STPHAEUBG": "{:retro_case:false:false:_}"

        TEFT " test"
        TEFT " test test"
        TEFT " test test test"
        STPHAEUBG " test test_test"
        STPHAEUBG " test_test_test"
        '''
