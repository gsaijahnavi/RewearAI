import os
import re
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

def show_outfit_montage(
    suggestion: dict,
    metadata_store: list,
    image_size: tuple = (200, 200),
    title: str = "Outfit"
):
    """
    suggestion: {
      "top": "<item_name>",
      "bottom": "<item_name>",
      "outerwear": "<item_name or 'none'>",
      "comment": "<explanation text>"
    }
    metadata_store: [
      {"item": "<item_name>", "image_path": "<path/to/img.png>", ...},
      ...
    ]
    """
    # 1) pick parts
    parts = ["top", "bottom"]
    if suggestion.get("outerwear", "").lower() not in ("none", ""):
        parts.append("outerwear")

    # 2) lookup paths (exact match including digits, case-insensitive)
    paths = []
    for part in parts:
        name = suggestion[part]
        # Match suggestion name (e.g., 'blazer1') to image filename (without extension), case-insensitive
        path = next((m["image_path"] for m in metadata_store if name.lower() == os.path.splitext(os.path.basename(m["image_path"]))[0].lower()), None)
        paths.append(path)

    # 3) load or placeholder
    images = []
    for idx, p in enumerate(paths):
        if p and os.path.exists(p):
            img = Image.open(p).convert("RGB").resize(image_size)
        else:
            # grey placeholder
            img = Image.new("RGB", image_size, (200,200,200))
            draw = ImageDraw.Draw(img)
            font = ImageFont.load_default()
            w,h = draw.textbbox((0,0), parts[idx], font=font)[2:]
            draw.text(((image_size[0]-w)//2,(image_size[1]-h)//2),
                      parts[idx], fill="black", font=font)
        images.append(img)

    # 4) compose canvas
    margin = 10
    # measure text areas
    measure = ImageDraw.Draw(Image.new("RGB",(1,1)))
    title_h = measure.textbbox((0,0), title, font=ImageFont.load_default())[3]
    cmnt_h  = measure.textbbox((0,0), suggestion["comment"], 
                               font=ImageFont.load_default())[3]

    canvas_w = len(images)*image_size[0] + margin*(len(images)-1)
    canvas_h = title_h + margin + image_size[1] + margin + cmnt_h + margin
    canvas = Image.new("RGB",(canvas_w,canvas_h),"white")
    draw = ImageDraw.Draw(canvas)

    # draw title
    tw = measure.textbbox((0,0), title, font=ImageFont.load_default())[2]
    draw.text(((canvas_w-tw)//2, 5), title, font=ImageFont.load_default(), fill="black")

    # paste images
    y0 = title_h + margin
    x0 = 0
    for img in images:
        canvas.paste(img, (x0, y0))
        x0 += image_size[0] + margin

    # draw comment
    draw.text((5, y0 + image_size[1] + margin), 
              suggestion["comment"], font=ImageFont.load_default(), fill="black")

    # show
    plt.figure(figsize=(len(images)*2, 4))
    plt.imshow(canvas)
    plt.axis("off")
    plt.show()

# Ensure this is at the bottom of the file, not at the top level
if __name__ == "__main__":
    pass


