# By jeffjag.eth
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to
# deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import torch
import numpy as np
from PIL import Image, ImageOps
import pilgram.css.blending

class ResizeBlend:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Image_Top": ("IMAGE",),
                "Image_Base": ("IMAGE",),
                "Resize_Width": ("INT", {"default": 896, "min": 64, "max": 4096, "step": 8}),
                "Resize_Height": ("INT", {"default": 1152, "min": 64, "max": 4096, "step": 8}),
                "Supersample": (["true", "false"],),
                "Resample": (["lanczos", "nearest", "bilinear", "bicubic"],),
                "Blending_Mode": ([
                    "add",
                    "color",
                    "color_burn",
                    "color_dodge",
                    "darken",
                    "difference",
                    "exclusion",
                    "hard_light",
                    "hue",
                    "lighten",
                    "multiply",
                    "overlay",
                    "screen",
                    "soft_light"
                ],),
                "Blend_Percentage": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "process_images"
    CATEGORY = "image/processing"

    def tensor2pil(self, image):
        return Image.fromarray(np.clip(255. * image[0].cpu().numpy(), 0, 255).astype(np.uint8))

    def pil2tensor(self, image):
        return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)


    def process_images(self, Image_Top, Image_Base, Resize_Width, Resize_Height, Supersample, Resample, Blending_Mode, Blend_Percentage):
        try:
            import pilgram.css.blending
        except ImportError:
            raise ImportError("The 'pilgram' library is required for this node. Please install it using 'pip install pilgram' in your ComfyUI Python environment.")

        # Ensure width and height are divisible by 8
        new_width = Resize_Width if Resize_Width % 8 == 0 else Resize_Width + (8 - Resize_Width % 8)
        new_height = Resize_Height if Resize_Height % 8 == 0 else Resize_Height + (8 - Resize_Height % 8)

        # Define resampling filters
        resample_filters = {
            'nearest': Image.NEAREST,
            'bilinear': Image.BILINEAR,
            'bicubic': Image.BICUBIC,
            'lanczos': Image.LANCZOS
        }

        # Process Image_Top
        pil_img_top = self.tensor2pil(Image_Top)
        if Supersample == 'true':
            pil_img_top = pil_img_top.resize((new_width * 8, new_height * 8), resample=resample_filters[Resample])
        resized_top = pil_img_top.resize((new_width, new_height), resample=resample_filters[Resample])

        # Process Image_Base
        pil_img_base = self.tensor2pil(Image_Base)
        if Supersample == 'true':
            pil_img_base = pil_img_base.resize((new_width * 8, new_height * 8), resample=resample_filters[Resample])
        resized_base = pil_img_base.resize((new_width, new_height), resample=resample_filters[Resample])

        # Apply blending
        img_b = resized_top
        img_a = resized_base

        # Apply blending
        if Blending_Mode:
            if Blending_Mode == "color":
                out_image = pilgram.css.blending.color(img_a, img_b)
            elif Blending_Mode == "color_burn":
                out_image = pilgram.css.blending.color_burn(img_a, img_b)
            elif Blending_Mode == "color_dodge":
                out_image = pilgram.css.blending.color_dodge(img_a, img_b)
            elif Blending_Mode == "darken":
                out_image = pilgram.css.blending.darken(img_a, img_b)
            elif Blending_Mode == "difference":
                out_image = pilgram.css.blending.difference(img_a, img_b)
            elif Blending_Mode == "exclusion":
                out_image = pilgram.css.blending.exclusion(img_a, img_b)
            elif Blending_Mode == "hard_light":
                out_image = pilgram.css.blending.hard_light(img_a, img_b)
            elif Blending_Mode == "hue":
                out_image = pilgram.css.blending.hue(img_a, img_b)
            elif Blending_Mode == "lighten":
                out_image = pilgram.css.blending.lighten(img_a, img_b)
            elif Blending_Mode == "multiply":
                out_image = pilgram.css.blending.multiply(img_a, img_b)
            elif Blending_Mode == "add":
                out_image = pilgram.css.blending.normal(img_a, img_b)
            elif Blending_Mode == "overlay":
                out_image = pilgram.css.blending.overlay(img_a, img_b)
            elif Blending_Mode == "screen":
                out_image = pilgram.css.blending.screen(img_a, img_b)
            elif Blending_Mode == "soft_light":
                out_image = pilgram.css.blending.soft_light(img_a, img_b)
            else:
                out_image = img_a
        else:
            out_image = img_a

        out_image = out_image.convert("RGB")
        
        # Blend image
        blend_mask = Image.new(mode="L", size=img_a.size, color=(round(Blend_Percentage * 255)))
        blend_mask = ImageOps.invert(blend_mask)
        final_result = Image.composite(img_a, out_image, blend_mask)

        # Convert the result back to a ComfyUI-compatible tensor
        return (self.pil2tensor(final_result),)

NODE_CLASS_MAPPINGS = {
    "ResizeBlend": ResizeBlend
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "ResizeBlend": "Resize and Blend"
}