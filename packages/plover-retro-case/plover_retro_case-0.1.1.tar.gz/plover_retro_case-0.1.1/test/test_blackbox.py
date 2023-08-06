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
        "TH-": "this",
        "KAPL": "{:retro_case:false:true}",

        TEFT " test"
        TH " test this"
        TEFT " test this test"
        KAPL " test thisTest"
        KAPL " testThisTest"
        KAPL " testThisTest"
        '''

    def test_pascal_case(self):
        r'''
        "TEFT": "test",
        "TH-": "this",
        "PAFBG": "{:retro_case:true:true}"

        TEFT " test"
        TH " test this"
        TEFT " test this test"
        PAFBG " test ThisTest"
        PAFBG " TestThisTest"
        '''

    def test_snake_case(self):
        r'''
        "TEFT": "test",
        "TH-": "this",
        "STPHAEUBG": "{:retro_case:false:false:_}"

        TEFT " test"
        TH " test this"
        TEFT " test this test"
        STPHAEUBG " test this_test"
        STPHAEUBG " test_this_test"
        '''
