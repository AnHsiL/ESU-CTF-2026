# from urllib.parse import urlsplit

# urls = [
#     "http://previewsite/",
#     "http://previewsite:80/",
#     "http://127.0.0.1#@previewsite/",
#     "http://previewsite@127.0.0.1/",
#     "http://previewsite\\@127.0.0.1/",
# ]

# for url in urls:
#     p = urlsplit(url)

#     print(f"\nURL: {url}")
#     print(f"  netloc   : {p.netloc}")
#     print(f"  hostname : {p.hostname}")
#     print(f"  port     : {p.port}")
#     print(f"  fragment : {p.fragment}")




import requests
from urllib.parse import urlsplit

urls = [
    "http://previewsite/a/../login",
    "http://previewsite/a/%2e%2e/login",
    "http://previewsite/a/%252e%252e/login",
]

for url in urls:
    parsed = urlsplit(url)
    prepared = requests.Request("GET", url).prepare()

    print("Original:", url)
    print("Parsed:  ", parsed.path)
    print("Prepared:", prepared.url)
    print()