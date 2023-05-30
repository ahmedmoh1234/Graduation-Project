from simple_image_download import simple_image_download as simp
import os

response = simp.simple_image_download

keywords = [
"Wool Fabric Texture",
"Denim Fabric Texture",
"Leather Fabric Texture",
"Cotton Fabric Texture",
"Silk Fabric Texture"
]

for key in keywords:
    response().download(key, 200)