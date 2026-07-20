# CPU-Based Animation Toolkit

All tools here run **without a GPU** (CPU only). They produce real 3D /
traditional animation — NOT AI video diffusion (that needs a CUDA GPU).

## What's installed

| Tool | CPU? | Use | How to run |
|------|------|-----|------------|
| **Blender 3.0.1** | Yes (Cycles CPU) | Studio-lit 3D rendering, best quality | `bash animation/render_blender.sh 120` |
| **Panda3D 1.10.16** | Yes (headless) | Real-time 3D scenes, game-style animation | `python3 animation/panda3d/panda3d_render.py animation/output/panda3d 120` |
| **Godot 3.2.3** (headless server) | Yes | 2D/3D game & animation engine | `godot3-server --path animation/godot --script render.gd` |
| **ffmpeg 4.4.2** | Yes | Encode PNG frames -> pro MP4 (H.264 CRF 18) | `bash animation/encode.sh animation/output/blender 24 out.mp4` |

## Quick start (Blender, the highest quality)

```bash
cd <workspace>
bash animation/render_blender.sh 120        # renders 120 frames + encodes
# result: animation/output/blender.mp4
```

To use your own model instead of the demo torus: replace the
`primitive_torus_*` block in `animation/blender/blender_render.py` with
`bpy.ops.import_scene.obj(filepath="your_model.obj")` or load a `.blend` / `.glb`.

## Panda3D

```bash
python3 animation/panda3d/panda3d_render.py animation/output/panda3d 120
bash animation/encode.sh animation/output/panda3d 24 animation/output/panda3d.mp4
```

## Godot (headless)

```bash
godot3-server --path animation/godot --script render.gd
bash animation/encode.sh animation/output/godot 24 animation/output/godot.mp4
```

## Honest expectations

- **Quality:** Blender + Cycles gives genuinely "studio" lighting (3-point
  lights, denoising, depth-of-field). It is real CGI, not AI video.
- **Speed:** On CPU this is SLOW. A 1080p Cycles frame can take 10s–2min
  each; a 5s clip (120 frames) may take 20–60+ min on CPU. Lower
  `resolution_x/y` and `cycles.samples` for speed.
- **"Fast + studio quality" on CPU is contradictory** for raytracing. For
  speed, use Panda3D/Godot (real-time rasterization, much faster, slightly
  less photoreal) or drop Blender samples to ~32.

## AI video (needs GPU — not runnable here)

The earlier SkyReels-V2 and Wan-family setups are GPU-only. They are cloned
in `SkyReels-V2/` and import cleanly, but require a CUDA GPU to actually
generate video. For true "Kling-like" AI motion, run those on a cloud GPU.
