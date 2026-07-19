#!/usr/bin/env python3
"""Lightweight, CPU-only short animation generator -> sunrise_sunset."""
import struct
import zlib
import math
import os

W, H = 480, 270
FRAMES = 90
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frames")
os.makedirs(OUT, exist_ok=True)


def write_png(path, pixels):
    def chunk(typ, data):
        c = struct.pack(">I", len(data)) + typ + data
        c += struct.pack(">I", zlib.crc32(typ + data) & 0xffffffff)
        return c
    raw = bytearray()
    stride = W * 3
    for y in range(H):
        raw.append(0)
        raw.extend(pixels[y * stride:(y + 1) * stride])
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    idat = zlib.compress(bytes(raw), 9)
    with open(path, "wb") as f:
        f.write(sig)
        f.write(chunk(b"IHDR", ihdr))
        f.write(chunk(b"IDAT", idat))
        f.write(chunk(b"IEND", b""))


def lerp(a, b, t):
    return a + (b - a) * t


def clamp(v):
    return max(0, min(255, int(v)))


def sky_color(t):
    day_top = (90, 160, 230)
    night_top = (10, 14, 40)
    day_bot = (200, 225, 245)
    night_bot = (30, 24, 60)
    k = t / 0.5 if t < 0.5 else (1 - t) / 0.5
    k = max(0, min(1, k))
    top = tuple(lerp(night_top[i], day_top[i], k) for i in range(3))
    bot = tuple(lerp(night_bot[i], day_bot[i], k) for i in range(3))
    return top, bot


def draw_circle(buf, cx, cy, r, col):
    for y in range(max(0, cy - r), min(H, cy + r)):
        for x in range(max(0, cx - r), min(W, cx + r)):
            dx, dy = x - cx, y - cy
            if dx * dx + dy * dy <= r * r:
                idx = (y * W + x) * 3
                buf[idx] = clamp(col[0]); buf[idx + 1] = clamp(col[1]); buf[idx + 2] = clamp(col[2])


def draw_rect(buf, x0, y0, x1, y1, col):
    for y in range(max(0, y0), min(H, y1)):
        for x in range(max(0, x0), min(W, x1)):
            idx = (y * W + x) * 3
            buf[idx] = clamp(col[0]); buf[idx + 1] = clamp(col[1]); buf[idx + 2] = clamp(col[2])


def draw_star(buf, cx, cy, r, bright):
    draw_circle(buf, cx, cy, max(1, int(r * bright)), (255, 255, 230))


for f in range(FRAMES):
    t = f / (FRAMES - 1)
    buf = bytearray(W * H * 3)
    top, bot = sky_color(t)
    for y in range(H):
        k = y / H
        r = lerp(top[0], bot[0], k); g = lerp(top[1], bot[1], k); b = lerp(top[2], bot[2], k)
        for x in range(W):
            idx = (y * W + x) * 3
            buf[idx] = clamp(r); buf[idx + 1] = clamp(g); buf[idx + 2] = clamp(b)
    draw_rect(buf, 0, int(H * 0.82), W, H, (40, 70, 40))
    draw_rect(buf, 0, int(H * 0.82), W, int(H * 0.82) + 4, (30, 55, 30))
    sun_x = int(lerp(60, W - 60, t))
    sun_y = int(lerp(H * 0.80, H * 0.30, math.sin(math.pi * t)))
    draw_circle(buf, sun_x, sun_y, 32, (255, 220, 90))
    draw_circle(buf, sun_x, sun_y, 26, (255, 230, 120))
    moon_alpha = max(0.0, 1 - abs(t - 0.5) * 2)
    if moon_alpha > 0.02:
        draw_circle(buf, W - sun_x, H - sun_y, 20, (225, 230, 240))
    for i in range(20):
        sx = (i * 53 + 17) % W
        sy = (i * 29 + 11) % int(H * 0.7)
        tw = 0.5 + 0.5 * math.sin(f * 0.3 + i)
        if moon_alpha > 0.3:
            draw_star(buf, sx, sy, 2, tw * moon_alpha)
    write_png(os.path.join(OUT, f"frame_{f:03d}.png"), buf)

print("frames written:", len(os.listdir(OUT)))
