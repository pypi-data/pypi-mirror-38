# coding=utf-8

import string

import delegator
import pexpect
import pytest
from hypothesis import given, strategies as st
from mockito import mock, unstub, verify, when

import elib.run
from elib.run import filter_line


@pytest.fixture(name='process', autouse=True)
def _process():
    process = mock()
    subprocess = mock()
    process.out = 'output'
    process.err = ''
    process.name = 'test.exe'
    process.return_code = 0
    process.subprocess = subprocess
    when(delegator).run(...).thenReturn(process)
    when(elib.run).find_executable('test').thenReturn(process)
    when(elib.run).cmd_start(...)
    when(elib.run).cmd_end(...)
    when(elib.run).info(...)
    when(elib.run).error(...)
    when(elib.run).std_out(...)
    when(elib.run).std_err(...)
    yield process


@given(text=st.text(alphabet=string.printable))
def test_filter_line_raw(text):
    assert filter_line(text, None) == text


def test_filter_line():
    text = 'some random text'
    assert filter_line(text, None) == text
    assert filter_line(text, ['some']) is None
    assert filter_line(text, [' some']) == text
    assert filter_line(text, ['some ']) is None
    assert filter_line(text, ['random']) is None
    assert filter_line(text, [' random']) is None
    assert filter_line(text, ['random ']) is None
    assert filter_line(text, [' random ']) is None
    assert filter_line(text, ['text']) is None
    assert filter_line(text, [' text']) is None
    assert filter_line(text, [' text ']) == text


def test_exe_not_found():
    when(elib.run).find_executable(...).thenReturn(None)
    with pytest.raises(SystemExit):
        elib.run.run('test')


def _basic_check(output, code):
    verify(elib.run).info('test.exe -> 0')
    verify(elib.run, times=0).cmd_start(...)
    verify(elib.run, times=0).cmd_end(...)
    verify(elib.run, times=0).std_err(...)
    verify(elib.run).std_out(output)
    verify(elib.run, times=0).error(...)
    assert code == 0


@pytest.mark.parametrize(
    'input_,output',
    [
        ('test', 'test'),
        ('test\n', 'test'),
        ('test\n\n', 'test'),
        ('test\n\ntest', 'test\ntest'),
        ('test\n\ntest\n', 'test\ntest'),
        ('test\n\ntest\n\n', 'test\ntest'),
    ]
)
def test_output(process, input_, output):
    process.out = input_
    out, code = elib.run.run('test')
    _basic_check(out, code)
    assert out == output


def test_no_output(process):
    process.out = ''
    out, code = elib.run.run('test')
    _basic_check(out, code)
    assert out == ''


def test_filtered_output():
    out, code = elib.run.run('test', filters=['output'])
    _basic_check(out, code)
    assert out == ''


def test_mute_output():
    out, code = elib.run.run('test', mute=True)
    verify(elib.run, times=0).info(...)
    verify(elib.run, times=0).error(...)
    verify(elib.run).cmd_end(' -> 0')
    verify(elib.run, times=0).std_err(...)
    verify(elib.run, times=0).std_out(...)
    assert code == 0
    assert out == 'output'


def test_filter_as_str(process):
    process.out = 'output\ntest'
    out, code = elib.run.run('test', mute=True, filters='test')
    verify(elib.run, times=0).info(...)
    verify(elib.run, times=0).error(...)
    verify(elib.run).cmd_end(' -> 0')
    verify(elib.run, times=0).std_err(...)
    verify(elib.run, times=0).std_out(...)
    assert code == 0
    assert out == 'output'


def test_error(process):
    process.return_code = 1
    process.out = 'some error'
    out, code = elib.run.run('test', filters=['output'], failure_ok=True)
    verify(elib.run, times=0).cmd_start(...)
    verify(elib.run, times=0).cmd_end(...)
    verify(elib.run).std_err('test.exe error:\nsome error')
    verify(elib.run, times=0).std_out(...)
    verify(elib.run, times=1).error('command failed: test.exe -> 1')
    assert code == 1
    assert out == 'some error'


def test_error_no_result(process):
    process.return_code = 1
    process.out = ''
    out, code = elib.run.run('test', filters=['output'], failure_ok=True)
    verify(elib.run, times=0).cmd_start(...)
    verify(elib.run, times=0).cmd_end(...)
    verify(elib.run, times=0).std_err(...)
    verify(elib.run, times=0).std_out(...)
    verify(elib.run).error('command failed: test.exe -> 1')
    assert code == 1
    assert out == ''


def test_error_muted(process):
    process.return_code = 1
    unstub(process.subprocess)
    when(process.subprocess).read_nonblocking(1, None).thenReturn('some output').thenRaise(pexpect.exceptions.EOF(None))
    out, code = elib.run.run('test', filters=['output'], failure_ok=True, mute=True)
    verify(elib.run, times=0).info(...)
    verify(elib.run).cmd_end('')
    verify(elib.run, times=0).std_err(...)
    verify(elib.run, times=0).std_out(...)
    verify(elib.run).error('command failed: test.exe -> 1')
    assert code == 1
    assert out == ''


def test_failure(process):
    process.return_code = 1
    process.out = 'error'
    with pytest.raises(SystemExit):
        elib.run.run('test', filters=['output'])
    verify(elib.run, times=0).cmd_start(...)
    verify(elib.run, times=0).cmd_end(...)
    verify(elib.run).std_err('test.exe error:\nerror')
    verify(elib.run, times=0).std_out(...)
    verify(elib.run).error('command failed: test.exe -> 1')
