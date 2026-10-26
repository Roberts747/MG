"""AChR-MG 分子动画 · Blender 项目初始化脚本

适用版本：Blender 5.2（与 Molecular Nodes 520.x 配套）。

做什么：
  1. 项目设置：1920×1080、24 fps、全片 7200 帧、色彩管理设为 Standard（保证配色与 HEX 一致）。
  2. 按分镜配色规范建立全部材质（MG_ 开头）。
  3. 在时间轴上为 S01–S34 每个镜头放置标记（marker）。
  4. 搭建"接头级"神经肌肉接头剖面骨架：神经末梢、活性区、突触小泡与 ACh、基底膜、
     乙酰胆碱酯酶、褶皱突触后膜、肌细胞胞质，以及嵴顶 AChR、谷底 Nav1.4 代理模型。
  5. 另建一套"受损版"突触后膜（褶皱变浅变宽、数目减少，受体与钠通道减少），
     供 S22、S24、S27 等前后对比镜头使用；默认不启用，在大纲视图中勾选 NMJ_Scaffold_受损 即可。
  6. 建立剖面摄像机与灯光。

比例：1 Blender 单位（BU）= 1 nm，与 Molecular Nodes 520.x 导入结构的默认比例一致，
     因此用 mg_import_structures.py 导入的真实蛋白结构可直接放到嵴顶替换代理模型。
     间隙宽度、小泡、受体按真实数量级；褶皱深度做了压缩；ACh 小球做了放大（示意）。

用法：
  · 图形界面：Scripting 工作区 → 打开本文件 → 运行脚本。
    MODE = "new" 会清空当前场景，请在新文件中运行；分镜时间改动后，把 MODE 改为 "markers"
    并在已有项目中运行，只更新镜头标记和帧范围（先用 storyboard_to_post.py 更新 shots.json，
    再把 SHOTS_JSON 设为其路径）。
  · 命令行：blender -b -P mg_project_setup.py -- --save mg_project.blend
            可选 --shots ../post/shots.json（读取最新镜头时间）、--markers-only（只更新标记）、
            --preview preview.png（渲染一张预览图）
"""

import argparse
import json
import math
import random
import sys

import bpy  # 须先于 bmesh / mathutils 导入（以 pip 版 bpy 模块运行时）
import bmesh
from mathutils import Matrix, Vector

# 图形界面运行时可修改的设置
MODE = "new"       # "new"：新建全部（清空当前场景）；"markers"：只更新镜头标记与帧范围
SHOTS_JSON = ""    # 留空则用下方内置的镜头表；也可填 production/post/shots.json 的完整路径

FPS = 24

# 镜号、起止秒数、所属幕（由 production/tools/storyboard_to_post.py 从分镜生成）
SHOTS = [
    ("S01", 0, 3, "第一幕 开场"),
    ("S02", 3, 12, "第一幕 开场"),
    ("S03", 12, 20, "第二幕 正常神经肌肉接头信号传递"),
    ("S04", 20, 28, "第二幕 正常神经肌肉接头信号传递"),
    ("S05", 28, 38, "第二幕 正常神经肌肉接头信号传递"),
    ("S06", 38, 47, "第二幕 正常神经肌肉接头信号传递"),
    ("S07", 47, 58, "第二幕 正常神经肌肉接头信号传递"),
    ("S08", 58, 67, "第二幕 正常神经肌肉接头信号传递"),
    ("S09", 67, 77, "第二幕 正常神经肌肉接头信号传递"),
    ("S10", 77, 87, "第三幕 自身抗体出现"),
    ("S11", 87, 97, "第三幕 自身抗体出现"),
    ("S12", 97, 101, "第三幕 自身抗体出现"),
    ("S13", 101, 111, "第四幕 三条致病机制"),
    ("S14", 111, 117, "第四幕 三条致病机制"),
    ("S15", 117, 127, "第四幕 三条致病机制"),
    ("S16", 127, 136, "第四幕 三条致病机制"),
    ("S17", 136, 146, "第四幕 三条致病机制"),
    ("S18", 146, 156, "第四幕 三条致病机制"),
    ("S19", 156, 165, "第四幕 三条致病机制"),
    ("S20", 165, 175, "第四幕 三条致病机制"),
    ("S21", 175, 181, "第四幕 三条致病机制"),
    ("S22", 181, 190, "第四幕 三条致病机制"),
    ("S23", 190, 197, "第四幕 三条致病机制"),
    ("S24", 197, 207, "第五幕 信号减弱与肌无力"),
    ("S25", 207, 216, "第五幕 信号减弱与肌无力"),
    ("S26", 216, 227, "第五幕 信号减弱与肌无力"),
    ("S27", 227, 239, "第六幕 波动性肌无力"),
    ("S28", 239, 248, "第六幕 波动性肌无力"),
    ("S29", 248, 260, "第六幕 波动性肌无力"),
    ("S30", 260, 269, "第七幕 补充：MuSK-MG 与 AChR-MG 的差异"),
    ("S31", 269, 282, "第七幕 补充：MuSK-MG 与 AChR-MG 的差异"),
    ("S32", 282, 289, "第七幕 补充：MuSK-MG 与 AChR-MG 的差异"),
    ("S33", 289, 296, "第八幕 结尾"),
    ("S34", 296, 300, "第八幕 结尾"),
]

# 材质名: (HEX, 不透明度, 粗糙度, 自发光强度)
# 前 6 项为分镜约定配色，其余为补充配色，与分镜脚本第二部分一致。
PALETTE = {
    "MG_Presynaptic": ("#A9D4F5", 0.35, 0.5, 0.0),       # 突触前膜 / 神经末梢（半透明，露出小泡）
    "MG_PresynapticMembrane": ("#A9D4F5", 1.0, 0.5, 0.0),  # 末梢朝向间隙的膜
    "MG_Vesicle": ("#A9D4F5", 0.45, 0.3, 0.0),           # 突触小泡
    "MG_ACh": ("#F5922F", 1.0, 0.35, 0.3),               # 乙酰胆碱：橙色小球
    "MG_AChR": ("#3FAF62", 1.0, 0.4, 0.0),               # AChR：绿色跨膜蛋白
    "MG_AChR_Alpha": ("#23864A", 1.0, 0.4, 0.0),         # AChR α 亚基：略深的绿（真实结构中区分 α）
    "MG_IgG": ("#D62839", 1.0, 0.4, 0.0),                # IgG 自身抗体：红色 Y 型
    "MG_C1q": ("#B9A2E3", 1.0, 0.45, 0.0),               # 补体 C1q：浅紫
    "MG_C3b": ("#8F63CC", 1.0, 0.45, 0.0),               # 补体 C3b：中紫
    "MG_MAC": ("#5B2E91", 1.0, 0.45, 0.0),               # 膜攻击复合物：深紫
    "MG_Postsynaptic": ("#C8CDD3", 1.0, 0.55, 0.0),      # 突触后膜：浅灰褶皱
    "MG_Ca": ("#FFE04A", 1.0, 0.3, 2.0),                 # Ca²⁺：亮黄光点
    "MG_Na": ("#FFFFFF", 1.0, 0.3, 2.0),                 # Na⁺：白色光点
    "MG_Signal": ("#FFFFFF", 0.6, 0.3, 3.0),             # 终板电位 / 动作电位光晕
    "MG_Nav": ("#2B5FD0", 1.0, 0.4, 0.0),                # Nav1.4：钴蓝
    "MG_AChE": ("#8C5A2E", 1.0, 0.5, 0.0),               # 乙酰胆碱酯酶：棕色
    "MG_BasalLamina": ("#EFE6D2", 0.3, 0.6, 0.0),        # 基底膜：半透明米白细网
    "MG_Lysosome": ("#F4EFE2", 0.5, 0.4, 0.0),           # 溶酶体：半透明乳白
    "MG_AChR_Inactive": ("#7E9A88", 1.0, 0.5, 0.0),      # 失活 AChR：灰绿
    "MG_Agrin": ("#F2F2F2", 1.0, 0.45, 0.0),             # 聚集蛋白 agrin：白
    "MG_LRP4": ("#E8D88E", 1.0, 0.45, 0.0),              # LRP4：淡黄
    "MG_MuSK": ("#1597C9", 1.0, 0.45, 0.0),              # MuSK：青蓝
    "MG_Rapsyn": ("#4A4F57", 1.0, 0.5, 0.0),             # rapsyn：深灰
    "MG_IgG4_OtherArm": ("#C4C4C4", 1.0, 0.45, 0.0),     # IgG4 无关臂：灰白
    "MG_MuscleFiber": ("#E5C7A1", 1.0, 0.6, 0.0),        # 肌纤维：暖米色（宏观镜头）
    "MG_MuscleCytoplasm": ("#3A3330", 1.0, 0.8, 0.0),    # 肌细胞胞质剖面：暗暖灰
    "MG_ActiveZone": ("#6FA6D6", 1.0, 0.5, 0.0),         # 活性区：较深的浅蓝
    "MG_Neutral": ("#9AA0A6", 1.0, 0.5, 0.0),            # 未归类结构：中性灰
}
BACKGROUND = "#0F1726"  # 背景：深海军蓝

# 接头级剖面的几何参数（单位 nm，1 BU = 1 nm）
SLAB_X = 240.0         # 剖面左右半宽
SLAB_Y = 40.0          # 剖面前后半厚
CLEFT = 50.0           # 初级突触间隙宽度
MEMBRANE = 4.0         # 脂双层厚度
FOLD_SPACING = 60.0    # 褶皱间距（示意，已压缩）
FOLD_HALF_OPENING = 10.0
FOLD_DEPTH = 90.0      # 褶皱深度（示意，真实约 0.5–1 μm，已压缩）
FILLET = 6.0           # 褶皱开口处圆角
FOLDS = [FOLD_SPACING * (i - 3.5) for i in range(8)]  # 8 个褶皱的中心 x
TERMINAL_TOP = 210.0
VESICLE_R = 20.0       # 小泡半径（直径约 40 nm）
ACH_R = 2.2            # ACh 小球半径（真实 < 1 nm，放大示意）
ACHR_KEEP = 1.0        # 保留的 AChR 代理比例
NAV_KEEP = 1.0         # 保留的 Nav1.4 代理比例
RNG = random.Random(7)

# 受损版突触后膜：补体反复攻击后褶皱变浅变宽、数目减少，受体与钠通道减少。
# 各数值为示意，用于前后对比，不代表定量的病理数据。
DAMAGED = {
    "FOLDS": [FOLDS[i] for i in (0, 2, 3, 5, 7)],
    "FOLD_HALF_OPENING": 16.0,
    "FOLD_DEPTH": 45.0,
    "FILLET": 10.0,
    "ACHR_KEEP": 0.35,
    "NAV_KEEP": 0.4,
}


# ---------- 通用工具 ----------

def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hex_to_rgba(hex_color, alpha=1.0):
    h = hex_color.lstrip("#")
    return tuple(srgb_to_linear(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4)) + (alpha,)


def make_material(name, hex_color, alpha, roughness, emission):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if not mat.node_tree:
        mat.use_nodes = True
    rgba = hex_to_rgba(hex_color)
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = rgba
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Alpha"].default_value = alpha
    if emission:
        bsdf.inputs["Emission Color"].default_value = rgba
        bsdf.inputs["Emission Strength"].default_value = emission
    mat.diffuse_color = rgba[:3] + (alpha,)  # 视图着色时的颜色
    if alpha < 1.0:
        if hasattr(mat, "surface_render_method"):
            mat.surface_render_method = "BLENDED"
        if hasattr(mat, "use_transparency_overlap"):
            mat.use_transparency_overlap = True
    return mat


def collection(name, parent=None):
    col = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    parent = parent or bpy.context.scene.collection
    if col.name not in parent.children:
        parent.children.link(col)
    return col


def mesh_object(name, bm, material, col, smooth=True):
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    if smooth and hasattr(mesh, "shade_smooth"):
        mesh.shade_smooth()
    mesh.materials.append(material)
    obj = bpy.data.objects.new(name, mesh)
    col.objects.link(obj)
    return obj


def add_cylinder(bm, radius, depth, matrix, segments=12):
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segments,
                          radius1=radius, radius2=radius, depth=depth, matrix=matrix)


def add_sphere(bm, radius, center, segments=12):
    bmesh.ops.create_uvsphere(bm, u_segments=segments, v_segments=max(6, segments // 2),
                              radius=radius, matrix=Matrix.Translation(center))


def add_box(bm, size, matrix):
    """size 为 (x, y, z) 全长。"""
    m = matrix @ Matrix.Diagonal(Vector((size[0], size[1], size[2], 1.0)))
    bmesh.ops.create_cube(bm, size=1.0, matrix=m)


def extrude_profile(bm, points, half_depth):
    """把 x–z 平面上的闭合多边形沿 y 方向拉伸成实体。"""
    front = [bm.verts.new((x, -half_depth, z)) for x, z in points]
    back = [bm.verts.new((x, half_depth, z)) for x, z in points]
    bm.faces.new(front[::-1])
    bm.faces.new(back)
    n = len(points)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((front[i], front[j], back[j], back[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])


def arc(cx, cz, r, a0, a1, steps=8):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * k / steps)),
             cz + r * math.sin(math.radians(a0 + (a1 - a0) * k / steps))) for k in range(steps + 1)]


def fold_profile(offset):
    """突触后膜在 x–z 平面上的轮廓（从左到右）。offset=0 为朝向间隙的膜表面，
    offset=MEMBRANE 为膜的胞质侧（向肌细胞内平移）。"""
    w = FOLD_HALF_OPENING + offset
    r = FILLET - offset
    bottom = -(FOLD_DEPTH + offset)
    pts = [(-SLAB_X, -offset)]
    for xc in FOLDS:
        pts += arc(xc - w - r, -offset - r, r, 90, 0)            # 左侧开口圆角
        pts += arc(xc, bottom + w, w, 180, 360, steps=12)       # 褶皱底部半圆（左壁→右壁）
        pts += arc(xc + w + r, -offset - r, r, 180, 90)          # 右侧开口圆角
    pts.append((SLAB_X, -offset))
    return pts


# ---------- 场景设置 ----------

def setup_scene(shots):
    scene = bpy.context.scene
    scene.render.resolution_x, scene.render.resolution_y = 1920, 1080
    scene.render.resolution_percentage = 100
    scene.render.fps = FPS
    engines = {e.identifier for e in scene.render.bl_rna.properties["engine"].enum_items}
    scene.render.engine = "BLENDER_EEVEE" if "BLENDER_EEVEE" in engines else "BLENDER_EEVEE_NEXT"
    try:  # 默认的 AgX 会压暗、去饱和，Standard 才能让渲染颜色与 HEX 一致
        scene.view_settings.view_transform = "Standard"
        scene.view_settings.look = "None"
    except TypeError:
        print("注意：未找到 Standard 视图变换，请在 渲染属性 → 色彩管理 中手动设置")
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = "//render/frame_"
    scene.unit_settings.system = "NONE"

    world = scene.world or bpy.data.worlds.new("MG_World")
    scene.world = world
    if not world.node_tree:
        world.use_nodes = True
    bg = next(n for n in world.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs["Color"].default_value = hex_to_rgba(BACKGROUND)
    bg.inputs["Strength"].default_value = 1.0

    update_markers(shots)


def update_markers(shots):
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = shots[-1][2] * FPS
    scene.timeline_markers.clear()
    for sid, start, _end, _act in shots:
        scene.timeline_markers.new(sid, frame=start * FPS + 1)


def load_shots(path):
    data = json.loads(open(path, encoding="utf-8").read())
    if data["fps"] != FPS:
        print(f"注意：shots.json 按 {data['fps']} fps 生成，本脚本使用 {FPS} fps，按秒数重新换算帧号")
    return [(s["id"], s["start_seconds"], s["end_seconds"], s["act"]) for s in data["shots"]]


# ---------- 接头级剖面骨架 ----------

def build_postsynaptic(col, mats, suffix=""):
    top = fold_profile(0.0)
    under = fold_profile(MEMBRANE)

    bm = bmesh.new()
    extrude_profile(bm, top + under[::-1], SLAB_Y)
    mesh_object("Postsynaptic_Membrane" + suffix, bm, mats["MG_Postsynaptic"], col, smooth=False)

    bm = bmesh.new()
    bottom = -140.0  # 正常版与受损版的胞质底面一致，便于叠化过渡
    extrude_profile(bm, under + [(SLAB_X, bottom), (-SLAB_X, bottom)], SLAB_Y - 0.1)
    mesh_object("Muscle_Cytoplasm" + suffix, bm, mats["MG_MuscleCytoplasm"], col, smooth=False)


def crest_ranges():
    edges = [-SLAB_X] + [x for xc in FOLDS for x in (xc - FOLD_HALF_OPENING - FILLET,
                                                    xc + FOLD_HALF_OPENING + FILLET)] + [SLAB_X]
    return list(zip(edges[0::2], edges[1::2]))


def build_achr_proxies(col, mats, suffix=""):
    """嵴顶密集排列的 AChR 代理：5 个圆柱围成的五聚体，直径约 8 nm、长约 16 nm，
    胞外段伸出膜面约 6 nm。"""
    bm = bmesh.new()
    spacing = 9.0
    for x0, x1 in crest_ranges():
        n = max(1, int((x1 - x0 - 10.0) / spacing) + 1)  # 两端各留出约一个受体半径
        span = (n - 1) * spacing
        for i in range(n):
            x = (x0 + x1) / 2 - span / 2 + i * spacing
            for k in range(9):
                y = -36.0 + k * spacing
                if RNG.random() > ACHR_KEEP:
                    continue
                spin = RNG.uniform(0, 2 * math.pi)
                for s in range(5):
                    a = spin + s * 2 * math.pi / 5
                    m = Matrix.Translation((x + 2.4 * math.cos(a), y + 2.4 * math.sin(a), -2.0))
                    add_cylinder(bm, 1.7, 16.0, m, segments=10)
    return mesh_object("AChR_Proxies_Crests" + suffix, bm, mats["MG_AChR"], col)


def build_nav_proxies(col, mats, suffix=""):
    """褶皱谷底的 Nav1.4 代理：底部一排，两侧壁下部各两排。"""
    bm = bmesh.new()
    rot_y = Matrix.Rotation(math.pi / 2, 4, "Y")
    wall_bottom = -(FOLD_DEPTH - FOLD_HALF_OPENING)  # 侧壁与底部半圆的交界
    for xc in FOLDS:
        for k in range(7):
            y = -36.0 + k * 12.0
            if RNG.random() <= NAV_KEEP:
                add_box(bm, (6.0, 6.0, 9.0), Matrix.Translation((xc, y, -FOLD_DEPTH - 1.0)))
            for z in (-FOLD_DEPTH + 24.0, -FOLD_DEPTH + 13.0):
                for side in (-1, 1):
                    if z > wall_bottom or RNG.random() > NAV_KEEP:
                        continue
                    x = xc + side * (FOLD_HALF_OPENING + 1.0)
                    add_box(bm, (6.0, 6.0, 9.0), Matrix.Translation((x, y, z)) @ rot_y)
    return mesh_object("Nav14_Proxies_Troughs" + suffix, bm, mats["MG_Nav"], col, smooth=False)


def build_damaged(mats):
    """在同一位置另建受损版突触后膜，默认从视图层中排除。"""
    g = globals()
    saved = {k: g[k] for k in DAMAGED}
    g.update(DAMAGED)
    try:
        col = collection("NMJ_Scaffold_受损")
        build_postsynaptic(col, mats, "_Damaged")
        build_achr_proxies(col, mats, "_Damaged")
        build_nav_proxies(col, mats, "_Damaged")
    finally:
        g.update(saved)
    bpy.context.view_layer.layer_collection.children[col.name].exclude = True


def build_presynaptic(col, mats):
    bm = bmesh.new()
    height = TERMINAL_TOP - CLEFT
    add_box(bm, (2 * SLAB_X - 20.0, 2 * SLAB_Y - 2.0, height),
            Matrix.Translation((0, 0, CLEFT + height / 2)))
    term = mesh_object("Presynaptic_Terminal", bm, mats["MG_Presynaptic"], col, smooth=False)
    bevel = term.modifiers.new("Bevel", "BEVEL")
    bevel.width, bevel.segments = 15.0, 6

    bm = bmesh.new()
    add_box(bm, (2 * SLAB_X - 40.0, 2 * SLAB_Y - 4.0, MEMBRANE),
            Matrix.Translation((0, 0, CLEFT + MEMBRANE / 2)))
    mesh_object("Presynaptic_Membrane", bm, mats["MG_PresynapticMembrane"], col, smooth=False)

    # 活性区：与褶皱开口上下对位的条带
    bm = bmesh.new()
    for xc in FOLDS:
        add_box(bm, (16.0, 2 * SLAB_Y - 6.0, 3.0), Matrix.Translation((xc, 0, CLEFT + MEMBRANE + 1.5)))
    mesh_object("Active_Zones", bm, mats["MG_ActiveZone"], col, smooth=False)


def build_vesicles(col, mats):
    centers = []
    floor = CLEFT + MEMBRANE + 3.0 + VESICLE_R
    for xc in FOLDS:  # 锚定在活性区的小泡
        for y in (-18.0, 18.0):
            centers.append(Vector((xc, y, floor)))
    tries = 0
    while len(centers) < 60 and tries < 5000:  # 末梢内其余小泡
        tries += 1
        c = Vector((RNG.uniform(-SLAB_X + 30, SLAB_X - 30), RNG.uniform(-18.0, 18.0),
                    RNG.uniform(floor + 10.0, TERMINAL_TOP - VESICLE_R - 10.0)))
        if all((c - o).length > 2 * VESICLE_R + 3.0 for o in centers):
            centers.append(c)

    bm = bmesh.new()
    for c in centers:
        add_sphere(bm, VESICLE_R, c, segments=24)
    mesh_object("Synaptic_Vesicles", bm, mats["MG_Vesicle"], col)

    bm = bmesh.new()
    for c in centers:
        for _ in range(10):
            d = Vector((RNG.gauss(0, 1), RNG.gauss(0, 1), RNG.gauss(0, 1))).normalized()
            add_sphere(bm, ACH_R, c + d * RNG.uniform(0, VESICLE_R - 5.0), segments=8)
    mesh_object("ACh_In_Vesicles", bm, mats["MG_ACh"], col)


def build_cleft(col, mats):
    # 基底膜：位于间隙中部的细网
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=96, y_segments=16, size=1.0)
    xs = [v.co.x for v in bm.verts]
    ys = [v.co.y for v in bm.verts]
    sx = 2 * (SLAB_X - 5.0) / (max(xs) - min(xs))
    sy = 2 * (SLAB_Y - 2.0) / (max(ys) - min(ys))
    bmesh.ops.scale(bm, vec=(sx, sy, 1.0), verts=bm.verts[:])
    bmesh.ops.translate(bm, vec=(0, 0, CLEFT / 2), verts=bm.verts[:])
    lamina = mesh_object("Basal_Lamina", bm, mats["MG_BasalLamina"], col, smooth=False)
    wire = lamina.modifiers.new("Wireframe", "WIREFRAME")
    wire.thickness = 0.5

    # 乙酰胆碱酯酶：以细尾锚定在基底膜上的棕色酶
    bm = bmesh.new()
    for x0, x1 in crest_ranges()[1:-1]:
        for y in (-24.0, 12.0):
            x = RNG.uniform(x0 + 3.0, x1 - 3.0)
            z = CLEFT / 2 - 4.5
            add_sphere(bm, 3.2, Vector((x - 2.0, y, z)), segments=10)
            add_sphere(bm, 3.2, Vector((x + 2.0, y, z - 1.0)), segments=10)
            add_cylinder(bm, 0.5, 4.5, Matrix.Translation((x, y, CLEFT / 2 - 1.5)), segments=6)
    mesh_object("AChE", bm, mats["MG_AChE"], col)


def build_camera_and_lights(col):
    scene = bpy.context.scene
    cam_data = bpy.data.cameras.new("CAM_Section")
    cam_data.lens = 35
    cam_data.clip_start, cam_data.clip_end = 1.0, 5000.0
    cam = bpy.data.objects.new("CAM_Section", cam_data)
    col.objects.link(cam)
    cam.location = (0.0, -580.0, 55.0)
    cam.rotation_euler = (math.radians(90), 0.0, 0.0)
    scene.camera = cam

    key = bpy.data.lights.new("Key_Sun", "SUN")
    key.energy = 3.0
    key_obj = bpy.data.objects.new("Key_Sun", key)
    key_obj.rotation_euler = (math.radians(50), math.radians(-15), math.radians(-20))
    col.objects.link(key_obj)

    fill = bpy.data.lights.new("Fill_Sun", "SUN")
    fill.energy = 1.0
    fill_obj = bpy.data.objects.new("Fill_Sun", fill)
    fill_obj.rotation_euler = (math.radians(75), 0.0, math.radians(30))
    col.objects.link(fill_obj)


def clear_scene():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for col in list(bpy.data.collections):
        bpy.data.collections.remove(col)


def main(argv):
    ap = argparse.ArgumentParser(prog="mg_project_setup.py")
    ap.add_argument("--save", help="保存为 .blend 文件")
    ap.add_argument("--shots", help="production/post/shots.json 的路径")
    ap.add_argument("--preview", help="渲染一张剖面预览图（PNG）")
    ap.add_argument("--markers-only", action="store_true", help="只更新镜头标记与帧范围")
    args = ap.parse_args(argv)

    shots_json = args.shots or SHOTS_JSON
    shots = load_shots(shots_json) if shots_json else SHOTS
    if args.markers_only or MODE == "markers":
        update_markers(shots)
        print(f"已更新 {len(shots)} 个镜头标记，帧范围 1–{bpy.context.scene.frame_end}")
        if args.save:
            bpy.ops.wm.save_as_mainfile(filepath=bpy.path.abspath(args.save))
        return

    clear_scene()
    setup_scene(shots)
    mats = {name: make_material(name, *spec) for name, spec in PALETTE.items()}

    scaffold = collection("NMJ_Scaffold_接头级")
    pre = collection("Presynaptic_突触前", scaffold)
    cleft = collection("Cleft_突触间隙", scaffold)
    post = collection("Postsynaptic_突触后", scaffold)
    collection("Structures_结构级")
    rig = collection("Camera_Lights")

    build_presynaptic(pre, mats)
    build_vesicles(pre, mats)
    build_cleft(cleft, mats)
    build_postsynaptic(post, mats)
    build_achr_proxies(post, mats)
    build_nav_proxies(post, mats)
    build_damaged(mats)
    build_camera_and_lights(rig)

    if args.save:
        bpy.ops.wm.save_as_mainfile(filepath=bpy.path.abspath(args.save))
        print(f"已保存：{args.save}")
    if args.preview:
        scene = bpy.context.scene
        scene.frame_set(scene.timeline_markers["S03"].frame)
        scene.render.filepath = bpy.path.abspath(args.preview)
        bpy.ops.render.render(write_still=True)
        print(f"预览图：{args.preview}")
    print(f"完成：{len(mats)} 个材质，{len(shots)} 个镜头标记，帧范围 1–{bpy.context.scene.frame_end}")


if __name__ == "__main__":
    main(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
