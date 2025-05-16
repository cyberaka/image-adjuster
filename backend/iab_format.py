import os
import sys
import json
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

def parse_position(position_data):
    """
    Parse position data from various formats into a standard format.
    
    Args:
        position_data: Can be a string like 'center', 'top-left', etc.,
                      a list/tuple of [x, y] coordinates (0-1),
                      or a dict with a 'position' key
    
    Returns:
        A standardized position value (string or tuple)
    """
    valid_positions = [
        "center", "top-left", "top-center", "top-right", 
        "middle-left", "middle-right", "right", "left", "top", "bottom",
        "bottom-left", "bottom-center", "bottom-right"
    ]
    
    # If it's a dictionary with position key
    if isinstance(position_data, dict) and 'position' in position_data:
        position = position_data['position']
        # If it's a list/array in the JSON, convert to tuple
        if isinstance(position, list) and len(position) == 2:
            return (float(position[0]), float(position[1]))
        return position
    
    # If it's a string position
    if isinstance(position_data, str):
        if position_data in valid_positions:
            return position_data
        print(f"Invalid position: {position_data}. Using 'center' instead.")
        return "center"
    
    # If it's already a tuple or list of coordinates
    if (isinstance(position_data, tuple) or isinstance(position_data, list)) and len(position_data) == 2:
        try:
            return (float(position_data[0]), float(position_data[1]))
        except (ValueError, TypeError):
            print(f"Invalid position coordinates: {position_data}. Using 'center' instead.")
            return "center"
    
    # Default to center if nothing else matched
    print(f"Unrecognized position format: {position_data}. Using 'center' instead.")
    return "center"

def process_from_json(config_path):
    """
    Process images according to a JSON configuration file.
    
    Args:
        config_path: Path to the JSON configuration file
    """
    if not os.path.exists(config_path):
        print(f"Configuration file not found: {config_path}")
        return
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON configuration: {e}")
        return
    except Exception as e:
        print(f"Error reading configuration file: {e}")
        return
    
    # Extract configuration
    subject_path = config.get('subject_image')
    if not subject_path or not os.path.exists(subject_path):
        print(f"Subject image not found: {subject_path}")
        return
    
    # Get format-specific positions or use default
    format_positions = config.get('format_positions', {})
    default_position = parse_position(config.get('default_position', 'center'))
    
    # Get output settings
    output_settings = config.get('output_settings', {})
    output_dir = output_settings.get('output_dir', 'output_images')
    html_output = output_settings.get('html_output', 'iab_gallery.html')
    background_color = tuple(output_settings.get('background_color', [255, 255, 255, 0]))
    
    # Call main with the configuration
    main(
        subject_path, 
        format_positions=format_positions,
        default_position=default_position,
        output_dir=output_dir,
        html_output=html_output,
        background_color=background_color
    )

def main(subject_path, format_positions=None, default_position="center", 
         output_dir="output_images", html_output="iab_gallery.html", 
         background_color=(255, 255, 255, 0)):
    """
    Generate IAB standard size images with the subject image positioned according to preference.
    
    Args:
        subject_path: Path to the subject image
        format_positions: Dictionary mapping IAB format names to position settings
        default_position: Default position to use when not specified in format_positions
        output_dir: Directory to save output images
        html_output: Filename for the HTML gallery
        background_color: RGBA background color for the images
    """
    if not os.path.exists(subject_path):
        print(f"File not found: {subject_path}")
        return
    
    # Initialize format positions if not provided
    if format_positions is None:
        format_positions = {}
    
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
            .comment {{ color: #666; font-style: italic; margin-bottom: 10px; }}
        </style>
    </head>
    <body>
        <h1>IAB Static Ad Sizes (With Subject)</h1>
        <div>
            <h2>Original Subject Image</h2>
            <img src="{os.path.join(os.path.basename(output_dir), subject_output_filename)}" alt="Original Subject" class="original-image">
        </div>
    """

    def calculate_offsets(position_value, width, height, new_width, new_height):
        """Helper function to calculate x and y offsets based on position value"""
        x_offset = 0
        y_offset = 0
        
        max_x_offset = width - new_width
        max_y_offset = height - new_height
        
        if isinstance(position_value, tuple) and len(position_value) == 2:
            # Custom percentage offsets
            x_percentage, y_percentage = position_value
            x_percentage = max(0, min(1, x_percentage))  # Clamp between 0 and 1
            y_percentage = max(0, min(1, y_percentage))  # Clamp between 0 and 1
            
            x_offset = int(max_x_offset * x_percentage)
            y_offset = int(max_y_offset * y_percentage)
        else:
            # Predefined positions
            if position_value == "center" or position_value == "middle-center":
                x_offset = max_x_offset // 2
                y_offset = max_y_offset // 2
            elif position_value == "top-left":
                x_offset = 0
                y_offset = 0
            elif position_value == "top-center":
                x_offset = max_x_offset // 2
                y_offset = 0
            elif position_value == "top-right":
                x_offset = max_x_offset
                y_offset = 0
            elif position_value == "middle-left":
                x_offset = 0
                y_offset = max_y_offset // 2
            elif position_value == "middle-right":
                x_offset = max_x_offset
                y_offset = max_y_offset // 2
            elif position_value == "bottom-left":
                x_offset = 0
                y_offset = max_y_offset
            elif position_value == "bottom-center":
                x_offset = max_x_offset // 2
                y_offset = max_y_offset
            elif position_value == "bottom-right":
                x_offset = max_x_offset
                y_offset = max_y_offset
            elif position_value == "right":
                x_offset = max_x_offset
                y_offset = max_y_offset // 2
            elif position_value == "left":
                x_offset = 0
                y_offset = max_y_offset // 2
            elif position_value == "top":
                x_offset = max_x_offset // 2
                y_offset = 0
            elif position_value == "bottom":
                x_offset = max_x_offset // 2
                y_offset = max_y_offset
                
        return x_offset, y_offset

    with Image.open(subject_path) as img:
        for name, (width, height) in IAB_SIZES.items():
            # Get the position for this format, or use default
            format_position_data = format_positions.get(name, default_position)
            current_position = parse_position(format_position_data)
            
            # Extract comment if available
            comment = None
            if isinstance(format_position_data, dict) and 'comment' in format_position_data:
                comment = format_position_data['comment']
            
            # Create a new blank image with the target dimensions
            new_img = Image.new("RGBA", (width, height), background_color)
            
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
            
            # Calculate position offsets
            x_offset, y_offset = calculate_offsets(
                current_position, width, height, new_width, new_height
            )
            
            # Paste the resized image onto the blank image
            new_img.paste(resized, (x_offset, y_offset))
            
            out_path = os.path.join(output_dir, f"{name.replace(' ', '_')}.png")
            new_img.save(out_path)

            # Display position in human-readable format
            position_display = current_position
            if isinstance(current_position, tuple):
                position_display = f"Custom ({current_position[0]:.2f}, {current_position[1]:.2f})"
            
            # Add format section to HTML    
            html_content += f"""
            <section>
                <h2>{name} ({width}×{height})</h2>
                <p>Position: {position_display}</p>
            """
            
            # Add comment if available
            if comment:
                html_content += f'<p class="comment">Note: {comment}</p>'
                
            html_content += f"""
                <img src="{os.path.join(os.path.basename(output_dir), os.path.basename(out_path))}" width="{width}" height="{height}" alt="{name}">
            </section>
            """

    html_content += "</body></html>"

    # Place HTML file one level above the output_dir
    parent_dir = os.path.dirname(os.path.abspath(output_dir))
    html_file = os.path.join(parent_dir, html_output)
    with open(html_file, "w") as f:
        f.write(html_content)

    print(f"HTML output generated: {html_file}")
    print(f"All images saved to: {output_dir}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate IAB standard images with subject image")
    parser.add_argument("image_path", nargs="?", help="Path to the subject image (not needed if using --config)")
    parser.add_argument(
        "--position", 
        default="center",
        help=(
            "Position of subject in frame. Options: center (default), top-left, "
            "top-center, top-right, middle-left, middle-right, bottom-left, "
            "bottom-center, bottom-right. Or use custom position with x,y values "
            "between 0 and 1 (e.g., '0.2,0.8')"
        )
    )
    parser.add_argument(
        "--config",
        help="Path to JSON configuration file"
    )
    parser.add_argument(
        "--output-dir",
        default="output_images",
        help="Directory to save output images (default: output_images)"
    )
    parser.add_argument(
        "--html-output",
        default="iab_gallery.html",
        help="Filename for the HTML gallery (default: iab_gallery.html)"
    )
    
    args = parser.parse_args()
    
    # Check if we're using a config file
    if args.config:
        process_from_json(args.config)
    else:
        # Check if image path is provided
        if not args.image_path:
            parser.error("image_path is required when not using --config")
        
        # Handle custom position if provided as x,y format
        position = args.position
        if isinstance(position, str) and "," in position:
            try:
                x, y = map(float, position.split(","))
                position = (x, y)
            except ValueError:
                print(f"Invalid custom position format: {position}. Using 'center' instead.")
                position = "center"
        
        main(
            args.image_path, 
            default_position=position,
            output_dir=args.output_dir,
            html_output=args.html_output
        )
