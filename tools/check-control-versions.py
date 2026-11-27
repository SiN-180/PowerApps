"""Check Power Apps control versions against reference/control-versions.md.

Usage:
  python tools/check-control-versions.py --vault <app-slug>       read the Screen YAML Vault (needs UPLOAD_PASSWORD in
                                                                  ~/.config/cloudflare/pages.env; the password is never printed)
  python tools/check-control-versions.py file1.yaml [file2.yaml]  read screen YAML files

Exit code 0 = everything current, 1 = something superseded or unknown.
"""
import os, re, sys, json, collections, urllib.request, urllib.parse, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
REG = os.path.join(HERE, '..', 'reference', 'control-versions.md')


def block(name, text):
    m = re.search(r'```' + name + r'\n(.*?)```', text, re.S)
    return [l.strip() for l in m.group(1).splitlines() if l.strip()] if m else []


reg = open(REG, encoding='utf-8').read()
current = set(block('current-versions', reg))
unverified = set(block('unverified-versions', reg))
superseded = dict(l.split(' -> ') for l in block('superseded-versions', reg))


def vault_texts(slug):
    env = os.path.expanduser('~/.config/cloudflare/pages.env')
    pw = ''
    for line in open(env, encoding='utf-8'):
        line = line.strip()
        if line.startswith('export '):
            line = line[len('export '):]
        if line.startswith('UPLOAD_PASSWORD='):
            pw = line.split('=', 1)[1].strip().strip('"\'')
    url = 'https://powerapps.pages.dev/api/screen-yaml?app=%s&password=%s' % (slug, urllib.parse.quote(pw))
    req = urllib.request.Request(url, headers={'User-Agent': 'control-version-check/1.0'})
    try:
        data = json.load(urllib.request.urlopen(req, timeout=60))
    except urllib.error.HTTPError as e:
        sys.exit('Vault request failed with HTTP %s (the URL is not shown because it contains the password).' % e.code)
    for name, sec in data['sections'].items():
        yield '%s (vault, saved %s)' % (name, sec.get('updated', '?')), sec.get('content', '')


def main(argv):
    sources = []
    if argv[:1] == ['--vault']:
        sources = list(vault_texts(argv[1]))
    else:
        for f in argv:
            sources.append((f, open(f, encoding='utf-8').read()))
    if not sources:
        print(__doc__)
        return 2
    bad = 0
    total = collections.Counter()
    for label, text in sources:
        seen = collections.Counter(re.findall(r'Control: (\S+)', text))
        total.update(seen)
        issues = []
        for c, n in sorted(seen.items()):
            if c in current:
                continue
            bad += 1
            if c in superseded:
                issues.append('  SUPERSEDED %s (x%d) -> now %s' % (c, n, superseded[c]))
            elif c in unverified:
                issues.append('  UNVERIFIED %s (x%d): in the old allowlist, never seen in a Studio export. Update the registry.' % (c, n))
            else:
                issues.append('  UNKNOWN    %s (x%d): not in the registry. Add it, with the date, if Studio produced it.' % (c, n))
        print('%s: %d controls, %s' % (label, sum(seen.values()), 'all current' if not issues else 'needs attention'))
        for i in issues:
            print(i)
    print('\nDistinct versions seen: %d. Registry: %s' % (len(total), os.path.normpath(REG)))
    return 1 if bad else 0


sys.exit(main(sys.argv[1:]))
