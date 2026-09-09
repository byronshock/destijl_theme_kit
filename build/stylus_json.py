"""Generate the Stylus import file from the user style (elevated/destijl.user.css -> elevated/destijl.stylus.json).

Stylus reads its own JSON export cleanly and balks at *.user.css files, so the kit ships both: the user.css
is the source, the JSON is what a person imports (Stylus > Manage > Import). The JSON's code is the body of
the @-moz-document block with a one-line header naming the version, and its urlPrefixes are the block's
url-prefix() arguments. Run after editing the sheet:  python3 build/stylus_json.py
"""
import json, os, re, sys, time

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
SRC = os.path.join(ROOT, 'elevated', 'destijl.user.css'); OUT = os.path.join(ROOT, 'elevated', 'destijl.stylus.json')


def build(src=SRC):
    s = open(src, encoding='utf-8').read()
    name = re.search(r'@name\s+(.+)', s).group(1).strip()
    version = re.search(r'@version\s+(\S+)', s).group(1)
    m = re.search(r'@-moz-document\s+([^{]*)\{\n(.*)\n\}\s*$', s, re.S)
    prefixes = re.findall(r'url-prefix\("([^"]+)"\)', m.group(1))
    header = f'/* {name} {version} — DESTIJL_STYLE.md §1, §1b, §2, §3, §7. github.com/byronshock/destijl_theme_kit */'
    code = header + '\n' + m.group(2).strip()
    return [{
        'enabled': True, 'name': name,
        'sections': [{'code': code, 'urlPrefixes': prefixes}],
        'updateUrl': None, 'md5Url': None, 'url': None, 'originalMd5': None,
        'installDate': int(time.time() * 1000),
    }]


if __name__ == '__main__':
    data = build()
    if '--check' in sys.argv:            # compare with a Stylus export, ignoring installDate
        other = json.load(open(sys.argv[sys.argv.index('--check') + 1]))
        a = {**data[0], 'installDate': 0}; b = {**other[0], 'installDate': 0}
        print('matches export:', a == b)
        if a != b:
            for k in a:
                if a[k] != b[k]: print('  differs:', k)
            if a['sections'][0]['code'] != b['sections'][0]['code']:
                import difflib
                print('\n'.join(list(difflib.unified_diff(b['sections'][0]['code'].splitlines(), a['sections'][0]['code'].splitlines(), 'export', 'generated', lineterm='', n=0))[:20]))
        sys.exit(0 if a == b else 1)
    json.dump(data, open(OUT, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(OUT, 'a').write('\n')
    print(OUT, data[0]['name'], re.search(r'@version\s+(\S+)', open(SRC).read()).group(1))
