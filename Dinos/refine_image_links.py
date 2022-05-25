import json

metadata_address = "https://bafybeihcxpepca3qpauurthpn2ec7vc7eayxjook2ioesj3b27hb2weuti.ipfs.nftstorage.link"


def refine_token_image(token_name):
    split_image_name = token_name.split(".")

    # join after first parameter
    return metadata_address.join(split_image_name[0:2]) + ".png"


def update_token_image(file_path):
    # update file content
    with open(file_path, 'r+') as f:
        data = json.load(f)
        data['image'] = refine_token_image(data['image'])
        # write back to file
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()


for i in range(10000):
    file_path = "./metadata/" + str(i+1) + ".json"
    update_token_image(file_path)




