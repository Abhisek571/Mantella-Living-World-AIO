"""Builds the Mantella Living World All in One archive: every Living World mod in one FOMOD installer.

Takes the newest release archives that already exist (the Integration Hub's dist folder for the Living World modules,
Direct AI Connect's release folder for the patched Mantella.exe), lays each one out as its own FOMOD option and packs
one .7z into dist/. Nothing is rebuilt from source here: the AIO carries exactly the files of the separate releases.

usage: py -3 tools/build_aio.py [--version 1.0.0] [--keep]
"""
import argparse, glob, os, re, shutil, subprocess, sys
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODING = os.path.dirname(HERE)
HUB_DIST = os.path.join(CODING, 'Mantella-Living-World-Hub', 'dist')
DAC_RELEASE = os.path.join(CODING, 'Mantella-Direct-AI-Connect', 'release')
SEVEN_ZIP = r'C:\Program Files\7-Zip\7z.exe'
STAGE = os.path.join(HERE, 'build', 'stage')
OUT = os.path.join(HERE, 'dist')
CHARTS = r'E:\CODING\LW-pages\charts'  # module maps (map-<key>.png), shown beside each option

# key, folder in the archive, archive name prefix, option name, description, plugin that makes it Recommended
MODULES = [
    ('hub', '00 Integration Hub', 'Mantella Living World - Integration Hub', 'Integration Hub',
     'The base every module needs: the Living World tab in Mantella\'s settings page, memory, action gates and the debug menu. Always installed.', None),
    ('dac', '01 Direct AI Connect', 'Mantella - Direct AI Connect', 'Mantella - Direct AI Connect',
     'The patched Mantella.exe that Living World runs inside. Needed for everything in Living World. Untick it only if you already have Direct AI Connect installed as its own mod. After installing, run Setup Backend.cmd in this mod\'s folder once (needs Python 3.11 once).', None),
    ('relationships', '10 Relationships', 'Mantella Living World - Relationships', 'Relationships',
     'Marriage, affection, family ties and shared history, from M.A.R.A.S, Relations Finder and Lover\'s Ledger when they are installed.', None),
    ('world', '11 World', 'Mantella Living World - World', 'World',
     'What NPCs know about you: fame, bounty, Thane titles, quest outcomes, what you did to them, recognition, settling a bounty with a guard, party banter.', None),
    ('knowledge', '12 Knowledge', 'Mantella Living World - Knowledge', 'Knowledge',
     'Each NPC knows what fits their life: home, hold, job, quest secrets, lore lookups and map marks.', None),
    ('survival', '13 Survival', 'Mantella Living World - Survival', 'Survival',
     'NPCs notice hunger, cold, rest, food, beds, wounds and vampirism. Hunger needs Survival Mode; cold and tiredness need Survival Mode Improved.', None),
    ('followers', '14 Followers', 'Mantella Living World - Followers', 'Followers',
     'Party orders by talking. Needs Nether\'s Follower Framework.', 'nwsFollowerFramework.esp'),
    ('missives', '15 Missives', 'Mantella Living World - Missives', 'Missives',
     'Job posters who know their own jobs. Needs Missives.', 'Missives.esp'),
    ('arousal', '16 Arousal', 'Mantella Living World - Arousal', 'Arousal (adult)',
     'Arousal, appetite and temperament from OSL Aroused. Needs OSL Aroused and powerofthree\'s Papyrus Extender.', 'OSLAroused.esp'),
    ('ostim', '17 OStim Expansion', 'Mantella Living World - OStim Expansion', 'OStim Expansion (adult)',
     'OStim scenes and affection (dances, kisses, hugs) run by conversation. Needs OStim Standalone, OSL Aroused and Actions For Mantella - Expanded Sex Actions. After installing, run Build Flows.cmd once (see the readme).', 'OStim.esp'),
]
ALWAYS_ON = {'hub'}
DEFAULT_ON = {'dac', 'relationships', 'world', 'knowledge', 'survival'}
# Direct AI Connect's own docs move under Docs so they do not sit loose in the mod folder next to the Living World ones
DAC_DOCS = ('README.md', 'LICENSE', 'CHANGELOG.md', 'SOURCE-AND-LICENSES.txt', 'Licenses')  # INSTALL.txt stays: Setup Backend.cmd points to it
DAC_DROP = ('meta.ini',)  # MO2 writes its own meta.ini for the installed mod


def version_key(path):
    m = re.search(r'(\d+)\.(\d+)(?:\.(\d+))?\.(?:7z|zip)$', path)
    return tuple(int(x or 0) for x in m.groups()) if m else (0, 0, 0)


def newest(folder, prefix, ext):
    found = [p for p in glob.glob(os.path.join(folder, f'{prefix} *.{ext}')) if re.search(r' \d+\.\d+(\.\d+)?\.' + ext + '$', p)]
    if not found:
        raise SystemExit(f'No release archive for {prefix} in {folder}')
    return max(found, key=version_key)


def unpack(archive, dest):
    os.makedirs(dest, exist_ok=True)
    subprocess.run([SEVEN_ZIP, 'x', '-y', f'-o{dest}', archive], check=True, stdout=subprocess.DEVNULL)


def stage_dac(dest):
    docs = os.path.join(dest, 'Docs', 'Mantella - Direct AI Connect')
    os.makedirs(docs, exist_ok=True)
    for name in DAC_DOCS:
        p = os.path.join(dest, name)
        if os.path.exists(p):
            shutil.move(p, os.path.join(docs, name))
    for name in DAC_DROP:
        p = os.path.join(dest, name)
        if os.path.isfile(p):
            os.remove(p)


def check_no_overlap(stage):
    seen = {}
    for key, folder, *_ in MODULES:
        root = os.path.join(stage, folder)
        for dirpath, _, files in os.walk(root):
            for f in files:
                rel = os.path.relpath(os.path.join(dirpath, f), root).lower()
                if rel in seen:
                    raise SystemExit(f'{rel} is in both {seen[rel]} and {folder}')
                seen[rel] = folder
    return len(seen)


def option_xml(key, folder, name, desc, plugin, images):
    img = f'\n\t\t\t\t\t\t<image path="fomod\\images\\{key}.png"/>' if key in images else ''
    if key in ALWAYS_ON:
        type_xml = '<type name="Required"/>'
    elif plugin:
        type_xml = ('<dependencyType><defaultType name="Optional"/><patterns><pattern><dependencies operator="And">'
                    f'<fileDependency file="{escape(plugin)}" state="Active"/></dependencies><type name="Recommended"/>'
                    '</pattern></patterns></dependencyType>')
    else:
        type_xml = f'<type name="{"Recommended" if key in DEFAULT_ON else "Optional"}"/>'
    return f'''
					<plugin name="{escape(name)}">
						<description>{escape(desc)}</description>{img}
						<files><folder source="{escape(folder)}" destination="" priority="0"/></files>
						<typeDescriptor>{type_xml}</typeDescriptor>
					</plugin>'''


def module_config(images, readme_folder):
    core = [m for m in MODULES if m[0] in ('hub', 'dac')]
    mods = [m for m in MODULES if m[0] not in ('hub', 'dac')]
    opts = lambda group: ''.join(option_xml(k, f, n, d, p, images) for k, f, _, n, d, p in group)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://qconsulting.ca/fo3/ModConfig5.0.xsd">
	<moduleName>Mantella Living World - All in One</moduleName>
	<requiredInstallFiles>
		<folder source="{escape(readme_folder)}" destination=""/>
	</requiredInstallFiles>
	<installSteps order="Explicit">
		<installStep name="Base">
			<optionalFileGroups order="Explicit">
				<group name="Base" type="SelectAny">
					<plugins order="Explicit">{opts(core)}
					</plugins>
				</group>
			</optionalFileGroups>
		</installStep>
		<installStep name="Modules">
			<optionalFileGroups order="Explicit">
				<group name="Modules (each one works on its own)" type="SelectAny">
					<plugins order="Explicit">{opts(mods)}
					</plugins>
				</group>
			</optionalFileGroups>
		</installStep>
	</installSteps>
</config>
'''


def info_xml(version):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<fomod>
	<Name>Mantella Living World - All in One</Name>
	<Author>itsPigeon2000</Author>
	<Version>{version}</Version>
	<Description>Every Mantella Living World mod in one installer: the Integration Hub, Direct AI Connect and all modules. Pick the modules you want.</Description>
	<Groups>
		<element>Immersion</element>
	</Groups>
</fomod>
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--version', default='1.0.0')
    ap.add_argument('--keep', action='store_true', help='keep the staging folder')
    args = ap.parse_args()

    shutil.rmtree(STAGE, ignore_errors=True)
    os.makedirs(STAGE)
    used = []
    for key, folder, prefix, *_ in MODULES:
        archive = newest(DAC_RELEASE, prefix, 'zip') if key == 'dac' else newest(HUB_DIST, prefix, '7z')
        dest = os.path.join(STAGE, folder)
        unpack(archive, dest)
        if key == 'dac':
            stage_dac(dest)
        used.append((folder, os.path.basename(archive)))
    files = check_no_overlap(STAGE)

    readme_folder = 'Docs AIO'
    docs = os.path.join(STAGE, readme_folder, 'Docs', 'Mantella Living World - All in One')
    os.makedirs(docs)
    readme = open(os.path.join(HERE, 'tools', 'readme_template.md'), encoding='utf-8').read()
    included = '\n'.join('- ' + re.sub(r'\.(7z|zip)$', '', name) for _, name in used)
    readme = readme.replace('{INCLUDED}', included).replace('{VERSION}', args.version)
    open(os.path.join(docs, 'Readme.txt'), 'w', encoding='utf-8', newline='\r\n').write(readme)

    fomod = os.path.join(STAGE, 'fomod')
    os.makedirs(os.path.join(fomod, 'images'))
    images = set()
    for key, *_ in MODULES:
        src = os.path.join(CHARTS, f'map-{key}.png')
        if os.path.isfile(src):
            subprocess.run(['magick', src, '-resize', '1280x>', os.path.join(fomod, 'images', f'{key}.png')], check=True)
            images.add(key)
    open(os.path.join(fomod, 'info.xml'), 'w', encoding='utf-8').write(info_xml(args.version))
    open(os.path.join(fomod, 'ModuleConfig.xml'), 'w', encoding='utf-8').write(module_config(images, readme_folder))

    os.makedirs(OUT, exist_ok=True)
    out = os.path.join(OUT, f'Mantella Living World - All in One {args.version}.7z')
    if os.path.exists(out):
        os.remove(out)
    subprocess.run([SEVEN_ZIP, 'a', '-t7z', '-mx=9', out, os.path.join(STAGE, '*')], check=True, stdout=subprocess.DEVNULL)
    for folder, name in used:
        print(f'{folder:22} <- {name}')
    print(f'{files} files, no overlaps -> {out} ({os.path.getsize(out) // 1024} KB)')
    if not args.keep:
        shutil.rmtree(STAGE, ignore_errors=True)


if __name__ == '__main__':
    main()
