#from palettetools import palettetools
import palettetools as pt
import json

css = 'css'
json_string = 'json'
img1 = "https://assets.imgix.net/examples/bluehat.jpg"
img2 = "https://sherwinski.imgix.net/pineneedles.jpg"
img3 = "https://sherwinski.imgix.net/pineneedles1.jpg"
img4 = "https://www.google.com/"
'''
print("Parsing for bluehat.jpg")
print("Running with css...\n")
print(pt.extract_colors_css(img1))
print("Running with json...\n")
print(pt.extract_colors_json(img1))
print("\nRunning for text color...\n")
print(pt.overlay_text_color(img1))
'''
print("Parsing for pineneedles.jpg")
print("Running with css...\n")
print(pt.extract_colors_css(img2))
print("Running with json...\n")
print(pt.extract_colors_json(img2))
print("\nRunning for text color...\n")
print(pt.overlay_text_color(img2))

'''
print("---------------------")
resp = pt.extract_colors_json(img2)


try:
	json_obj = json.loads(resp)
except Exception as e:
	raise ValueError ('Invalid imgix-url, function call cannot be completed')
'''