import palettetools as pt

css = 'css'
json = 'json'
img1 = "https://assets.imgix.net/examples/bluehat.jpg"
img2 = "https://sherwinski.imgix.net/pineneedles.jpg"

print("Parsing for bluehat.jpg")
print("Running with css...\n")
print(pt.extract_colors_css(img1))
print("Running with json...\n")
print(pt.extract_colors_json(img1))
print("\nRunning for text color...\n")
print(pt.overlay_text_color(img1))

print("Parsing for pineneedles.jpg")
print("Running with css...\n")
print(pt.extract_colors_css(img2))
print("Running with json...\n")
print(pt.extract_colors_json(img2))
print("\nRunning for text color...\n")
print(pt.overlay_text_color(img2))