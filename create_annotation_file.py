import argparse
import json
import os.path as path

def read_file(**kwargs):
    fn = kwargs['file_name']

    with open(fn) as df:
        data = json.load(df)

    return data

def write_file(**kwargs):
    fp, d = kwargs['file_path'], kwargs['data']

    with open(fp, 'w') as fh:
        json.dump(d, fh)

def map_from_coll(**kwargs):
    c, k = kwargs['collection'], kwargs['key']

    return {e[k]: {ek: e[ek] for ek in set(e.keys()).difference({k})} for e in c}

def compute_output(**kwargs):
    rp, cn = kwargs['read_path'], kwargs['category_names']
    cs, nk, i_d, ak, im_key, cat_id, im_id, inf, lic = 'categories', 'name', 'id', 'annotations', 'images',\
                                      'category_id', 'image_id', 'info', 'licenses'

    data = read_file(file_name=rp)
    cats_name = map_from_coll(collection=data[cs], key=nk)
    cats_id = map_from_coll(collection=data[cs], key=i_d)
    cat_entries = {i: cats_id[i] for i in map(lambda n: cats_name[n][i_d], cn)}    
    annos = filter(lambda a: a[cat_id] in cat_entries, data[ak])
    img_ids = set(map(lambda i: i[im_id], annos))
    imgs = filter(lambda i: i[i_d] in img_ids, data[im_key])

    return {inf: data[inf], lic: data[lic], ak: annos, im_key: imgs, cs: data[cs]}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Write out an annotation file')
    parser.add_argument('--read-path', required=True)
    parser.add_argument('--write-path', required=True)
    parser.add_argument('--category-names', nargs='+', required=True, help='Categories')
    args = parser.parse_args()

    output = compute_output(read_path=args.read_path, write_path=args.write_path,
                            category_names=args.category_names)
    write_file(file_path=args.write_path, data=output)

    
