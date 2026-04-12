# Blender Quick Start Guide

## ✅ Setup Complete

Blender 4.2 is installed and the isometric template is ready!

## 🎯 Your Goal

Create better 2D sprites by:
1. Building simple 3D models in Blender
2. Rendering them as 2D sprites
3. Using them in your Godot game

## 🚀 How to Use

### Step 1: Open the Template
```bash
cd ~/hermes-workspace/hermes/development/sakartvelo-defenders/blender_assets
~/.local/bin/blender models/base_templates/isometric_template.blend
```

### Step 2: Create a Simple Model
1. Delete the "ReferenceGrid" (press X)
2. Add a basic shape:
   - Press `Shift + A` → Mesh → Cube (for tower)
   - Press `Shift + A` → Mesh → Cylinder (for enemy)
3. Scale it: Press `S` and drag
4. Rotate if needed: Press `R` and drag
5. Move it: Press `G` and drag

### Step 3: Apply Material
1. Select your object
2. Go to Material Properties (red ball icon)
3. Click `+` to add new material
4. Choose "CelShader" from the dropdown
5. Change Base Color to your desired color

### Step 4: Preview Isometric View
1. Press `Numpad 0` to switch to camera view
2. Press `Numpad 5` to toggle orthographic/perspective
3. You should see the isometric angle

### Step 5: Render Sprite
1. Open the Text Editor (top menu)
2. Click `+ New` → Paste `render_helper.py` content
3. Select your object (right-click)
4. Click the "Run Script" button (play icon)
5. Sprite saves to `renders/[category]/[name].png`

### Step 6: Check Output
```bash
ls -la renders/enemies/  # or heroes/, towers/
```

## 📐 Asset Sizes

| Asset Type | Resolution | Use For |
|-----------|-----------|---------|
| Enemies | 64x64 | Small enemy sprites |
| Heroes | 256x256 | Large hero portraits |
| Towers | 128x128 | Tower sprites |
| Maps | 128x128 | Isometric tiles |
| VFX | 128x128 | Effect sprites |

## 🎨 Style Guidelines

**Keep it simple and stylized:**
- Low poly (few vertices)
- Bold, flat colors
- No complex textures
- Clean silhouettes
- Cel-shaded look

**Why?**
- Faster to create
- Renders cleanly as 2D
- Fits your game's aesthetic
- Easy to modify later

## 🔧 Modifying Render Settings

Edit `render_helper.py` to change:
- Resolution: Edit `RENDER_RESOLUTIONS`
- Camera angle: Edit `ISO_CAMERA_ROTATION`
- Output path: Edit `RENDER_PATH`

## 📝 Workflow Example

Let's create a simple enemy sprite:

```bash
# 1. Open template
~/.local/bin/blender models/base_templates/isometric_template.blend

# 2. In Blender:
#    - Delete grid
#    - Add Cylinder (Shift+A → Mesh → Cylinder)
#    - Scale to make it taller (S + Z)
#    - Add a Sphere on top (Shift+A → Mesh → UV Sphere)
#    - Move sphere up (G + Z)
#    - Select both, join (Ctrl+J)
#    - Apply red material
#    - Rename object to "enemy_test"

# 3. Render
#    - Open Text Editor, paste render_helper.py
#    - Select enemy_test
#    - Run script

# 4. Check output
ls -la renders/enemies/enemy_test.png
```

## 🎯 Next Steps

**Today:**
- ✅ Blender installed
- ✅ Template created
- ⏳ Practice making 1 simple model
- ⏳ Render it to PNG

**This Week:**
- Create base templates for:
  - Simple enemy (humanoid)
  - Simple tower (geometric)
  - Simple hero (detailed humanoid)

**Next Phase:**
- Create all 10 era variants
- Set up batch rendering
- Replace existing 2D assets

## 💡 Tips

1. **Save often!** (Ctrl+S)
2. **Use reference images** - Keep your existing 2D assets open
3. **Start simple** - Don't overcomplicate
4. **Test renders frequently** - See how it looks in 2D
5. **Iterate** - Adjust and re-render until happy

## 🆘 Common Issues

**"Can't see my model"**
- Check camera is active (press Numpad 0)
- Check orthographic view (press Numpad 5)
- Check model isn't hidden (press Alt+H)

**"Render is black"**
- Check lighting is visible
- Check material has color
- Check object is in front of camera

**"Script doesn't run"**
- Make sure object is selected (right-click)
- Check for Python errors in console
- Verify file paths in script

## 📚 Resources

- Blender Basics: https://www.youtube.com/watch?v=TPrnSACiTJ4
- Isometric in Blender: https://docs.blender.org/manual/en/latest/editors/3dview/navigate/views.html
- Cel Shading: https://www.youtube.com/watch?v=dZJ408_7mT8

---

**Ready to start?** Open Blender and try making your first model!
