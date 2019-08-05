import json
import argparse

def read_file(**kwargs):
    data_file = kwargs['data_file']

    with open(data_file) as data_file:
        data = json.load(data_file)

    return data

def images_by_category(**kwargs):
    d, ak, cid, img_id, i_d = kwargs['data'], kwargs['anno_key'], kwargs['category_id'], kwargs['image_id'],\
                              kwargs['i_d']

    cat_img = {}
    for e, v in d[ak].iteritems():
        if e[cid] not in cat_img:
            cat_img[e[cid]] = []
        cat_img[e[cid]].append({i_d: e[i_d], img_id: e[img_id]})
        
    return cat_img

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Split a dataset')
    parser.add_argument('--instance-files', nargs='+', required=True, help='Annotations file')
    parser.add_argument('--category-ids', nargs='+', required=True, help='Categories')
    args = parser.parse_args()

    print('reading in data')
    data = read_file(data_file=args.instance_files[0])
    print('data keys: ' + str(data.keys()))

    ims = images_by_category(data=data, anno_key='annotations', category_id='categories', 
                       image_id='images', i_d='id')

    im_count = {k: len(ims[k]) for k in ims.keys()}
    print('counts ' + str(im_count))
