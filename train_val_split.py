import argparse
import json

def read_file(path):
    with open(path, 'r') as df:
        data = df.read()
    return data

def read_json_file(path):
    with open(path) as jf:
        data = json.load(jf)

    return data

def map_from_coll(coll, key):
    return {e[key]: {ek: e[ek] for ek in set(e.keys()).difference({key})} for e in coll}

def data_maps(inst_map, cat_key, anno_key, i_d, map_func, read_func):
    images = 'images'
    maps = {}
    for insf, ds in inst_map.iteritems():    
        data = read_func(path=insf)
        data_maps = {kc[0]: map_func(coll=kc[1], key=i_d) for kc in 
         ((cat_key, data[cat_key]), (images, data[images]), (anno_key, data[anno_key]))}
        maps[insf] = (data_maps, data)
    
    return maps

def validate_args(pr):
    args = pr.parse_args()
    d_len = set(map(lambda d: len(d), (args.image_dirs, args.target_dirs, args.instance_files)))
    if len(d_len) != 1:
        print('instance-files, target-dirs, and current-dirs must have same len as they map one-to-one-to-one')
        exit(0)
    else:
        return args, {v: (args.image_dirs[i], args.target_dirs[i]) for i, v in enumerate(args.instance_files)}

def subset_of_image_keys(data_maps, remove_keys, im_key):
    total = reduce(lambda i1, i2 : i1.union(i2), 
                            map(lambda f: set(data_maps[f][0][im_key]), data_maps))
    return total, total.difference(remove_keys)

def remove_ids(path, read_func):
    return set(map(lambda i: int(i), 
                   filter(lambda n: n, read_func(path=path).split('\n'))))

def annotations_by_cat(annos, cat_id_key, img_id, i_d, inc_im_ids):
    result = {}
    for e in annos:
        if e[img_id] in inc_im_ids:
            if e[cat_id_key] not in result:
                result[e[cat_id_key]] = []
            result[e[cat_id_key]].append({i_d: e[i_d], img_id: e[img_id]})

    return result

def image_ids_histo(annos, img_id, inc_im_ids):
    result = {}
    for a in annos:
        if a[img_id] in inc_im_ids:
            if a[img_id] not in result:
                result[a[img_id]] = []
            result[a[img_id]].append({k: a[k] for k in a.keys() if k != img_id})
            
    return result            

def split_by_category(data_maps, remove_keys, images, anno_key, cat_id, i_d, 
                    image_id, cat_key, subset_func):
    total, all_minus_rem = subset_func(data_maps=data_maps, remove_keys=remove_keys, im_key=images)
    print('Diff:' + str(len(total) - len(all_minus_rem)))

    all_annos = reduce(lambda l1, l2: l1 + l2, map(lambda f: data_maps[f][1][anno_key], data_maps))
    im_histo = image_ids_histo(annos=all_annos, img_id=image_id, inc_im_ids=all_minus_rem)

    img_num_anns = map(lambda i: (i, len(im_histo[i])), im_histo)
    len_anns_groups = {}
    for i, na in img_num_anns:
        if na not in len_anns_groups:
            len_anns_groups[na] = []
        len_anns_groups[na].append(i)

    print(len(len_anns_groups))
    for l, ims in len_anns_groups.iteritems():
        print("Num annos: %d, Num images: %d" % (l, len(ims)))
        if l == 93:
            print('93 annotation image: ' + str(ims))
    return {}

CAT_KEY, ANNOTATIONS, IMAGE_ID, I_D, CAT_ID_KEY, IMAGES = 'categories', 'annotations', 'image_id', 'id', 'category_id',\
                                                     'images'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Split a dataset')
    parser.add_argument('--instance-files', nargs='+', required=True, help='Annotations files')
    parser.add_argument('--remove-ids-path', required=True)
    parser.add_argument('--target-dirs', nargs='+', required=True, help='Paths of target dirs. Should correspond ' 
                        + 'one-to-one with instance-files')
    parser.add_argument('--image-dirs', required=True, nargs='+', help='Paths of dirs with images. Should correspond ' 
                        + 'one-to-one with instance-files')

    args, inst_dirs = validate_args(pr=parser)
    ms = data_maps(inst_map=inst_dirs, cat_key=CAT_KEY, anno_key=ANNOTATIONS, i_d=I_D, 
                   map_func=map_from_coll, read_func=read_json_file)
    rids = remove_ids(path=args.remove_ids_path, read_func=read_file)
    sbc = split_by_category(data_maps=ms, remove_keys=rids, image_id=IMAGE_ID, anno_key=ANNOTATIONS, 
                    cat_id=CAT_ID_KEY, i_d=I_D, images=IMAGES, cat_key=CAT_KEY, subset_func=subset_of_image_keys)
    
    
