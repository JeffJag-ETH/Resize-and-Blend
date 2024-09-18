# Resize-and-Blend by JeffJag
A node that allows you to combine two images with a built in image resize function so they are both resized to the dimensions you prefer before applying the blend mode of choice at the opacity of choice.

# To install this custom node manually in ComfyUI, follow these steps:

1. Locate your ComfyUI installation directory.

2. Find the "custom_nodes" folder within the ComfyUI directory. If it doesn't exist, create one.

3. Create a new folder within "custom_nodes" for this specific node. You could name it something like "ComfyUI_Image_Resize_And_Blend_Node".

4. Save the Python file in this folder from the repo. You can name it "image_resize_and_blend_node.py".

5. If ComfyUI is running, restart it. If it's not running, start it as you normally would.

Here's a step-by-step breakdown:

```
ComfyUI/
├── custom_nodes/
│   └── ComfyUI_Image_Resize_And_Blend_Node/
│       └── image_resize_and_blend_node.py
├── ...
```

After following these steps, the next time you start ComfyUI, it should automatically detect and load the new custom node. You should see "Image Blend" available in the node menu when you're creating your workflows.

If you encounter any issues:

1. Check the ComfyUI console output for any error messages related to loading custom nodes.
2. Verify that the file is in the correct location and has the correct name.
3. Ensure that the Python file contains the complete code, including the `NODE_CLASS_MAPPINGS` and `NODE_DISPLAY_NAME_MAPPINGS` at the end.

Remember, you'll need to restart ComfyUI each time you make changes to the custom node file for the changes to take effect.
