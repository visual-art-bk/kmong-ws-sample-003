def read_urls(path):
    with open("url.txt", "r") as file:
        return file.read().splitlines()
