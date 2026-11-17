"""Offline test of build_aio.py's source checks: a release archive that does not match its module's current source is
found (stale file, file gone, script added), built and generated files are not compared, line endings do not count,
and an out-of-date source mirror is reported.

usage: py -3 tools/test_build_aio.py
"""
import os, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_aio as B

FAILS = []


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + ('' if ok else f'  -> {detail}'))
    if not ok:
        FAILS.append(name)


def put(root, rel, data):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(data)


with tempfile.TemporaryDirectory() as tmp:
    repo, staged = os.path.join(tmp, 'repo'), os.path.join(tmp, 'staged')
    put(repo, 'Source/Scripts/A.psc', b'Scriptname A\nint x\n')
    put(repo, 'Source/Scripts/B.psc', b'Scriptname B\n')
    put(repo, 'server/lw_knowledge/hookup.py', b'print(1)\n')
    put(repo, 'data/profiles.json', b'{}')
    put(repo, 'SKSE/Plugins/MantellaSoftware/data/prompt_rules/20.txt', b'rule')
    put(repo, 'plugin/build/release/X.dll', b'MZ new')
    put(staged, 'Scripts/Source/A.psc', b'Scriptname A\r\nint x\r\n')        # same text, CRLF
    put(staged, 'Scripts/A.pex', b'compiled')                                   # built: not compared
    put(staged, 'Mantella Living World - Knowledge.esp', b'TES4')              # built: not compared
    put(staged, 'SKSE/Plugins/MantellaSoftware/extensions/lw_knowledge/hookup.py', b'print(0)\n')  # stale
    put(staged, 'SKSE/Plugins/MantellaSoftware/extensions/lw_knowledge/data/profiles.json', b'{}')
    put(staged, 'SKSE/Plugins/MantellaSoftware/data/prompt_rules/20.txt', b'rule')
    put(staged, 'SKSE/Plugins/MantellaSoftware/data/prompt_rules/99_old.txt', b'gone')            # removed from source
    put(staged, 'SKSE/Plugins/MantellaSoftware/data/living_world/versions/knowledge.json', b'{"version": "1"}')  # generated
    put(staged, 'SKSE/Plugins/X.dll', b'MZ old')                                                   # an older DLL
    rows = dict(B.stale_files('knowledge', staged, repo))
    check('a changed server file is stale', rows.get('SKSE/Plugins/MantellaSoftware/extensions/lw_knowledge/hookup.py') == 'differs from the source', rows)
    check('a file the source no longer has is stale', rows.get('SKSE/Plugins/MantellaSoftware/data/prompt_rules/99_old.txt') == 'not in the source any more', rows)
    check('a script the archive lacks is stale', rows.get('Source/Scripts/B.psc') == 'in the source, not in the archive', rows)
    check('an older DLL is stale', rows.get('SKSE/Plugins/X.dll') == 'differs from the source', rows)
    check('line endings, .pex, .esp, the version file and matching data are not reported',
          set(rows) == {'SKSE/Plugins/MantellaSoftware/extensions/lw_knowledge/hookup.py',
                        'SKSE/Plugins/MantellaSoftware/data/prompt_rules/99_old.txt', 'Source/Scripts/B.psc', 'SKSE/Plugins/X.dll'}, rows)
    put(staged, 'SKSE/Plugins/MantellaSoftware/extensions/lw_knowledge/hookup.py', b'print(1)\n')
    put(staged, 'Scripts/Source/B.psc', b'Scriptname B\n')
    os.remove(os.path.join(staged, 'SKSE/Plugins/MantellaSoftware/data/prompt_rules/99_old.txt'))
    put(staged, 'SKSE/Plugins/X.dll', b'MZ new')
    put(repo, 'SKSE/Plugins/MantellaSoftware/data/actions/new_action.json', b'{}')  # a data file added after the release
    check('a data file the archive lacks is stale', dict(B.stale_files('knowledge', staged, repo)).get(
        'SKSE/Plugins/MantellaSoftware/data/actions/new_action.json') == 'in the source, not in the archive')
    put(staged, 'SKSE/Plugins/MantellaSoftware/data/actions/new_action.json', b'{}')
    check('a release built from the current source: nothing reported', B.stale_files('knowledge', staged, repo) == [],
          B.stale_files('knowledge', staged, repo))

    mirror = os.path.join(tmp, 'mirror')
    put(mirror, 'Source/Scripts/A.psc', b'Scriptname A\r\nint x\r\n')
    put(mirror, 'Source/Scripts/Old.psc', b'x')
    put(mirror, 'server/lw_knowledge/hookup.py', b'print(0)\n')
    diff = dict(B.mirror_differences(mirror, repo))
    check('an out-of-date mirror is reported (changed and removed files), CRLF is not',
          diff == {'Source/Scripts/Old.psc': 'not in the module repository', 'server/lw_knowledge/hookup.py': 'differs'}, diff)

    dac_repo, dac_staged = os.path.join(tmp, 'dac'), os.path.join(tmp, 'dac_staged')
    put(dac_repo, 'Scripts/Source/MantellaConversation.psc', b'new')
    put(dac_repo, 'setup_backend.py', b'x')
    put(dac_staged, 'Scripts/Source/MantellaConversation.psc', b'old')
    put(dac_staged, 'setup_backend.py', b'x')
    put(dac_staged, 'meta.ini', b'[General]')
    check('Direct AI Connect: the release zip is compared file by file (meta.ini left out)',
          B.stale_files('dac', dac_staged, dac_repo) == [('Scripts/Source/MantellaConversation.psc', 'differs from the source')],
          B.stale_files('dac', dac_staged, dac_repo))

src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build_aio.py'), encoding='utf-8').read()
check('main stops on a stale archive unless --allow-stale', "if stale and not args.allow_stale:" in src and 'raise SystemExit' in src.split('if stale and not args.allow_stale:')[1][:300])

print('RESULT: ' + ('ALL PASS' if not FAILS else f'{len(FAILS)} FAILED'))
sys.exit(1 if FAILS else 0)
