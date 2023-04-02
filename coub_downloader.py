import time
import os
import requests
import json
import urllib.request

directory = ''


def download(link):
    vid_id = ""
    if "https://coub.com/view/" in link:
        vid_id = link.partition("https://coub.com/view/")[2]
    if len(vid_id) <= 0:
        return post_default("Bad link!")

    url = "http://coub.com/api/v2/coubs/" + vid_id
    resp = requests.get(url)
    if resp.status_code != 200:
        return post_default("Bad response code: " + str(resp.status_code))
    page = json.loads(resp.content)

    if "file_versions" not in page:
        return post_default("Failed to load! No file versions found!")
    versions = page["file_versions"]

    if "html5" not in versions:
        return post_default("Failed to load! No HTML5 video found!")
    html_vids = versions["html5"]["video"]

    hq_vid = get_video(html_vids)
    if hq_vid == "":
        return post_default("Failed to load! No video found!")

    file = page["permalink"] + '.mp4'
    file = os.path.join(directory, file)
    urllib.request.urlretrieve(hq_vid["url"], file)
    print("saved as " + file)
    with open(os.path.join(directory, 'video.txt'), 'w') as writer:
        writer.write(file)


def get_video(html_vids):
    if "higher" in html_vids:
        return html_vids["higher"]
    if "high" in html_vids:
        return html_vids["high"]
    if "mid" in html_vids:
        return html_vids["mid"]
    return ""


def post_default(msg):
    print(msg)
    print("posting DEFAULT")
    with open(os.path.join(directory, 'video.txt'), 'w') as writer:
        writer.write("")


def main() -> None:
    global directory
    directory = os.path.dirname(__file__)
    current_url = ''
    while True:
        time.sleep(10)
        url = ''
        with open(os.path.join(directory, 'db.txt'), 'r') as reader:
            url = reader.read()
        if url == current_url:
            continue
        current_url = url
        download(current_url)


if __name__ == '__main__':
    main()
