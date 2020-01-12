"""
import xml.dom.minidom

doc = xml.dom.minidom.parse("rbcappstore.xml")

print(doc.nodeName)
print(doc.firstChild.tagName)
entries = doc.getElementsByTagName("entry")

for node in entries:
    content = node.getElementsbyTagName("content")
    rating = node.getElementsbyTagName("im:rating")
    print(node.getAttribute("title"))
    print(node.getAttribute("im:rating"))
"""

import xml.etree.ElementTree as ET
import io
import os


def addReview(text, filename):
    with io.open(filename + '.txt', 'a', encoding="utf-8") as file:
        file.write(text)
        file.write('\n')


tree = ET.parse("rbcappstore.xml")
root = tree.getroot()





print(root.tag)

if os.path.exists("title.txt"):
    os.remove("title.txt")

if os.path.exists("rating.txt"):
    os.remove("rating.txt")

if os.path.exists("content.txt"):
    os.remove("content.txt")

ratings = []
contents = []
titles = []

for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
    content = entry.find('.//{http://www.w3.org/2005/Atom}content[@type="text"]').text
    rating = entry.find('{http://itunes.apple.com/rss}rating').text
    title = entry.find('{http://www.w3.org/2005/Atom}title').text

    content = content.replace(r'\n', ' ')
    rating = rating.replace(r'\n', ' ')
    title = title.replace(r'\n', ' ')

    ratings.append(rating)
    contents.append(content)
    titles.append(title)
    # print(repr(content))
    #print(type(title))

for text in contents:
    print(repr(text))
"""
    addReview(title, "title")
    addReview(rating, "rating")
    addReview(content, "content")
"""

# find all tags
"""
elemList=[]
for elem in root.iter():
    elemList.append(elem.tag)

# now I remove duplicities - by convertion to set and back to list
elemList = list(set(elemList))

# Just printing out the result
print(elemList)
"""
