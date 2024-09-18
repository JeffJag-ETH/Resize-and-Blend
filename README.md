# Resize-and-Blend by JeffJag
This custom node for ComfyUI allows you to resize and blend two images of different sizes then combine the Image Top over the Image Bottom using various blending modes. Many thanks to WASasquatch for their work on WAS Suite.

## Installation

1. Clone this repository into your `ComfyUI/custom_nodes/` directory:
   ```
   git clone https://github.com/JeffJag-ETH/Resize-and-Blend.git
   ```
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

After installation, the "Resize and Blend" node will be available in the ComfyUI interface under the "image/processing" category.

Use the included workflow json if you wish.

![Resize and Blend example](https://github.com/user-attachments/assets/5d8108fb-6de2-4dad-bab9-d10217928bcb)

## Parameters

- Image_Top: The top image for blending
- Image_Base: The base image for blending
- Resize_Width: Width to resize images to
- Resize_Height: Height to resize images to
- Supersample: Whether to use supersampling
- Resample: Resampling method
- Blending_Mode: The blending mode to use
- Blend_Percentage: The percentage of blending to apply

## License
GNU GENERAL PUBLIC LICENSE - Version 3, 29 June 2007
