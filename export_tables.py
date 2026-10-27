"""Export all 15 frozen book tables to UTF-8 CSV. No source input is changed."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path)
    args=parser.parse_args(argv)
    root=Path(__file__).resolve().parent
    source=json.loads((root/'tables.json').read_text(encoding='utf-8'))
    dest=args.output_dir or root/'tables'
    dest.mkdir(parents=True,exist_ok=True)
    index=[]
    for n,rows in enumerate(source['tables'],1):
        target=dest/f'table_{n:02d}.csv'
        with target.open('w',encoding='utf-8',newline='') as f:
            csv.writer(f).writerows(rows)
        with target.open(encoding='utf-8',newline='') as f:
            assert list(csv.reader(f)) == rows
        index.append({'table':n,'file':target.name,'data_rows':len(rows)-1,'columns':len(rows[0]),'cells_preserved_as_printed_strings':True})
    assert len(index)==15
    (dest/'index.json').write_text(json.dumps({'source':'tables.json','source_table_file_sha256':hashlib.sha256((root/'tables.json').read_bytes()).hexdigest(),'baseline_date':source.get('baseline_date','2026-10-27'),'tables':index,'scope':'Frozen display/table strings; original numeric units and assumption status are explained in DATA_DICTIONARY.md and FIGURES.md. CSV export does not make assumed inputs empirical observations.'},indent=2),encoding='utf-8')
    print(f'Exported and round-trip checked {len(index)} tables to {dest}')

if __name__=='__main__':main()
