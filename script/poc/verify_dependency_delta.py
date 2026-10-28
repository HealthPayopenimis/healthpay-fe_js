#!/usr/bin/env python3
"""Allow only exact reviewed claim/location git pins; no dependency/version drift."""
from pathlib import Path
import copy,json,re,sys
baseline=json.loads(Path(sys.argv[1]).read_text());current=json.loads(Path(sys.argv[2]).read_text());config=json.loads(Path('openimis.json').read_text())
ALLOWED={'@openimis/fe-claim':'healthpay-fe-claim_js','@openimis/fe-location':'healthpay-fe-location_js'}
def pins(value,repo):
    if isinstance(value,dict):
        for item in value.values():
            if isinstance(item,str) and repo+'#' in item:yield item.split('#')[-1]
            yield from pins(item,repo)
    elif isinstance(value,list):
        for item in value:yield from pins(item,repo)
replacements={}
for package,repo in ALLOWED.items():
    matches=set(pins(config,repo));assert len(matches)==1,'SINGLE_EXACT_PIN_REQUIRED:'+package
    sha=matches.pop();assert re.fullmatch('[a-f0-9]{40}',sha),'EXACT_SHA_REQUIRED:'+package
    old=baseline['packages']['']['dependencies'][package].split('#')[-1]
    assert current['packages']['']['dependencies'][package].split('#')[-1]==sha,'ROOT_PIN_MISMATCH:'+package
    assert current['packages']['node_modules/'+package]['resolved'].split('#')[-1]==sha,'INSTALLED_PIN_MISMATCH:'+package
    replacements[old]='<'+package+'_SOURCE>';replacements[sha]=replacements[old]
def normalize(value):
    if isinstance(value,str):
        for sha,marker in replacements.items():value=value.replace(sha,marker)
        return value
    if isinstance(value,dict):return {k:normalize(v) for k,v in value.items()}
    if isinstance(value,list):return [normalize(v) for v in value]
    return value
a=normalize(baseline);b=normalize(current)
if a!=b:
    differences=[]
    for key in sorted(set(a['packages'])|set(b['packages'])):
        left=a['packages'].get(key);right=b['packages'].get(key)
        if left!=right:differences.append({'package':key,'changedFields':[field for field in sorted(set(left or {})|set(right or {})) if (left or {}).get(field)!=(right or {}).get(field)]})
    print('DEPENDENCY_DELTA_DIAGNOSTIC',json.dumps(differences,sort_keys=True))
assert a==b,'UNRELATED_DEPENDENCY_LOCK_DRIFT'
print('DEPENDENCY_DELTA_PASS: only exact reviewed claim/location source pins may differ; every package version and other field remains fixed')
