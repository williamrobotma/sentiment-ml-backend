import xml.etree.ElementTree as ET

def parseItunesXml(filename, contents, ratings, titles):
    tree = ET.parse(filename)
    root = tree.getroot()
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        content = entry.find('.//{http://www.w3.org/2005/Atom}content[@type="text"]').text
        rating = entry.find('{http://itunes.apple.com/rss}rating').text
        title = entry.find('{http://www.w3.org/2005/Atom}title').text

        ratings.append(rating)
        contents.append(content)
        titles.append(title)
        # print(repr(content))
        #print(type(title))

### How to use function
"""
contents = []
ratings = []
titles = []

parseItunesXml("rbcappstore.xml", contents, ratings, titles)

for content in contents:
    print(repr(content))
"""

