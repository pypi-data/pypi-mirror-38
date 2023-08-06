from urllib.parse import urlsplit


def return_int_from_image_url(url):
    current_url = urlsplit(url)
    return int(current_url.path.split("/")[-1].split(".")[0][0])

