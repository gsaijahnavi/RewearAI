import os
import re
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import textwrap

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
            img = Image.open(p).convert("RGB")
            # Pad image to keep aspect ratio
            orig_w, orig_h = img.size
            target_w, target_h = image_size
            ratio = min(target_w / orig_w, target_h / orig_h)
            new_w, new_h = int(orig_w * ratio), int(orig_h * ratio)
            img = img.resize((new_w, new_h), Image.LANCZOS)
            padded = Image.new("RGB", image_size, (255,255,255))
            pad_x = (target_w - new_w) // 2
            pad_y = (target_h - new_h) // 2
            padded.paste(img, (pad_x, pad_y))
            img = padded
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
    title_font = None
    try:
        title_font = ImageFont.truetype("Arial.ttf", 28)
    except Exception:
        title_font = ImageFont.load_default()
    heading = "OOTD"
    # Use title_font for all title measurements
    title_h = measure.textbbox((0,0), heading, font=title_font)[3]
    tw = measure.textbbox((0,0), heading, font=title_font)[2]
    cmnt_h  = measure.textbbox((0,0), suggestion["comment"], 
                               font=ImageFont.load_default())[3]

    canvas_w = len(images)*image_size[0] + margin*(len(images)-1)
    canvas_h = title_h + margin + image_size[1] + margin + cmnt_h + margin
    canvas = Image.new("RGB",(canvas_w,canvas_h),"white")
    draw = ImageDraw.Draw(canvas)

    # draw title with a cleaner font and custom heading
    draw.text(((canvas_w-tw)//2, 5), heading, font=title_font, fill="#22223B")

    # paste images
    y0 = title_h + margin
    x0 = 0
    for img in images:
        canvas.paste(img, (x0, y0))
        x0 += image_size[0] + margin

    # draw comment (wrap to fit actual pixel width, and dynamically expand canvas if needed)
    comment = suggestion["comment"]
    font = ImageFont.load_default()
    max_width = canvas_w - 10
    # Wrap comment to fit pixel width
    lines = []
    for line in comment.splitlines():
        # Use textwrap to split, but check pixel width for each line
        for chunk in textwrap.wrap(line, width=100):
            # Further split if pixel width is too large
            while font.getbbox(chunk)[2] > max_width:
                # Find a split point
                for i in range(len(chunk)-1, 0, -1):
                    if chunk[i] == ' ':
                        break
                if i == 0:
                    break
                lines.append(chunk[:i])
                chunk = chunk[i+1:]
            lines.append(chunk)
    # Dynamically expand canvas height if needed
    comment_height = sum([font.getbbox(line)[3] + 2 for line in lines])
    needed_canvas_h = title_h + margin + image_size[1] + margin + comment_height + margin
    if needed_canvas_h > canvas_h:
        # Create a new, taller canvas and copy old content
        new_canvas = Image.new("RGB", (canvas_w, needed_canvas_h), "white")
        new_canvas.paste(canvas, (0, 0))
        canvas = new_canvas
        draw = ImageDraw.Draw(canvas)
    y_comment = y0 + image_size[1] + margin
    for line in lines:
        draw.text((5, y_comment), line, font=font, fill="black")
        y_comment += font.getbbox(line)[3] + 2

    # show
    plt.figure(figsize=(len(images)*2, 4))
    plt.imshow(canvas)
    plt.axis("off")
    plt.show()

# Ensure this is at the bottom of the file, not at the top level
if __name__ == "__main__":
    pass


