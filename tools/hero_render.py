# Render hero stills of Chinbi V2 (standing pose, M1 frame 60) at high resolution.
import os, sys, math
src = open(os.path.expanduser("~/chinbi_blend/render_blend.py")).read()
exec(src[:src.index("os.makedirs(OUT,exist_ok=True)")])
OUTD = os.path.expanduser(OPT.get("out", "~/chinbi_blend/hero/")); os.makedirs(OUTD, exist_ok=True)
f = [f for f in MV if f["seg"] == "M1"][60]
for ob, m in OBJ:
    key = m["top"] if m["top"] in f else "body"
    A = np.array(f[key]); A[:3, 3] *= 0.001; ob.matrix_world = Matrix(A.tolist())
sc.cycles.samples = int(OPT.get("hs", "512")); sc.cycles.adaptive_threshold = 0.01
tgt = Vector((0.0, 0.0, -0.27))
def shot(name, w, h, dist, az, el, fovy):
    HR = float(OPT.get("hr", "1")); sc.render.resolution_x, sc.render.resolution_y = int(w * HR), int(h * HR)
    cd.angle_y = fovy
    d = Vector((math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el)))
    cam.location = tgt + d * dist; cam.rotation_euler = (tgt - cam.location).to_track_quat("-Z", "Y").to_euler()
    sc.render.filepath = OUTD + name; t1 = time.time(); bpy.ops.render.render(write_still=True)
    print("HERO", name, "%.0fs" % (time.time() - t1), flush=True)
az0 = math.atan2(1.9226, 1.0433)  # same side as the video camera
shot("hero_wide.png", 2880, 1220, 2.15, az0, math.radians(14), 0.50)
shot("hero_card.png", 2000, 1400, 2.0, az0, math.radians(16), 0.62)
print("HDONE", flush=True)
