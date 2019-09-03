import argparse
import json

CAT_KEY = 'categories'
ANNOTATIONS = 'annotations'
IMAGE_ID = 'image_id'
I_D = 'id'
CAT_ID_KEY = 'category_id'
IMAGES = 'images'   

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

def ids_from_path(path, read_func):
    return set(map(lambda i: int(i), 
                   filter(lambda n: n, read_func(path=path).split('\n'))))

def annotations_from_disk(path, read_func, map_func, cat_key, images_key, 
                          anno_key, id_key):
    data = read_func(path=path)
    data_maps = {kc[0]: map_func(coll=kc[1], key=id_key) for kc in 
         ((cat_key, data[cat_key]), (images_key, data[images_key]), (anno_key, data[anno_key]))}
    return (data, data_maps)

def split_data(data_maps, val_ids, images_key, anno_key, image_id_key):
    val_images = {ik: data_maps[images_key][ik] for ik in data_maps[images_key] if ik in ids}
    val_annos = {ak: data_maps[anno_key][ak] for ak in data_maps[anno_key]\
             if data_maps[anno_key][ak][image_id_key] in ids}
    train_images = {ik: data_maps[images_key][ik] for ik in\
                    set(data_maps[images_key]).difference(set(val_images))}
    train_annos = {ak: data_maps[anno_key][ak] for ak in\
                   set(data_maps[anno_key]).difference(set(val_annos))}

    return (train_images, train_annos), (val_images, val_annos)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Split a dataset')
    parser.add_argument('--instance-file', required=False)
    parser.add_argument('--image-dir', required=False)
    parser.add_argument('--validation-ids-path', required=False)
    parser.add_argument('--target-train', nargs=2, required=False)
    parser.add_argument('--target-validation', nargs=2, required=False)
    args = parser.parse_args()

    ids = ids_from_path(path=args.validation_ids_path, read_func=read_file)
    data, data_maps = annotations_from_disk(args.instance_file, read_func=read_json_file, 
                                            map_func=map_from_coll, cat_key=CAT_KEY, images_key=IMAGES, 
                                            anno_key=ANNOTATIONS, id_key=I_D)

    train, val = split_data(data_maps=data_maps, val_ids=ids, images_key=IMAGES, anno_key=ANNOTATIONS, 
               image_id_key=IMAGE_ID)


