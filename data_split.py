import json
import argparse

# def dep_func(**kwargs):
#     perc, tot = percentages(category_counts=ncs)
#     val = sort_by_val(data_map=perc)
#     print_data(data_map=val)
#     print("Total: %d" % (tot))

def read_file(**kwargs):
    data_file = kwargs['data_file']

    with open(data_file) as data_file:
        data = json.load(data_file)

    return data

def images_by_category(**kwargs):
    d, ak, cid, img_id, i_d, img_mk, imgs = kwargs['data'], kwargs['anno_key'],\
                                      kwargs['category_id'], kwargs['image_id'],\
                                      kwargs['i_d'], kwargs['image_map_key'], kwargs['images']

    cat_img = {}
    for e in d[ak]:
        if e[cid] not in cat_img:
            cat_img[e[cid]] = []
        cat_img[e[cid]].append({i_d: e[i_d], img_id: e[img_id], 
                                img_mk: imgs[e[img_id]]})
        
    return cat_img

def sort_by_val(**kwargs):
    m = kwargs['data_map']

    return sorted(list(m.iteritems()), key=lambda x: x[1][1])

def name_categories(**kwargs):
    i_d, nk, cats, im_bc = kwargs['id_key'], kwargs['name_key'], kwargs['category_data'],\
                           kwargs['images_by_category']

    return {cats[k][nk]: im_bc[k] for k in im_bc.keys()}

def print_data(**kwargs):
    d = kwargs['data_map']

    for e in d:
        print("key: %s\t(%d, %f)" % (e[0], e[1][1], e[1][2]))

def category_file_names(**kwargs):
    cs, imgs_bc, fnk, imk = kwargs['categories'], kwargs['images_by_category'], kwargs['file_name_key'],\
                            kwargs['image_map_key']

    return {k: map(lambda e: e[imk][fnk], imgs_bc[k]) for k in cs}

def percentages(**kwargs):
    cs = kwargs['category_counts']

    total = float(sum(map(lambda v: len(v), cs.values())))
    return {k: (cs[k], len(cs[k]), round(len(cs[k]) / total, 5)) for k in cs.keys()}, total

def map_from_coll(**kwargs):
    c, k = kwargs['collection'], kwargs['key']

    return {e[k]: {ek: e[ek] for ek in set(e.keys()).difference({k})} for e in c}

def images_for_file(**kwargs):
    inst_m, cat_key, ak, im_id, i_d, im = kwargs['instance_map'], kwargs['categories'], kwargs['annotations'],\
                                          kwargs['image_id'], kwargs['id'], kwargs['image_map']

    mappings = {}
    for insf, t_dir in inst_m.iteritems():    
        data = read_file(data_file=insf)
        data_maps = {kc[0]: map_from_coll(collection=kc[1], key=i_d) for kc in 
         ((cat_key, data[cat_key]), (images, data[images]), (ak, data[ak]))}

        imgs_bc = images_by_category(data=data, anno_key=ak, category_id=cat_id, 
                                     image_id=im_id, i_d=i_d, image_map_key=im, images=data_maps[images])
        ncs = name_categories(id_key=i_d, name_key=nk, category_data=data_maps[cat_key], 
                        images_by_category=imgs_bc)
        fns = category_file_names(categories=args.category_names, images_by_category=ncs, 
                                  file_name_key=fn, image_map_key=im)
        mappings[t_dir] = fns
    
    return mappings    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Split a dataset')
    parser.add_argument('--instance-files', nargs='+', required=True, help='Annotations files')
    parser.add_argument('--category-names', nargs='+', required=True, help='Categories')
    parser.add_argument('--percentages', required=False, action='store_true')
    parser.add_argument('--directories', nargs='+', required=True, help='Paths of data dirs. Should correspond ' 
                        + 'one-to-one with instance-files')
    args = parser.parse_args()
    if len(args.instance_files) != len(args.directories):
        print('instance-files and directories must have same len as they map one-to-one')
        exit(0)
    instances_dirs = {v: args.directories[i] for i, v in enumerate(args.instance_files)}
    cat_key, ak, cat_id, im_id, i_d, nk, images, im, fn = 'categories', 'annotations', 'category_id',\
                                                  'image_id', 'id', 'name', 'images', 'image_map',\
                                                  'file_name'
    key_args = {cat_key: cat_key, ak: ak, im_id: im_id, i_d: i_d, im: im}
    ms = images_for_file(instance_map=instances_dirs, **key_args)
    for f, fv in ms.iteritems():
        print('file ' + f)
        for k, v in fv.iteritems():
            print((k, len(v), v))
    
