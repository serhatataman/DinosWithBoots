import json


def refine_token_name(token_name):
    split_name = token_name.split(" ")

    # remove leading zeros
    number = split_name[-1].replace("#", "")
    r = number.lstrip("0")

    # combine the rest
    return (" ".join(split_name[:-1]) + " #" + r).strip()


def update_token_name(file_path):
    # update file content
    with open(file_path, 'r+') as f:
        data = json.load(f)
        data['name'] = refine_token_name(data['name'])
        # write back to file
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()


for i in range(10000):
    file_path = "./metadata/" + str(i+1) + ".json"
    update_token_name(file_path)




