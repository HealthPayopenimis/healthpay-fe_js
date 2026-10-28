#!/usr/bin/env python3
"""Compare generated assembly lock with verified prior candidate; no network."""
from pathlib import Path
import copy, json, sys
baseline=json.loads(Path(sys.argv[1]).read_text())
current=json.loads(Path(sys.argv[2]).read_text())
config=json.loads(Path('openimis.json').read_text())
def walk(value):
    if isinstance(value,dict):
        for key,item in value.items():
            if isinstance(item,str) and 'healthpay-fe-claim_js#' in item:
                yield item.split('#')[-1]
            yield from walk(item)
    elif isinstance(value,list):
        for item in value:yield from walk(item)
sha=list(walk(config))
assert len(set(sha))==1 and len(sha[0])==40,'EXACT_CLAIM_PIN_REQUIRED'
sha=sha[0]
a=copy.deepcopy(baseline);b=copy.deepcopy(current)
old=a['packages']['']['dependencies']['@openimis/fe-claim'].split('#')[-1]
assert b['packages']['']['dependencies']['@openimis/fe-claim'].split('#')[-1]==sha
assert b['packages']['node_modules/@openimis/fe-claim']['resolved'].split('#')[-1]==sha
# Normalize only claim commit references. Every other field/package remains fixed.
def normalize(value):
    if isinstance(value,str):return value.replace(old,'<CLAIM_SOURCE>').replace(sha,'<CLAIM_SOURCE>')
    if isinstance(value,dict):return {key:normalize(item) for key,item in value.items()}
    if isinstance(value,list):return [normalize(item) for item in value]
    return value
aa=normalize(a);bb=normalize(b)
if aa!=bb:
    differences=[]
    for key in sorted(set(aa['packages'])|set(bb['packages'])):
        left=aa['packages'].get(key);right=bb['packages'].get(key)
        if left!=right:
            fields=sorted(set(left or {})|set(right or {}))
            differences.append({'package':key,'before':left,'after':right,'changedFields':[field for field in fields if (left or {}).get(field)!=(right or {}).get(field)]})
    print('DEPENDENCY_DELTA_DIAGNOSTIC',json.dumps(differences,sort_keys=True))
assert aa==bb,'UNRELATED_DEPENDENCY_LOCK_DRIFT'
print('DEPENDENCY_DELTA_PASS: only exact reviewed claim module source changed; all other packages fixed')
