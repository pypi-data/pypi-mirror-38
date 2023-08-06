
from click.testing import CliRunner

from strengthtrainingtoolkit.cli import main


def test_main():  # TODO: implement testing library
    runner = CliRunner()
    result = runner.invoke(main, [])

    assert result.output == '()\n'
    assert result.exit_code == 0
