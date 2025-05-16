# IAB Format Generator

This tool generates images according to IAB (Interactive Advertising Bureau) standard sizes, with a subject image positioned as specified, while preserving aspect ratio.

## Features

- Creates images in all standard IAB sizes
- Preserves aspect ratio when resizing
- Supports multiple positioning options (corners, edges, center)
- Custom positioning using percentage coordinates
- JSON configuration for batch processing with different settings per format
- HTML gallery output for easy visualization

## Usage

### Basic Command Line Usage

```bash
# Basic usage (centers the image in all formats)
python iab_format.py path/to/your/image.jpg

# Specify a predefined position
python iab_format.py path/to/your/image.jpg --position bottom-right

# Use a custom position (x=0.2, y=0.8) - percentages from 0-1
python iab_format.py path/to/your/image.jpg --position 0.2,0.8

# Specify output directory and HTML filename
python iab_format.py path/to/your/image.jpg --output-dir my_output --html-output my_gallery.html
```

### Using JSON Configuration

For more control, you can create a JSON configuration file:

```bash
python iab_format.py --config example_config.json
```

## JSON Configuration Format

The configuration file allows you to specify:

- The subject image path
- Default position for all formats
- Per-format positions
- Output settings

Example:

```json
{
  "subject_image": "/path/to/your/image.jpg",
  "default_position": "center",
  
  "format_positions": {
    "Medium Rectangle": "center",
    "Large Rectangle": "bottom-right",
    "Leaderboard": "top-center",
    "Mobile Leaderboard": "bottom-center",
    "Wide Skyscraper": {
      "position": [0.5, 0.2],
      "comment": "Custom position: centered horizontally, near the top"
    },
    "Half Page": {
      "position": [0.8, 0.3],
      "comment": "Custom position: right side, upper third"
    }
    // Add more formats as needed
  },
  
  "output_settings": {
    "output_dir": "output_images",
    "html_output": "iab_gallery.html",
    "background_color": [255, 255, 255, 0]
  }
}
```

## Position Options

### Predefined Positions

- `center` (default)
- `top-left`, `top-center`, `top-right`
- `middle-left`, `middle-right`
- `bottom-left`, `bottom-center`, `bottom-right`

### Custom Positions

Custom positions use x,y coordinates where both values are between 0 and 1, representing the percentage of available space.

Examples:
- `[0.5, 0.5]`: Center (same as "center")
- `[0, 0]`: Top-left (same as "top-left")
- `[1, 1]`: Bottom-right (same as "bottom-right")
- `[0.5, 0]`: Top-center (same as "top-center")

## Output

The script generates:

1. IAB standard size images with the subject image positioned as specified
2. An HTML gallery showing all generated images
3. A copy of the original subject image for reference