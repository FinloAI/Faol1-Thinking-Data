#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Validate the released JSONL, bilingual grouping, metadata and checksums."""
import collections,hashlib,json,pathlib,re,sys
ROOT=pathlib.Path(__file__).resolve().parent
def check(condition,message):
    if not condition:raise ValueError(message)
def canonical(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()
def load_lines(name):
    return [json.loads(line) for line in (ROOT/name).read_text().splitlines() if line.strip()]
def main():
    rows=load_lines('train.jsonl');metadata=load_lines('metadata.jsonl')
    stats=json.loads((ROOT/'STATISTICS.json').read_text())
    check(len(rows)==len(metadata)==stats['rows']==828,'Unexpected row count')
    pairs=collections.defaultdict(set);seen=set();families=collections.Counter()
    for i,(row,meta) in enumerate(zip(rows,metadata),1):
        check(set(row)=={'messages'},f'Row {i}: unexpected training fields')
        messages=row['messages']
        check([m.get('role') for m in messages]==['system','user','assistant'],f'Row {i}: role order')
        check(all(set(m)=={'role','content'} and isinstance(m['content'],str) and m['content'].strip() for m in messages),f'Row {i}: empty/extra message data')
        content=messages[-1]['content']
        check(bool(re.match(r'^\s*<think>\s*\S',content)) and content.count('<think>')==content.count('</think>')==1,f'Row {i}: think structure')
        check(bool(content.split('</think>',1)[1].strip()),f'Row {i}: empty public answer')
        check(bool(re.search(r'\*\*1\.|\*\*1\b',content)),f'Row {i}: numbered stage missing')
        fingerprint=digest(canonical(row))
        check(fingerprint==meta['record_sha256'],f'Row {i}: record fingerprint mismatch')
        check(fingerprint not in seen,f'Row {i}: duplicate');seen.add(fingerprint)
        check(digest(messages[1]['content'])==meta['question_sha256'],f'Row {i}: question fingerprint')
        check(digest(content)==meta['assistant_sha256'],f'Row {i}: assistant fingerprint')
        check(meta['split']=='train' and meta['pair_id'].startswith('train-'),f'Row {i}: non-training source')
        check(meta['language'] in ['en','fi'],f'Row {i}: language')
        check(meta['source']['license']=='CC-BY-SA-4.0',f'Row {i}: missing license')
        check('/Users/' not in canonical(row) and '/Users/' not in canonical(meta),f'Row {i}: private local path')
        if meta['source']['kind']=='adapted_public_dataset_question':
            check(meta['source']['dataset']=='allenai/ai2_arc' and meta['source']['original_split']=='train',f'Row {i}: upstream split')
        pairs[meta['pair_id']].add(meta['language']);families[meta['family']]+=1
    check(len(pairs)==stats['language_pairs']==414,'Unexpected pair count')
    check(all(langs=={'en','fi'} for langs in pairs.values()),'Incomplete language pair')
    check(dict(families)==stats['families'],'Family counts differ')
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        expected,name=line.split('  ',1);path=ROOT/name
        check(path.is_file() and not path.is_symlink(),f'Missing/unsafe package file: {name}')
        check(hashlib.sha256(path.read_bytes()).hexdigest()==expected,f'Checksum mismatch: {name}')
    print(json.dumps({'valid':True,'rows':len(rows),'language_pairs':len(pairs),'languages':stats['languages'],'split':'train','sha256s_verified':True},ensure_ascii=False))
if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,TypeError,json.JSONDecodeError) as exc:
        print(f'Validation failed: {exc}',file=sys.stderr);sys.exit(1)

