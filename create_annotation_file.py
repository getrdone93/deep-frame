import argparse
import json
import os.path as path
import copy

def read_file(**kwargs):
    fn = kwargs['file_name']

    with open(fn) as df:
        data = json.load(df)

    return data

def write_file(**kwargs):
    fp, d = kwargs['file_path'], kwargs['data']

    with open(fp, 'w') as fh:
        json.dump(d, fh)

def write_text_file(**kwargs):
    fp, d = kwargs['file_path'], kwargs['data']

    with open(fp, 'w') as fh:
        fh.write(d)

def map_from_coll(**kwargs):
    c, k = kwargs['collection'], kwargs['key']

    return {e[k]: {ek: e[ek] for ek in set(e.keys()).difference({k})} for e in c}

def cat_pbtxt(**kwargs):
    c, nk, idk = kwargs['cat_entry'], 'name', 'id'

    dn = "\n" + '  display_name: "{}"'.format(c[nk])
    i_d = "\n" + '  id: {}'.format(c[idk])
    return 'item {' + i_d + dn + "\n}\n"

def pbtxt_out(**kwargs):
    cs, cnv_func = kwargs['categories'], kwargs['conversion_func']

    return reduce(lambda s1, s2: s1 + s2, map(lambda c: cnv_func(cat_entry=c), cs))

def compute_output(**kwargs):
    rp, cn = kwargs['read_path'], kwargs['category_names']
    cs, nk, i_d, ak, im_key, cat_id, im_id, inf, lic, pb = 'categories', 'name', 'id', 'annotations', 'images',\
                                      'category_id', 'image_id', 'info', 'licenses', 'pbtxt'

    data = read_file(file_name=rp)
    cats_name = map_from_coll(collection=data[cs], key=nk)
    cats_id = map_from_coll(collection=data[cs], key=i_d)
    cat_entries = {i: cats_id[i] for i in map(lambda n: cats_name[n][i_d], cn)}    
    annos = filter(lambda a: a[cat_id] in cat_entries, data[ak])
    img_ids = set(map(lambda i: i[im_id], annos))
    imgs = filter(lambda i: i[i_d] in img_ids, data[im_key])
    cname_newid = {ic[0]: ic[1] for ic in zip(cn, range(1, len(cn) + 1))}
    for a in annos:
        a.update({cat_id: cname_newid[cat_entries[a[cat_id]][nk]]})
    new_cs = copy.deepcopy(filter(lambda c: c[i_d] in cat_entries, data[cs]))
    for c in new_cs:
        c.update({i_d: cname_newid[cat_entries[c[i_d]][nk]]})
    new_cs = sorted(new_cs, key=lambda e: e[i_d])

    return {inf: data[inf], lic: data[lic], ak: annos, im_key: imgs, 
            cs: new_cs, 
            pb: pbtxt_out(categories=new_cs, conversion_func=cat_pbtxt)}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Write out an annotation file')
    parser.add_argument('--read-path', required=True)
    parser.add_argument('--write-path', required=False)
    parser.add_argument('--pbtxt-write-path', required=False)
    parser.add_argument('--category-names', nargs='+', required=True, help='Categories')
    args = parser.parse_args()
    pbtxt = 'pbtxt'
    output = compute_output(read_path=args.read_path, write_path=args.write_path,
                            category_names=args.category_names)
    if args.write_path:
        write_file(file_path=args.write_path, data={k: output[k] for k in set(output.keys()).difference({pbtxt})})
    if args.pbtxt_write_path:
        write_text_file(file_path=args.pbtxt_write_path, data=output[pbtxt])

    
