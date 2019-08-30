import json
import argparse
import os.path as path
import shutil
import os
import glob

def read_file(**kwargs):
    data_file = kwargs['data_file']

    with open(data_file) as data_file:
        data = json.load(data_file)

    return data

def images_by_category(**kwargs):
    d, ak, cid, img_id, i_d, imgs = kwargs['data'], kwargs['anno_key'],\
                                      kwargs['category_id'], kwargs['image_id'],\
                                      kwargs['i_d'], kwargs['images']

    cat_img = {}
    for e in d[ak]:
        if e[cid] not in cat_img:
            cat_img[e[cid]] = []
        cat_img[e[cid]].append({i_d: e[i_d], img_id: e[img_id]})
        
    return cat_img

def sort_by_val(**kwargs):
    m = kwargs['data_map']

    return sorted(list(m.iteritems()), key=lambda x: x[1][1])

def name_categories(**kwargs):
    i_d, nk, cats, im_bc = kwargs['id_key'], kwargs['name_key'], kwargs['category_data'],\
                           kwargs['images_by_category']

    return {cats[k][nk]: im_bc[k] for k in im_bc.keys()}

def category_file_names(**kwargs):
    cs, imgs_bc, fnk, im_id, imgs = kwargs['categories'], kwargs['images_by_category'], kwargs['file_name_key'],\
                                    kwargs['image_id'], kwargs['all_images']

    return {k: map(lambda e: imgs[e[im_id]][fnk], imgs_bc[k]) for k in cs}

def percentages(**kwargs):
    cs, ck = kwargs['category_counts'], kwargs['count_key']

    total = float(len(reduce(lambda s1, s2: s1.union(s2), map(lambda l: set(map(lambda m: m[ck], l)), cs.values()))))
    return {k: (cs[k], len(set(map(lambda m: m[ck], cs[k]))), 
                round(len(set(map(lambda m: m[ck], cs[k]))) / total, 5)) for k in cs.keys()}, total

def map_from_coll(**kwargs):
    c, k = kwargs['collection'], kwargs['key']

    return {e[k]: {ek: e[ek] for ek in set(e.keys()).difference({k})} for e in c}

def output_percentages(**kwargs):
    ncs, fn, dm, ims, im_id = kwargs['name_categories'], kwargs['file_name'], kwargs['data_maps'],\
                          'images', kwargs['image_id']

    perc, tot = percentages(category_counts=ncs, count_key=im_id)
    val = sort_by_val(data_map=perc)
    print('File: ' + str(fn))
    for e in val:
        print("key: %s\t(%d, %f)" % (e[0], e[1][1], e[1][2]))
    print("Total (images can have many categories): %d\n" % (tot))

def subset_of_image_keys(data_maps, remove_keys, im_key):
    return reduce(lambda i1, i2 : i1.union(i2), 
                            map(lambda f: set(data_maps[f][0][im_key].keys()), data_maps))\
                            .difference(remove_keys)      

def images_for_file(**kwargs):
    inst_m, cat_key, ak, im_id, i_d, cat_id, images, fn, cn = kwargs['instance_map'], kwargs['categories'],\
                                          kwargs['annotations'],  kwargs['image_id'], kwargs['id'],\
                                          'category_id', 'images', 'file_name', kwargs['category_names']
    mappings = {}
    for insf, ds in inst_m.iteritems():    
        data = read_file(data_file=insf)
        data_maps = {kc[0]: map_from_coll(collection=kc[1], key=i_d) for kc in 
         ((cat_key, data[cat_key]), (images, data[images]), (ak, data[ak]))}
        imgs_bc = images_by_category(data=data, anno_key=ak, category_id=cat_id, 
                                     image_id=im_id, i_d=i_d, images=data_maps[images])
        ncs = name_categories(id_key=i_d, name_key=nk, category_data=data_maps[cat_key], 
                        images_by_category=imgs_bc)
        output_percentages(name_categories=ncs, file_name=path.basename(insf), data_maps=data_maps, image_id=im_id)
        fns = category_file_names(categories=cat_names, images_by_category=ncs, 
                                  file_name_key=fn, image_id=im_id, all_images=data_maps[images])
        mappings[ds] = fns
    
    return mappings        

def write_files(**kwargs):
    ms = kwargs['mappings']

    for ft, cat_files in ms.iteritems():
        print("copying files from %s to %s" % (str(ft[0]), str(ft[1])))
        for c, fs in cat_files.iteritems():
            fns = map(lambda f: (path.join(ft[0], f), path.join(ft[1], f)), fs)
            for f in fns:
                shutil.copyfile(f[0], f[1])
        print("Files in %s: %d" % (ft[1], len(glob.glob(path.join(ft[1], './*')))))

def data_maps(**kwargs):
    inst_m, cat_key, ak, i_d, images = kwargs['instance_map'], kwargs['categories'],\
                                          kwargs['annotations'], kwargs['id'],\
                                          'images'
    maps = {}
    for insf, ds in inst_m.iteritems():    
        data = read_file(data_file=insf)
        data_maps = {kc[0]: map_from_coll(collection=kc[1], key=i_d) for kc in 
         ((cat_key, data[cat_key]), (images, data[images]), (ak, data[ak]))}
        maps[insf] = (data_maps, data)
    
    return maps

def train_val_split(data_maps, remove_keys, im_key, anno_key, cat_id, i_d, im_id, name_key, 
                    cat_key):
    image_keys = subset_of_image_keys(data_maps, remove_keys, im_key)
    images = map(lambda fn: (fn, {ik: data_maps[fn][0][im_key][ik] for ik in image_keys\
                             if ik in data_maps[fn][0][im_key]}), data_maps)
    images_bc = map(lambda i: (i[0], images_by_category(data=data_maps[i[0]][1], 
                                                 anno_key=anno_key, category_id=cat_id, 
                                                 images=i[1], image_id=im_id, i_d=i_d)), images)
    named_bc = map(lambda i: (i[0], name_categories(id_key=i_d, name_key=name_key, 
                             category_data=data_maps[i[0]][0][cat_key], 
                             images_by_category=i[1])), images_bc)
    
    for dat in named_bc:
        output_percentages(name_categories=dat[1], file_name=path.basename(dat[0]), 
                           data_maps=data_maps[dat[0]][0], image_id=im_id)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Split a dataset')
    parser.add_argument('--instance-files', nargs='+', required=True, help='Annotations files')
    parser.add_argument('--category-names', nargs='+', required=False, help='Categories')
    parser.add_argument('--remove-ids', required=False, action='store_true')
    parser.add_argument('--target-dirs', nargs='+', required=True, help='Paths of target dirs. Should correspond ' 
                        + 'one-to-one with instance-files')
    parser.add_argument('--current-dirs', required=True, nargs='+', help='Paths of current dirs. Should correspond ' 
                        + 'one-to-one with instance-files')
    args = parser.parse_args()
    d_len = set(map(lambda d: len(d), (args.current_dirs, args.target_dirs, args.instance_files)))
    if len(d_len) != 1:
        print('instance-files, target-dirs, and current-dirs must have same len as they map one-to-one-to-one')
        exit(0)
    for d in args.target_dirs:
        if not path.exists(d):
            os.makedirs(d)
    instances_dirs = {v: (args.current_dirs[i], args.target_dirs[i]) for i, v in enumerate(args.instance_files)}
    cat_key, ak, im_id, i_d, nk = 'categories', 'annotations', 'image_id', 'id', 'name'
    key_args = {cat_key: cat_key, ak: ak, im_id: im_id, i_d: i_d}

    data = data_maps(instance_map=instances_dirs, **key_args)
    train_val_split(data_maps=data, remove_keys={}, im_key='images', anno_key=ak, cat_id='category_id', 
                    i_d=i_d, im_id=im_id, cat_key=cat_key, name_key=nk)
    #ms = images_for_file(instance_map=instances_dirs, category_names=args.category_names, **key_args)
    #write_files(mappings=ms)
    
