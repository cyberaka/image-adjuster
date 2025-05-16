import os
import sys
from PIL import Image

# IAB standard sizes
IAB_SIZES = {
    "Medium Rectangle": (300, 250),
    "Large Rectangle": (336, 280),
    "Leaderboard": (728, 90),
    "Mobile Leaderboard": (320, 50),
    "Wide Skyscraper": (160, 600),
    "Half Page": (300, 600),
    "Banner": (468, 60),
    "Square": (250, 250),
    "Small Square": (200, 200),
    "Vertical Rectangle": (240, 400),
}

def main(subject_path):
    if not os.path.exists(subject_path):
        print(f"File not found: {subject_path}")
        return

    output_dir = "output_images"
    os.makedirs(output_dir, exist_ok=True)

    # Copy the subject image to output directory for consistent referencing
    subject_filename = os.path.basename(subject_path)
    subject_output_filename = "original_" + subject_filename
    subject_output_path = os.path.join(output_dir, subject_output_filename)
    with Image.open(subject_path) as original_img:
        original_img.save(subject_output_path)
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>IAB Ad Formats with Subject</title>
        <style>
            body {{ font-family: Arial; padding: 20px; }}
            section {{ margin-bottom: 40px; }}
            img {{ display: block; margin-bottom: 10px; border: 1px solid #ccc; }}
            h2 {{ margin-bottom: 10px; }}
            .original-image {{ max-width: 100%; max-height: 400px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <h1>IAB Static Ad Sizes (With Subject)</h1>
        <div>
            <h2>Original Subject Image</h2>
            <img src="{os.path.join(output_dir, subject_output_filename)}" alt="Original Subject" class="original-image">
        </div>
    """

    with Image.open(subject_path) as img:
        for name, (width, height) in IAB_SIZES.items():
            # Create a new blank image with the target dimensions
            new_img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
            
            # Calculate aspect ratio and new dimensions
            img_width, img_height = img.size
            img_aspect = img_width / img_height
            target_aspect = width / height
            
            if img_aspect > target_aspect:
                # Image is wider than target area
                new_width = width
                new_height = int(width / img_aspect)
            else:
                # Image is taller than target area
                new_height = height
                new_width = int(height * img_aspect)
                
            # Resize image while preserving aspect ratio
            resized = img.copy().resize((new_width, new_height), Image.LANCZOS)
            
            # Calculate position to center the image
            x_offset = (width - new_width) // 2
            y_offset = (height - new_height) // 2
            
            # Paste the resized image onto the blank image
            new_img.paste(resized, (x_offset, y_offset))
            
            out_path = os.path.join(output_dir, f"{name.replace(' ', '_')}.png")
            new_img.save(out_path)

            html_content += f"""
            <section>
                <h2>{name} ({width}×{height})</h2>
                <img src="{out_path}" width="{width}" height="{height}" alt="{name}">
            </section>
            """

    html_content += "</body></html>"

    html_file = "iab_subject_gallery.html"
    with open(html_file, "w") as f:
        f.write(html_content)

    print(f"HTML output generated: {html_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_iab_gallery.py <subject_image_path>")
    else:
        main(sys.argv[1])
