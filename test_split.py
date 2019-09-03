# def test_split_data():
#     print("comp_images: %d, data_images: %d" % (len(comp_images), len(data[IMAGES])))
#     print("comp_annos: %d, data_annos: %d" % (len(comp_annos), len(data[ANNOTATIONS])))

#     print("comp_images == data_maps[IMAGES]: " + str(comp_images == set(data_maps[IMAGES])))
#     print("comp_annos == data_maps[ANNOTATIONS] " + str(comp_annos == set(data_maps[ANNOTATIONS])))

#     train_inter = set(train[0]).intersection(val[0])
#     val_inter = set(train[1]).intersection(val[1])

#     print("train_inter len " + str(len(train_inter)))
#     print("val_inter len " + str(len(val_inter)))

#     print("ids == val[0]: " + str(ids == set(val[0])))
