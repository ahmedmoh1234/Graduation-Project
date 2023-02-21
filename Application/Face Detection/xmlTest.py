import xml.etree.ElementTree as ET

tree = ET.parse("haarcascade_frontalface_default.xml")

for elem in tree.iter():
    print(elem)