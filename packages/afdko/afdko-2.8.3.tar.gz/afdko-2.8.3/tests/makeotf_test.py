# coding: utf-8

from __future__ import print_function, division, absolute_import

import os
import pytest
from shutil import copy2, copytree, rmtree
import subprocess32 as subprocess
import sys
import tempfile

from afdko.makeotf import (
    checkIfVertInFeature, getOptions, MakeOTFParams, getSourceGOADBData,
    readOptionFile, writeOptionsFile, kMOTFOptions, kOptionNotSeen,
    makeRelativePath)

from runner import main as runner
from differ import main as differ, SPLIT_MARKER
from test_utils import (get_input_path, get_expected_path, get_temp_file_path,
                        generate_ttx_dump, font_has_table)

TOOL = 'makeotf'
CMD = ['-t', TOOL]

T1PFA_NAME = 't1pfa.pfa'
UFO2_NAME = 'ufo2.ufo'
UFO3_NAME = 'ufo3.ufo'
CID_NAME = 'cidfont.ps'
TTF_NAME = 'font.ttf'
OTF_NAME = 'SourceSans-Test.otf'

DATA_DIR = os.path.join(os.path.split(__file__)[0], TOOL + '_data')
TEMP_DIR = os.path.join(DATA_DIR, 'temp_output')


xfail_py36_win = pytest.mark.xfail(
    sys.version_info >= (3, 0) and sys.platform == 'win32',
    reason="Console's encoding is not UTF-8 ?")


def setup_module():
    """
    Create the temporary output directory
    """
    os.mkdir(TEMP_DIR)


def teardown_module():
    """
    teardown the temporary output directory
    """
    rmtree(TEMP_DIR)


# -----
# Tests
# -----

def test_exit_no_option():
    # It's valid to run 'makeotf' without using any options,
    # but if a default-named font file is NOT found in the
    # current directory, the tool exits with an error
    with pytest.raises(subprocess.CalledProcessError) as err:
        subprocess.check_call([TOOL])
    assert err.value.returncode == 1


@pytest.mark.parametrize('arg', ['-v', '-h', '-u'])
def test_exit_known_option(arg):
    assert subprocess.call([TOOL, arg]) == 0


@pytest.mark.parametrize('arg', ['-j', '--bogus'])
def test_exit_unknown_option(arg):
    assert subprocess.call([TOOL, arg]) == 1


@pytest.mark.parametrize('arg, input_filename, ttx_filename', [
    ([], T1PFA_NAME, 't1pfa-dev.ttx'),
    ([], UFO2_NAME, 'ufo2-dev.ttx'),
    ([], UFO3_NAME, 'ufo3-dev.ttx'),
    ([], CID_NAME, 'cidfont-dev.ttx'),
    ([], TTF_NAME, 'ttf-dev.ttx'),
    (['r'], T1PFA_NAME, 't1pfa-rel.ttx'),
    (['r'], UFO2_NAME, 'ufo2-rel.ttx'),
    (['r'], UFO3_NAME, 'ufo3-rel.ttx'),
    (['r'], CID_NAME, 'cidfont-rel.ttx'),
    (['r', 'gf'], TTF_NAME, 'ttf-rel.ttx'),
])
def test_input_formats(arg, input_filename, ttx_filename):
    if 'gf' in arg:
        arg.append('_{}'.format(get_input_path('GOADB.txt')))
    actual_path = get_temp_file_path()
    runner(CMD + ['-o', 'f', '_{}'.format(get_input_path(input_filename)),
                        'o', '_{}'.format(actual_path)] + arg)
    actual_ttx = generate_ttx_dump(actual_path)
    expected_ttx = get_expected_path(ttx_filename)
    assert differ([expected_ttx, actual_ttx,
                   '-s',
                   '<ttFont sfntVersion' + SPLIT_MARKER +
                   '    <checkSumAdjustment value=' + SPLIT_MARKER +
                   '    <created value=' + SPLIT_MARKER +
                   '    <modified value=',
                   '-r', r'^\s+Version.*;hotconv.*;makeotfexe'])


def test_getSourceGOADBData():
    ttf_path = get_input_path('font.ttf')
    assert getSourceGOADBData(ttf_path) == [['.notdef', '.notdef', ''],
                                            ['a', 'a', 'uni0041'],
                                            ['g2', 'g2', '']]


@xfail_py36_win
@pytest.mark.parametrize('input_filename', [
    T1PFA_NAME, UFO2_NAME, UFO3_NAME, CID_NAME])
def test_path_with_non_ascii_chars_bug222(input_filename):
    temp_dir = os.path.join(tempfile.mkdtemp(), 'á意ê  ï薨õ 巽ù')
    os.makedirs(temp_dir)
    assert os.path.isdir(temp_dir)
    input_path = get_input_path(input_filename)
    temp_path = os.path.join(temp_dir, input_filename)
    if os.path.isdir(input_path):
        copytree(input_path, temp_path)
    else:
        copy2(input_path, temp_path)
    expected_path = os.path.join(temp_dir, OTF_NAME)
    assert os.path.exists(expected_path) is False
    runner(CMD + ['-o', 'f', '_{}'.format(temp_path)])
    assert os.path.isfile(expected_path)


@pytest.mark.parametrize('input_filename', [UFO2_NAME, UFO3_NAME])
def test_ufo_with_trailing_slash_bug280(input_filename):
    # makeotf will now save the OTF alongside the UFO instead of inside of it
    ufo_path = get_input_path(input_filename)
    temp_dir = tempfile.mkdtemp()
    tmp_ufo_path = os.path.join(temp_dir, input_filename)
    copytree(ufo_path, tmp_ufo_path)
    runner(CMD + ['-o', 'f', '_{}{}'.format(tmp_ufo_path, os.sep)])
    expected_path = os.path.join(temp_dir, OTF_NAME)
    assert os.path.isfile(expected_path)


@pytest.mark.parametrize('input_filename', [
    T1PFA_NAME, UFO2_NAME, UFO3_NAME, CID_NAME])
def test_output_is_folder_only_bug281(input_filename):
    # makeotf will output a default-named font to the folder
    input_path = get_input_path(input_filename)
    temp_dir = tempfile.mkdtemp()
    expected_path = os.path.join(temp_dir, OTF_NAME)
    assert os.path.exists(expected_path) is False
    runner(CMD + ['-o', 'f', '_{}'.format(input_path),
                        'o', '_{}'.format(temp_dir)])
    assert os.path.isfile(expected_path)


@pytest.mark.parametrize('input_filename', [
    't1pfa-noPSname.pfa',
    'ufo2-noPSname.ufo',
    'ufo3-noPSname.ufo',
    'cidfont-noPSname.ps',
])
def test_no_postscript_name_bug282(input_filename):
    # makeotf will fail for both UFO and Type 1 inputs
    with pytest.raises(subprocess.CalledProcessError) as err:
        runner(CMD + ['-o', 'f', '_{}'.format(input_filename)])
    assert err.value.returncode == 1


@pytest.mark.parametrize('fea_filename, result', [
    (None, 0),  # No feature path at...
    ('missing_file', 0),  # No feature path at...
    ('feat0.fea', 0),
    ('feat1.fea', 1),
    ('feat2.fea', 0),  # Could not find the include file...
    ('feat3.fea', 0),  # Could not find the include file...
    ('feat4.fea', 1),
])
def test_find_vert_feature_bug148(fea_filename, result):
    fea_path = None
    if fea_filename:
        input_dir = get_input_path('bug148')
        fea_path = os.path.join(input_dir, fea_filename)
    assert checkIfVertInFeature(fea_path) == result


@pytest.mark.parametrize('args, result', [
    # 'result' corresponds to the values of the
    # options 'ReleaseMode' and 'SuppressHintWarnings'
    ([], (None, None)),
    (['-r'], ('true', None)),
    (['-shw'], (None, None)),
    (['-nshw'], (None, 'true')),
    (['-r', '-shw'], ('true', None)),
    (['-r', '-nshw'], ('true', 'true')),
    # makeotf option parsing has no mechanism for mutual exclusivity,
    # so the last option typed on the command line wins
    (['-shw', '-nshw'], (None, 'true')),
    (['-nshw', '-shw'], (None, None)),
])
def test_options_shw_nshw_bug457(args, result):
    params = MakeOTFParams()
    getOptions(params, args)
    assert params.opt_ReleaseMode == result[0]
    assert params.opt_SuppressHintWarnings == result[1]


@pytest.mark.parametrize('args, result', [
    # 'result' corresponds to the values of the
    # options 'MacCmapScriptID' and 'MacCmapLanguageID'
    # CJK MacCmapScriptIDs: Japan/1, CN/2, Korea/3, GB/25
    ([], (None, None)),
    (['-cs', '1'], (1, None)),
    (['-cl', '2'], (None, 2)),
    (['-cs', '4', '-cl', '5'], (4, 5)),
])
def test_options_cs_cl_bug459(args, result):
    params = MakeOTFParams()
    getOptions(params, args)
    assert params.opt_MacCmapScriptID == result[0]
    assert params.opt_MacCmapLanguageID == result[1]


def test_writeOptionsFile():
    actual_path = get_temp_file_path()
    expected_path = get_expected_path('proj_write.txt')
    params = MakeOTFParams()
    params.currentDir = os.path.dirname(actual_path)
    params.opt_InputFontPath = 'font.pfa'
    params.opt_OutputFontPath = 'fôñt.otf'
    params.opt_kSetfsSelectionBitsOn = [7]
    params.opt_kSetfsSelectionBitsOff = [9, 8]
    params.opt_ConvertToCID = 'true'
    params.opt_kSetOS2Version = 3
    params.verbose = True
    # set options's sort order
    kMOTFOptions['InputFontPath'][0] = 1
    kMOTFOptions['OutputFontPath'][0] = kOptionNotSeen + 1
    kMOTFOptions['kSetfsSelectionBitsOn'][0] = 30
    writeOptionsFile(params, actual_path)
    assert differ([expected_path, actual_path])


def test_readOptionFile():
    INPUT_FONT_NAME = 'font.pfa'
    OUTPUT_FONT_NAME = 'font.otf'
    proj_path = get_input_path('proj.txt')
    abs_font_dir_path = os.path.dirname(proj_path)
    params = MakeOTFParams()
    assert params.fontDirPath == '.'

    params.currentDir = os.path.dirname(proj_path)
    assert readOptionFile(proj_path, params, 1) == (True, 7)
    assert params.fontDirPath == '.'
    assert params.opt_InputFontPath == INPUT_FONT_NAME
    assert params.opt_OutputFontPath == OUTPUT_FONT_NAME
    assert params.opt_ConvertToCID == 'true'
    assert params.opt_kSetfsSelectionBitsOff == '[8, 9]'
    assert params.opt_kSetfsSelectionBitsOn == [7]
    assert params.seenOS2v4Bits == [1, 1, 1]
    assert params.opt_UseOldNameID4 is None

    params.currentDir = os.getcwd()
    font_dir_path = os.path.relpath(abs_font_dir_path, params.currentDir)
    input_font_path = os.path.join(font_dir_path, INPUT_FONT_NAME)
    output_font_path = os.path.join(font_dir_path, OUTPUT_FONT_NAME)
    assert readOptionFile(proj_path, params, 1) == (True, 7)
    assert params.fontDirPath == os.path.normpath(font_dir_path)
    assert params.opt_InputFontPath == os.path.normpath(input_font_path)
    assert params.opt_OutputFontPath == os.path.normpath(output_font_path)


def test_readOptionFile_abspath():
    proj_path = get_input_path('proj2.txt')
    params = MakeOTFParams()

    root = os.path.abspath(os.sep)
    params.currentDir = os.path.join(root, 'different_dir')
    assert readOptionFile(proj_path, params, 1) == (False, 3)
    assert params.fontDirPath.startswith(root)
    assert params.opt_InputFontPath.startswith(root)
    assert params.opt_OutputFontPath.startswith(root)


@pytest.mark.parametrize('cur_dir_str', [
    'different_dir',
    './different_dir',
    '../different_dir',
])
def test_readOptionFile_relpath(cur_dir_str):
    INPUT_FONT_NAME = 'font.pfa'
    OUTPUT_FONT_NAME = 'font.otf'
    proj_path = get_input_path('proj2.txt')
    abs_font_dir_path = os.path.dirname(proj_path)
    params = MakeOTFParams()

    if '/' in cur_dir_str:
        # flip the slashes used in the test's input string
        params.currentDir = os.path.normpath(cur_dir_str)
    else:
        params.currentDir = cur_dir_str

    font_dir_path = os.path.relpath(abs_font_dir_path, params.currentDir)

    if cur_dir_str.startswith('..') and os.path.dirname(os.getcwd()) == os.sep:
        # the project is inside a folder located at the root level;
        # remove the two dots at the start of the path, otherwise
        # testing input '../different_dir' will fail.
        font_dir_path = font_dir_path[2:]

    input_font_path = os.path.join(font_dir_path, INPUT_FONT_NAME)
    output_font_path = os.path.join(font_dir_path, OUTPUT_FONT_NAME)
    assert readOptionFile(proj_path, params, 1) == (False, 3)
    assert params.fontDirPath == os.path.normpath(font_dir_path)
    assert params.opt_InputFontPath == os.path.normpath(input_font_path)
    assert params.opt_OutputFontPath == os.path.normpath(output_font_path)


def test_readOptionFile_filenotfound():
    proj_path = get_input_path('notafile')
    params = MakeOTFParams()
    params.currentDir = os.getcwd()
    assert readOptionFile(proj_path, params, 0) == (True, 0)


@pytest.mark.parametrize('cur_dir, target_path, result', [
    ('/folder/folder2', '/folder/folder2/font.pfa', 'font.pfa'),
    ('/folder/folder2', '/folder/font.pfa', '../font.pfa'),
    ('/folder', '/folder/font.pfa', 'font.pfa'),
    ('/folder', '/font.pfa', '../font.pfa'),
    ('/folder', None, None),
])
def test_makeRelativePath(cur_dir, target_path, result):
    if result:
        result = os.path.normpath(result)
    assert makeRelativePath(cur_dir, target_path) == result


@pytest.mark.skipif(sys.platform != 'win32', reason="windows-only")
@pytest.mark.parametrize('cur_dir, target_path, result', [
    ('C:\\folder', 'C:\\folder\\font.pfa', 'font.pfa'),
    ('F:\\folder', 'C:\\folder\\font.pfa', 'C:\\folder\\font.pfa'),
])
def test_makeRelativePath_win_only(cur_dir, target_path, result):
    assert makeRelativePath(cur_dir, target_path) == result


@pytest.mark.parametrize('args, input_filename, ttx_filename', [
    (['r'], T1PFA_NAME, 't1pfa-cmap.ttx'),
    (['r', 'cs', '_1'], T1PFA_NAME, 't1pfa-cmap_cs1.ttx'),
    (['r', 'cl', '_2'], T1PFA_NAME, 't1pfa-cmap_cl2.ttx'),
    (['r'], UFO2_NAME, 'ufo2-cmap.ttx'),
    (['r', 'cs', '_4'], UFO2_NAME, 'ufo2-cmap_cs4.ttx'),
    (['r', 'cl', '_5'], UFO2_NAME, 'ufo2-cmap_cl5.ttx'),
    (['r'], UFO3_NAME, 'ufo3-cmap.ttx'),
    (['r', 'cs', '_4'], UFO3_NAME, 'ufo3-cmap_cs4.ttx'),
    (['r', 'cl', '_5'], UFO3_NAME, 'ufo3-cmap_cl5.ttx'),
    (['r'], CID_NAME, 'cidfont-cmap.ttx'),
    (['r', 'cs', '_2'], CID_NAME, 'cidfont-cmap_cs2.ttx'),
    (['r', 'cl', '_3'], CID_NAME, 'cidfont-cmap_cl3.ttx'),
])
def test_build_options_cs_cl_bug459(args, input_filename, ttx_filename):
    actual_path = get_temp_file_path()
    runner(CMD + ['-o', 'f', '_{}'.format(get_input_path(input_filename)),
                        'o', '_{}'.format(actual_path)] + args)
    actual_ttx = generate_ttx_dump(actual_path, ['cmap'])
    expected_ttx = get_expected_path(ttx_filename)
    assert differ([expected_ttx, actual_ttx, '-s', '<ttFont sfntVersion'])


@pytest.mark.parametrize('args, font, fontinfo', [
    (['cn'], 'type1', ''),
    (['cn'], 'no_notdef', ''),
    (['cn'], 'blank_notdef', ''),
    (['cn'], 'notdef_not1st', ''),
    (['cn', 'fi'], 'type1', 'fi'),
    (['cn', 'fi'], 'type1', 'fi2'),
    (['cn', 'fi'], 'no_notdef', 'fi'),
    (['cn', 'fi'], 'no_notdef', 'fi2'),
    (['cn', 'fi'], 'blank_notdef', 'fi'),
    (['cn', 'fi'], 'blank_notdef', 'fi2'),
    (['cn', 'fi'], 'notdef_not1st', 'fi'),
    (['cn', 'fi'], 'notdef_not1st', 'fi2'),
])
def test_cid_keyed_cff_bug470(args, font, fontinfo):
    if 'fi' in args:
        fontinfo_file = 'bug470/{}.txt'.format(fontinfo)
        args.append('_{}'.format(get_input_path(fontinfo_file)))
        ttx_file = 'bug470/{}-{}.ttx'.format(font, 'fi')
    else:
        ttx_file = 'bug470/{}.ttx'.format(font)
    font_file = 'bug470/{}.pfa'.format(font)
    # 'dir=TEMP_DIR' is used for guaranteeing that the temp data is on same
    # file system as other data; if it's not, a file rename step made by
    # sfntedit will NOT work.
    actual_path = get_temp_file_path(directory=TEMP_DIR)
    runner(CMD + ['-o', 'f', '_{}'.format(get_input_path(font_file)),
                        'o', '_{}'.format(actual_path)] + args)
    actual_ttx = generate_ttx_dump(actual_path, ['CFF '])
    expected_ttx = get_expected_path(ttx_file)
    assert differ([expected_ttx, actual_ttx, '-s', '<ttFont sfntVersion'])


@pytest.mark.parametrize('opts', [
    [],
    ['r'],
    ['ga'],
    ['r', 'ga'],
    ['nga'],
    ['r', 'nga'],
    ['gf'],
    ['r', 'gf'],
    ['gf', 'ga'],
    ['gf', 'ga', 'nga'],  # GOADB will be applied, because 'ga' is first
    ['gf', 'nga'],
    ['gf', 'nga', 'ga'],  # GOADB not applied, because 'nga' is first
    ['r', 'ga', 'gf'],
    ['bit7n', 'bit8n', 'bit9n'],
    ['bit7y', 'bit8y', 'bit9y'],
    ['bit7y', 'bit8n', 'bit9n'],
    ['bit7y', 'bit8n', 'bit7n', 'bit8y'],
])
def test_GOADB_options_bug497(opts):
    font_path = get_input_path(T1PFA_NAME)
    feat_path = get_input_path('bug497/feat.fea')
    fmndb_path = get_input_path('bug497/fmndb.txt')
    goadb_path = get_input_path('bug497/goadb.txt')
    actual_path = get_temp_file_path()
    ttx_filename = '-'.join(['opts'] + opts) + '.ttx'

    args = []
    for opt in opts:  # order of the opts is important
        if opt == 'r':
            args.append(opt)
        elif opt == 'ga':
            args.append(opt)
        elif opt == 'nga':
            args.append(opt)
        elif opt == 'gf':
            args.extend([opt, '_{}'.format(goadb_path)])
        elif 'bit' in opt:
            bit_num = int(opt[3])
            bit_bol = 'osbOn' if opt[4] == 'y' else 'osbOff'
            args.extend([bit_bol, '_{}'.format(bit_num)])

    runner(CMD + ['-o', 'f', '_{}'.format(font_path),
                        'o', '_{}'.format(actual_path),
                        'ff', '_{}'.format(feat_path),
                        'mf', '_{}'.format(fmndb_path)] + args)
    actual_ttx = generate_ttx_dump(actual_path)
    expected_ttx = get_expected_path('bug497/{}'.format(ttx_filename))
    assert differ([expected_ttx, actual_ttx,
                   '-s',
                   '<ttFont sfntVersion' + SPLIT_MARKER +
                   '    <checkSumAdjustment value=' + SPLIT_MARKER +
                   '    <checkSumAdjustment value=' + SPLIT_MARKER +
                   '    <created value=' + SPLIT_MARKER +
                   '    <modified value=',
                   '-r', r'^\s+Version.*;hotconv.*;makeotfexe'])


@pytest.mark.parametrize('feat_name, has_warn', [('v0005', False),
                                                 ('ADBE', True)])
def test_fetch_font_version_bug610(feat_name, has_warn):
    input_filename = 't1pfa.pfa'
    feat_filename = 'bug610/{}.fea'.format(feat_name)
    otf_path = get_temp_file_path()

    stdout_path = runner(
        CMD + ['-s', '-o', 'r',
               'f', '_{}'.format(get_input_path(input_filename)),
               'ff', '_{}'.format(get_input_path(feat_filename)),
               'o', '_{}'.format(otf_path)])

    with open(stdout_path, 'rb') as f:
        output = f.read()
    assert b"Revision 0.005" in output
    assert (b"[Warning] Major version number not in "
            b"range 1 .. 255" in output) is has_warn


def test_update_cff_bbox_bug617():
    input_filename = "bug617/font.pfa"
    goadb_filename = "bug617/goadb.txt"
    actual_path = get_temp_file_path()
    ttx_filename = "bug617.ttx"
    runner(CMD + ['-o', 'f', '_{}'.format(get_input_path(input_filename)),
                        'gf', '_{}'.format(get_input_path(goadb_filename)),
                        'o', '_{}'.format(actual_path), 'r', 'gs'])
    actual_ttx = generate_ttx_dump(actual_path, ['head', 'CFF '])
    expected_ttx = get_expected_path(ttx_filename)
    assert differ([expected_ttx, actual_ttx,
                   '-s',
                   '<ttFont sfntVersion' + SPLIT_MARKER +
                   '    <checkSumAdjustment value=' + SPLIT_MARKER +
                   '    <checkSumAdjustment value=' + SPLIT_MARKER +
                   '    <created value=' + SPLIT_MARKER +
                   '    <modified value='])


@pytest.mark.parametrize('feat_filename', [
    'bug164/d1/d2/rel_to_main.fea',
    'bug164/d1/d2/rel_to_parent.fea',
])
def test_feature_includes_type1_bug164(feat_filename):
    input_filename = "bug164/d1/d2/font.pfa"
    otf_path = get_temp_file_path()

    runner(CMD + ['-o',
                  'f', '_{}'.format(get_input_path(input_filename)),
                  'ff', '_{}'.format(get_input_path(feat_filename)),
                  'o', '_{}'.format(otf_path)])

    assert font_has_table(otf_path, 'head')


def test_feature_includes_ufo_bug164():
    input_filename = "bug164/d1/d2/font.ufo"
    otf_path = get_temp_file_path()

    runner(CMD + ['-o',
                  'f', '_{}'.format(get_input_path(input_filename)),
                  'o', '_{}'.format(otf_path)])

    assert font_has_table(otf_path, 'head')
