import os
import json
import shutil
from css_html_js_minify import (
    process_single_html_file, process_single_js_file, process_single_css_file
)


def minify(path):
    if path.endswith(".htm"):
        process_single_html_file(path, overwrite=False)
    if path.endswith(".js"):
        process_single_js_file(path, overwrite=False)
    if path.endswith(".css"):
        process_single_css_file(path, overwrite=False)


def webfinger(root, author):
    folder = f"{root}/.well-known/"
    makefolder(folder, "")

    packet = {"subject": author.name, "links": [l[-1] for l in author.links]}
    with open(f"{folder}webfinger", "w") as fp:
        fp.write(json.dumps(packet))
    return


def makefolder(path, folder):
    if not os.path.exists(f"{path}/{folder}"):
        os.makedirs(f"{path}/{folder}")


def files(path):
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(".org"):
                yield root + os.sep + filename


def images(source, path, destination, doc):
    image_list = [i for i in doc.images()]
    if len(image_list) is 0:
        return

    print("## Images")
    for item in image_list:
        image = item.value[0]
        if image.startswith("http://") or image.startswith("https://"):
            continue

        current_path = os.path.abspath(path + os.sep + image)
        if not os.path.exists(current_path):
            print(f"Missing image {current_path}")
            continue

        print(f"Copying {current_path}")

        new_path = current_path[len(source) + 1:]
        folder = os.path.dirname(new_path)
        item.value[0] = f"../images{new_path}"
        destination_folder = f"{destination}images{new_path}"
        makefolder(destination, f"images{folder}")
        shutil.copy(current_path, f"{destination}/images{new_path}")
