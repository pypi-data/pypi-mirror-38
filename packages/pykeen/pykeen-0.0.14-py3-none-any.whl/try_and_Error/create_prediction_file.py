import json
import numpy as np

if __name__ == '__main__':
    input_path = '/Users/mehdi/PycharmProjects/BioKEEN/data/out/2018-11-20_12:52:31/entity_to_id.json'
    out = '/Users/mehdi/PycharmProjects/BioKEEN/data/out/2018-11-20_12:52:31/entities.tsv'
    with open(input_path) as json_data:
        entity_to_id = json.load(json_data)

    entities = np.array(list(entity_to_id.keys()),dtype=str)
    entities = np.reshape(entities,newshape=(-1,1))

    np.savetxt(fname=out,X=entities,fmt='%s')

    print(entities)