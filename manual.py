from pprint import pprint
import requests
from lxml import etree

def itter(tree):
    for ele in tree.iter():
        print("##########################")
        print("Tag:", ele.tag)
        print("Text:", ele.text)
        print("Attributes:", ele.attrib)
        print("##########################")


def main():
    # url = f"https://www.boardgamegeek.com/xmlapi/boardgame/174430"
    url = f"https://www.boardgamegeek.com/xmlapi2/thing"
    response = requests.get(url, params={"id": 174430, "stats": 1})
    print(response.request.url)
    print(response.status_code)
    print(response.content)
    tree = etree.fromstring(response.content)
    itter(tree)

if __name__ == "__main__":
    main()
