from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from stypuff_interpreter import StypuffEngine


def test_data_stypuff_example_executes_without_errors():
    source = '''
    @datalist{
        §value("Bash").id("1")
        §value("PowerShell").id("2")
    }
    '''
    engine = StypuffEngine()
    engine.execute(source)


def test_codelist_style_set_class_and_event_syntax_executes():
    source = '''
    styp.create("demo")
    set @data("player") = {}
    set @variable("score") = 10
    class("Pessoa") = {
        let nome = "Ana"
    }
    on @variable("clicked"):: $itsDisplaying("button") {
        print("clicked")
    }
    '''
    engine = StypuffEngine()
    engine.execute(source)
