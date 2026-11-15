"""Clean 720p MuJoCo clips of chinbi for the website (no debug captions, camera following the robot).

Usage (mujoco venv, headless):
  MUJOCO_GL=egl python web_clip.py <clip> <ckpt.pt|-> <out.mp4>
clips: walk, turn, payload, getup, sitstand
"""
import os, subprocess, sys
import mujoco
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eval_recovery_mujoco as E
import parameters as P
from eval_body_stability_mujoco import ROOT, viewer_script

W, H = 1280, 720
FRAME_EVERY = 7                        # 0.005 s steps -> 28.57 fps
FPS = 1.0 / (0.005 * FRAME_EVERY)


def scene(payload_kg=0.0):
    viewer_script.XML_PATH = os.path.join(ROOT, "../models/scene_flat.xml")
    viewer_script.PAYLOAD_KG = payload_kg
    xml = viewer_script.build_scene_xml([("", 0.0, None)])
    path = os.path.join(ROOT, "../models/_web_scene_%g.xml" % payload_kg)
    open(path, "w").write(xml)
    return path


class Rec:
    def __init__(self, sim, out, az=140.0, el=-14.0, dist=2.3):
        dist *= 0.78
        self.sim = sim
        sim.m.vis.global_.offwidth, sim.m.vis.global_.offheight = W, H
        sim.m.vis.quality.shadowsize = 8192
        self.r = mujoco.Renderer(sim.m, H, W)
        self.cam = mujoco.MjvCamera()
        self.cam.azimuth, self.cam.elevation, self.cam.distance = az, el, dist
        self.opt = mujoco.MjvOption()
        self.opt.geomgroup[3] = 1
        self.look = None
        self.n = 0
        self.enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                                     "-s", f"{W}x{H}", "-r", f"{FPS:.4f}", "-i", "-", "-c:v", "libx264", "-crf", "22",
                                     "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out],
                                    stdin=subprocess.PIPE)

    def tick(self, daz=0.0):
        self.n += 1
        if self.n % FRAME_EVERY:
            return
        p = self.sim.d.qpos[0:3].copy()
        p[2] = max(p[2] - 0.1, 0.15)
        self.look = p if self.look is None else 0.9 * self.look + 0.1 * p
        self.cam.lookat[:] = self.look
        self.cam.azimuth += daz
        self.r.update_scene(self.sim.d, self.cam, scene_option=self.opt)
        self.enc.stdin.write(self.r.render().tobytes())

    def close(self):
        self.enc.stdin.close(); self.enc.wait()


def pd_step(sim, target):
    d = sim.d
    tau = sim.kp * (target - d.qpos[sim.qa]) - sim.kd * d.qvel[sim.va]
    d.ctrl[sim.aid] = tau
    mujoco.mj_step(sim.m, d)


def settle(sim, s=1.5):
    """Scripted stand-up to the default pose before the policy starts (not recorded)."""
    q0 = sim.d.qpos[sim.qa].copy()
    n = int(s / sim.dt)
    for i in range(n):
        a = min(1.0, i / (0.7 * n))
        pd_step(sim, (1 - a) * q0 + a * sim.default)
    sim.target = sim.default.copy()
    sim.pending = [sim.default.copy() for _ in range(E.ACTION_DELAY_STEPS)]
    sim.step_i = 0


def run(sim, rec, cmd, s, daz=0.0):
    for _ in range(int(s / sim.dt)):
        sim.step(cmd); rec.tick(daz)


def main():
    clip, ckpt, out = sys.argv[1:4]
    payload = 12.0 if clip == "payload" else 0.0
    E.XML = scene(payload) if clip != "stairs" else os.path.join(ROOT, "../models/scene_slope_chatgpt.xml")
    policy = viewer_script.load_policy(ckpt) if ckpt != "-" else (lambda *a: None)
    sim = E.Sim(policy)
    if clip == "getup":
        sim.reset(quat=E.quat_from_rpy(np.pi / 2, 0, 0), z=0.25)
        for _ in range(int(0.3 / sim.dt)):
            pd_step(sim, sim.d.qpos[sim.qa].copy())
        rec = Rec(sim, out, az=150, el=-12, dist=2.2)
        run(sim, rec, [0, 0, 0], 4.0)
        run(sim, rec, [0.5, 0, 0], 3.0)
    else:
        sim.reset()
        settle(sim)
        if clip == "walk":
            rec = Rec(sim, out, az=120, el=-12, dist=2.4)
            run(sim, rec, [0, 0, 0], 0.8)
            run(sim, rec, [0.8, 0, 0], 7.0, daz=0.12)
            run(sim, rec, [0, 0, 0], 1.0)
        elif clip == "turn":
            rec = Rec(sim, out, az=135, el=-18, dist=2.2)
            run(sim, rec, [0, 0, 0], 0.6)
            run(sim, rec, [0, 0, 1.0], 6.5)
            run(sim, rec, [0, 0, 0], 1.0)
        elif clip == "payload":
            rec = Rec(sim, out, az=125, el=-14, dist=2.5)
            run(sim, rec, [0, 0, 0], 1.0)
            run(sim, rec, [0.5, 0, 0], 7.0, daz=0.1)
            run(sim, rec, [0, 0, 0], 1.0)
        elif clip == "stairs":
            rec = Rec(sim, out, az=105, el=-8, dist=3.4)
            for _ in range(int(13.0 / sim.dt)):
                w, x, y, z = sim.d.qpos[3:7]
                yaw = np.arctan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))
                sim.step([0.8, 0.0, float(np.clip(-2.0 * yaw, -1, 1))]); rec.tick()
                if sim.d.qpos[0] > 11.5: break
            run(sim, rec, [0, 0, 0], 1.0)
        elif clip == "sitstand":
            rec = Rec(sim, out, az=150, el=-10, dist=2.1)
            sit = sim.default.copy()
            hip = [i for i, n in enumerate(P.JOINT_NAME) if "hip" in n]
            knee = [i for i, n in enumerate(P.JOINT_NAME) if "knee" in n]
            back = [i for i, n in enumerate(P.JOINT_NAME) if n.startswith(("BR", "BL"))]
            for i in back:
                if i in hip: sit[i] += 0.75
                if i in knee: sit[i] -= 0.95
            sit = np.clip(sit, sim.lo, sim.hi)
            hold = lambda tgt, s: [(pd_step(sim, tgt), rec.tick()) for _ in range(int(s / sim.dt))]
            for _ in range(2):
                hold(sim.default, 0.8)
                q0 = sim.d.qpos[sim.qa].copy()
                n = int(1.2 / sim.dt)
                for k in range(n):
                    a = 0.5 - 0.5 * np.cos(np.pi * k / n); pd_step(sim, (1 - a) * sim.default + a * sit); rec.tick()
                hold(sit, 1.2)
                for k in range(n):
                    a = 0.5 - 0.5 * np.cos(np.pi * k / n); pd_step(sim, (1 - a) * sit + a * sim.default); rec.tick()
            hold(sim.default, 0.8)
    rec.close()
    print("DONE", clip, out, "frames", rec.n // FRAME_EVERY)


if __name__ == "__main__":
    main()
