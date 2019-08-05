import json
import argparse

def read_file(**kwargs):
    data_file = kwargs['data_file']

    with open(data_file) as data_file:
        data = json.load(data_file)

    return data

def images_by_category(**kwargs):
    d, ak, cid, img_id, i_d, img_mk, imgs = kwargs['data'], kwargs['anno_key'],\
                                      kwargs['category_id'], kwargs['image_id'],\
                                      kwargs['i_d'], kwargs['image_map_key'], kwargs['images_lis']

    cat_img = {}
    for e in d[ak]:
        if e[cid] not in cat_img:
            cat_img[e[cid]] = []
        cat_img[e[cid]].append({i_d: e[i_d], img_id: e[img_id], 
                                img_mk: filter(lambda i: i[i_d] == e[img_id], imgs)[0]})
        
    return cat_img

def sort_by_val(**kwargs):
    m = kwargs['data_map']

    return sorted(list(m.iteritems()), key=lambda x: x[1][1])

def name_categories(**kwargs):
    i_d, nk, cats, im_bc = kwargs['id_key'], kwargs['name_key'], kwargs['category_data'],\
                           kwargs['images_by_category']

    return {filter(lambda c: c[i_d] == k, cats)[0][nk]: im_bc[k] for k in im_bc.keys()}

def print_data(**kwargs):
    d = kwargs['data_map']

    for e in d:
        print("key: %s\t(%d, %f)" % (e[0], e[1][1], e[1][2]))

def category_file_names(**kwargs):
    cs, imgs_bc, fnk, imk = kwargs['categories'], kwargs['images_by_category'], kwargs['file_name_key'],\
                       kwargs['image_map_key']

    return {k: map(lambda e: e[imk][fnk], imgs_bc[k]) for k in cs}
    #return {k: map(lambda e: e, imgs_bc[k]) for k in cs}

def percentages(**kwargs):
    cs = kwargs['category_counts']

    total = float(sum(map(lambda v: len(v), cs.values())))
    return {k: (cs[k], len(cs[k]), round(len(cs[k]) / total, 5)) for k in cs.keys()}, total

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Split a dataset')
    parser.add_argument('--instance-files', nargs='+', required=True, help='Annotations file')
    parser.add_argument('--category-names', nargs='+', required=True, help='Categories')
    parser.add_argument('--percentages', required=False, action='store_true')
    args = parser.parse_args()
    cat_key, ak, cat_id, im_id, i_d, nk, images, im, fn = 'categories', 'annotations', 'category_id',\
                                                  'image_id', 'id', 'name', 'images', 'image_map',\
                                                  'file_name'

    print('reading in data')
    data = read_file(data_file=args.instance_files[0])
    print('data keys: ' + str(data.keys()))

    imgs_bc = images_by_category(data=data, anno_key=ak, category_id=cat_id, 
                                 image_id=im_id, i_d=i_d, image_map_key=im, images_lis=data[images])
    ncs = name_categories(id_key=i_d, name_key=nk, category_data=data[cat_key], 
                    images_by_category=imgs_bc)
    if args.percentages:
        perc, tot = percentages(category_counts=ncs)
        val = sort_by_val(data_map=perc)
        print_data(data_map=val)
        print("Total: %d" % (tot))
    else:
        fns = category_file_names(categories=args.category_names, images_by_category=ncs, 
                                  file_name_key=fn, image_map_key=im)
        for k, v in fns.iteritems():
            print((k, len(v), v))
    
