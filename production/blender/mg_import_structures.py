"""AChR-MG 分子动画 · 真实蛋白结构导入脚本（Molecular Nodes）

适用版本：Blender 5.2 + Molecular Nodes 520.x 扩展。需要联网（从 RCSB PDB / AlphaFold DB 下载）。

做什么：
  1. 下载并导入 IMPORT_CODES 中的结构（清单见下方 STRUCTURES）。
  2. 按每条链的分子描述（mmCIF entity）自动归类并套用分镜配色：
     AChR 绿（α 亚基略深）、IgG/Fab 红、补体紫（C1q/C3b/MAC 由浅到深）、AChE 棕、Nav1.4 钴蓝……
     实验用的毒素、去垢剂、脂质、离子和水不显示；ACh 配体显示为橙色球体。
  3. 含完整 AChR 五聚体的结构自动定向：孔道轴朝 +Z、胞外段朝上，受体顶端位于膜面以上约 6 nm，
     并挂在一个空物体（锚点）下——锚点位置即"孔道轴与膜外表面的交点"，
     把锚点移到 mg_project_setup.py 生成的嵴顶（z = 0 的膜面）上即可替换代理模型。
  4. 抗体与 AChR 共存的结构，在系统控制台打印抗体接触到的受体残基（表位），
     并标出是否落在主要免疫原区（MIR）或 ACh 结合口袋 C 环附近，供核对抗体类型。

用法：
  · 图形界面：先运行 mg_project_setup.py，再在 Scripting 工作区打开本文件，
    按需修改下方 IMPORT_CODES / PROTEIN_STYLE，点击运行。输出信息在"窗口 → 切换系统控制台"中查看。
  · 命令行：blender mg_project.blend -b -P mg_import_structures.py -- --codes 9DMH 9DMJ --save mg_project.blend
            可选 --files 名称=本地路径.cif（离线或自建模型）、--style cartoon
"""

import argparse
import importlib
import re
import sys
from pathlib import Path

import bpy  # 须先于 mathutils 导入（以 pip 版 bpy 模块运行时）
import numpy as np
from mathutils import Matrix, Vector

# 从扩展平台安装、从磁盘安装的扩展，以及 pip 安装的 molecularnodes（配合 bpy 模块）
for _module in ("bl_ext.blender_org.molecularnodes", "bl_ext.user_default.molecularnodes",
                "molecularnodes"):
    try:
        mn = importlib.import_module(_module)
        break
    except ImportError:
        continue
else:
    raise ImportError("未找到 Molecular Nodes：请先在 编辑 → 偏好设置 → 获取扩展 中安装")
if _module == "molecularnodes":
    mn.register()

# ---------- 可修改的设置 ----------

IMPORT_CODES = ["9DMH", "9DMJ", "5HBT", "1HZH"]  # 默认导入第二–四幕最常用的结构
LOCAL_FILES = {}  # 离线或自建模型，如 {"AChR_Fab35": "D:/MG/AChR_Fab35_MIR.cif"}，并把名称加入 IMPORT_CODES
PROTEIN_STYLE = "surface"  # 也可用 "cartoon"、"ribbon"、"spheres"
ECD_ABOVE_MEMBRANE = 6.0   # AChR 胞外段伸出膜面的高度（nm），与场景骨架中的代理模型一致
LAYOUT_SPACING = 60.0      # 导入的结构沿 x 轴排开的间距（nm）
LAYOUT_Z = -600.0          # 放在接头剖面下方，避开剖面摄像机

# 编号: (内容, 用于哪些镜头, 数据库)
STRUCTURES = {
    "9DMG": ("人成人型肌肉 AChR（α2βδε），apo 状态", "S03–S08 受体外形", "rcsb"),
    "9DMH": ("人成人型肌肉 AChR，ACh 结合态", "S04、S06 结合位点", "rcsb"),
    "9DMJ": ("人 AChR + 2 个 MG 患者来源 Fab（fab1b）", "S11–S15 抗体结合参考", "rcsb"),
    "9DMK": ("人 AChR + 1 个 Fab（fab1b）", "备选", "rcsb"),
    "9DML": ("人 AChR + Fab（fab2）", "备选", "rcsb"),
    "9DMQ": ("人 AChR + Fab（fab3）", "备选", "rcsb"),
    "9DMS": ("人 AChR + Fab（fab6）", "备选", "rcsb"),
    "9DMT": ("人 AChR + Fab（fab7）", "备选", "rcsb"),
    "5HBT": ("人 α1 胞外域 + Fab35（经典 MIR 抗体）", "S11 MIR 特写", "rcsb"),
    "1HZH": ("完整人 IgG1（b12）", "S10、S15、S18 IgG 外形", "rcsb"),
    "5DK3": ("完整人 IgG4（帕博利珠单抗）", "S31 IgG4 外形", "rcsb"),
    "1PK6": ("C1q 球状头部", "S18", "rcsb"),
    "2I07": ("C3b", "S19", "rcsb"),
    "6H03": ("膜攻击复合物 MAC（开放构象）", "S20", "rcsb"),
    "4EY4": ("人乙酰胆碱酯酶", "S08", "rcsb"),
    "6AGF": ("人 Nav1.4–β1", "S07、S22、S25", "rcsb"),
    "2IEP": ("MuSK 胞外 Ig1–2（大鼠）", "S30–S31", "rcsb"),
    "3V64": ("agrin–LRP4 复合物", "S30", "rcsb"),
    "Q13702": ("rapsyn（AlphaFold 预测模型，非实验结构）", "S30", "alphafold"),
}

# 与 mg_project_setup.py 的配色一致；若尚未运行该脚本，按此表补建材质
FALLBACK_PALETTE = {
    "MG_AChR": "#3FAF62",
    "MG_AChR_Alpha": "#23864A",
    "MG_ACh": "#F5922F",
    "MG_IgG": "#D62839",
    "MG_C1q": "#B9A2E3",
    "MG_C3b": "#8F63CC",
    "MG_MAC": "#5B2E91",
    "MG_AChE": "#8C5A2E",
    "MG_Nav": "#2B5FD0",
    "MG_Agrin": "#F2F2F2",
    "MG_LRP4": "#E8D88E",
    "MG_MuSK": "#1597C9",
    "MG_Rapsyn": "#4A4F57",
    "MG_Neutral": "#9AA0A6",
}

GLYCAN_WORDS = ("pyranose", "furanose", "mannose", "glucosamine", "galactose", "fucose",
                "neuraminic", "sialic", "acetamido")
THREE_TO_ONE = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLN": "Q", "GLU": "E",
    "GLY": "G", "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F",
    "PRO": "P", "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V",
}
MIR_MOTIF = re.compile(r"WNP.DYGG")     # α1 主要免疫原区核心（成熟肽 α67–76，人 WNPADYGGIK）
LOOP_C_MOTIF = re.compile(r"CC[A-Z]{4}Y")  # α1 C 环：邻位双半胱氨酸 + 酪氨酸（人 YSCCPDTPY）


def classify(description, is_protein):
    """按分子描述返回材质名；返回 None 表示不显示。"""
    d = description.lower()
    if "toxin" in d or d == "water":
        return None
    if "acetylcholinesterase" in d:
        return "MG_AChE"
    if "acetylcholine receptor" in d or "cholinergic receptor" in d:
        return "MG_AChR_Alpha" if "alpha" in d else "MG_AChR"
    if d == "acetylcholine":
        return "MG_ACh"
    if any(k in d for k in ("fab", "heavy chain", "light chain", "immunoglobulin", "antibody",
                            "igg", "pembrolizumab")):
        return "MG_IgG"
    if "sodium channel" in d:
        return "MG_Nav"
    if "c1q" in d:
        return "MG_C1q"
    if "complement" in d and re.search(r"\bc3[a-z]?\b", d):
        return "MG_C3b"
    if "complement" in d:
        return "MG_MAC"
    if "muscle, skeletal receptor tyrosine" in d or "musk" in d or "muscle-specific kinase" in d:
        return "MG_MuSK"
    if "lipoprotein receptor-related protein 4" in d or "lrp4" in d or "lrp-4" in d:
        return "MG_LRP4"
    if "agrin" in d:
        return "MG_Agrin"
    if "receptor-associated protein of the synapse" in d or "rapsyn" in d:
        return "MG_Rapsyn"
    if any(k in d for k in GLYCAN_WORDS):
        return "MG_Neutral"
    return "MG_Neutral" if is_protein else None  # 其余小分子（离子、去垢剂、脂质）不显示


# ---------- 工具 ----------

def ensure_material(name):
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
    h = FALLBACK_PALETTE[name].lstrip("#")
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
           for c in (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))]
    mat = bpy.data.materials.new(name)
    if not mat.node_tree:
        mat.use_nodes = True
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*lin, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.45
    mat.diffuse_color = (*lin, 1.0)
    return mat


def target_collection():
    name = "Structures_结构级"
    col = bpy.data.collections.get(name)
    if not col:
        col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(col)
    return col


def ranges(numbers):
    """[1,2,3,7,8] -> '1–3, 7–8'"""
    out, start, prev = [], None, None
    for n in sorted(set(int(x) for x in numbers)):
        if start is None:
            start = prev = n
        elif n == prev + 1:
            prev = n
        else:
            out.append(f"{start}–{prev}" if prev > start else f"{start}")
            start = prev = n
    if start is not None:
        out.append(f"{start}–{prev}" if prev > start else f"{start}")
    return ", ".join(out)


# ---------- 导入、上色、定向 ----------

def load(code, files):
    if code in files:  # 用绝对路径，重新打开 .blend 时 Molecular Nodes 才能找回源文件
        return mn.Molecule.load(str(Path(files[code]).expanduser().resolve()), name=code)
    database = STRUCTURES.get(code, ("", "", "rcsb"))[2]
    fmt = ".cif" if database == "alphafold" else ".bcif"
    return mn.Molecule.fetch(code, format=fmt, database=database)


def entity_table(mol):
    u = mol.universe
    names = list(mol.props.entity_ids or [])
    per_atom = np.asarray(u.atoms.entity_ids) if hasattr(u.atoms, "entity_ids") else None
    protein = np.isin(np.arange(u.atoms.n_atoms), u.select_atoms("protein").indices)
    rows = []
    if per_atom is None or not names:
        rows.append(("（文件无分子描述）", np.ones(u.atoms.n_atoms, bool), "MG_Neutral"))
        return rows
    for i, desc in enumerate(names):
        mask = per_atom == i
        if mask.any():
            rows.append((desc, mask, classify(desc, bool(protein[mask].any()))))
    return rows


def style_molecule(mol, rows, protein_style):
    u = mol.universe
    groups = {}
    for _desc, mask, mat in rows:
        if mat:
            groups[mat] = groups.get(mat, np.zeros(u.atoms.n_atoms, bool)) | mask
    for mat, mask in groups.items():
        atoms = u.atoms[mask]
        if mat == "MG_ACh":
            style = "spheres"
        elif atoms.select_atoms("protein").n_atoms == 0:
            style = "ball_and_stick"  # 糖链等
        else:
            style = protein_style
        mol.add_style(style, selection=atoms, material=ensure_material(mat), name=mat)
    return groups


def local_frame(mol, groups):
    """返回把分子放到锚点下的局部变换，以及说明文字。"""
    u = mol.universe
    pos = u.atoms.positions * mol.world_scale  # Å → nm（Blender 单位）
    none = np.zeros(len(pos), bool)
    achr = groups.get("MG_AChR", none) | groups.get("MG_AChR_Alpha", none)
    chains = np.asarray(u.atoms.chainIDs)
    receptor_chains = sorted(set(chains[achr]))
    if len(receptor_chains) >= 5:
        centroids = np.array([pos[achr & (chains == c)].mean(0) for c in receptor_chains])
        center = centroids.mean(0)
        normal = np.linalg.svd(centroids - center)[2][2]  # 五个亚基质心所在平面的法线 = 孔道轴
        alpha = groups.get("MG_AChR_Alpha", none)
        ecd = alpha & (np.asarray(u.atoms.resids) <= 210)
        ref = pos[ecd].mean(0) if ecd.any() else pos[achr].max(0)
        if np.dot(normal, ref - pos[achr].mean(0)) < 0:
            normal = -normal
        top = ((pos[achr] - center) @ normal).max()
        rot = Vector(normal).rotation_difference(Vector((0, 0, 1))).to_matrix().to_4x4()
        frame = (Matrix.Translation((0, 0, ECD_ABOVE_MEMBRANE - top)) @ rot
                 @ Matrix.Translation(Vector(-center)))
        return frame, f"已定向：孔道轴→+Z，胞外段朝上，锚点在膜外表面（{len(receptor_chains)} 个受体亚基）"
    shown = np.zeros(len(pos), bool)
    for mask in groups.values():
        shown |= mask
    center = pos[shown].mean(0) if shown.any() else pos.mean(0)
    return Matrix.Translation(Vector(-center)), "未定向（非 AChR 五聚体），锚点在分子中心"


def epitope_report(mol, rows, groups):
    if "MG_IgG" not in groups or not (set(groups) & {"MG_AChR", "MG_AChR_Alpha"}):
        return
    u = mol.universe
    receptor_mask = groups.get("MG_AChR", np.zeros(u.atoms.n_atoms, bool)) | groups.get(
        "MG_AChR_Alpha", np.zeros(u.atoms.n_atoms, bool))
    antibody = u.atoms[groups["MG_IgG"]]
    receptor = u.atoms[receptor_mask]
    from MDAnalysis.lib.distances import capped_distance  # Molecular Nodes 自带 MDAnalysis

    pairs = capped_distance(receptor.positions, antibody.positions, max_cutoff=4.0,
                            return_distances=False)
    contact = receptor[np.unique(pairs[:, 0])] if len(pairs) else receptor[[]]
    desc_of = {}
    for desc, mask, _mat in rows:
        for c in set(np.asarray(u.atoms.chainIDs)[mask]):
            desc_of.setdefault(c, desc)
    print("  抗体表位（距抗体 4 Å 以内的受体残基，按结构文件编号）：")
    if contact.n_atoms == 0:
        print("    无接触")
        return
    for chain in sorted(set(contact.chainIDs)):
        res = contact[contact.chainIDs == chain].residues
        line = f"    链 {chain}（{desc_of.get(chain, '?')}）：{ranges(res.resids)}"
        whole = receptor[receptor.chainIDs == chain].residues
        seq = "".join(THREE_TO_ONE.get(r, "X") for r in whole.resnames)
        notes = []
        m = MIR_MOTIF.search(seq)
        if m:
            mir = set(whole.resids[m.start():m.start() + 10])
            if mir & set(res.resids):
                notes.append("落在 MIR 核心（WNP.DYGG 模体）")
        c = LOOP_C_MOTIF.search(seq, 150)
        if c and "alpha" in desc_of.get(chain, "").lower():
            loop_c = set(whole.resids[max(0, c.start() - 4):c.end() + 2])
            if loop_c & set(res.resids):
                notes.append("接触 C 环（ACh 结合口袋）")
        print(line + ("  ← " + "；".join(notes) if notes else ""))


def import_structure(code, index, files, protein_style):
    title, shots, _db = STRUCTURES.get(code, ("本地结构", "", "rcsb"))
    print(f"\n== {code}：{title}（{shots}）")
    mol = load(code, files)
    rows = entity_table(mol)
    for desc, mask, mat in rows:
        print(f"  {'显示' if mat else '隐藏'}  {mat or '':14s} {desc}  [{int(mask.sum())} 个原子]")
    groups = style_molecule(mol, rows, protein_style)
    frame, note = local_frame(mol, groups)
    print(f"  {note}")
    epitope_report(mol, rows, groups)

    col = target_collection()
    anchor = bpy.data.objects.new(f"{code}_锚点", None)
    anchor.empty_display_type = "ARROWS"
    anchor.empty_display_size = 10.0
    anchor.location = (index * LAYOUT_SPACING, 0.0, LAYOUT_Z)
    col.objects.link(anchor)
    obj = mol.object
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)
    obj.parent = anchor
    obj.matrix_parent_inverse = Matrix.Identity(4)
    obj.matrix_basis = frame
    return mol


def main(argv):
    ap = argparse.ArgumentParser(prog="mg_import_structures.py")
    ap.add_argument("--codes", nargs="+", default=IMPORT_CODES)
    ap.add_argument("--files", nargs="*", default=[], help="名称=本地文件路径，离线或自建模型用")
    ap.add_argument("--style", default=PROTEIN_STYLE)
    ap.add_argument("--save", help="导入后保存为 .blend 文件")
    args = ap.parse_args(argv)
    files = {**LOCAL_FILES, **dict(item.split("=", 1) for item in args.files)}

    for i, code in enumerate(args.codes):
        import_structure(code, i, files, args.style)
    if args.save:
        bpy.ops.wm.save_as_mainfile(filepath=bpy.path.abspath(args.save))
        print(f"\n已保存：{args.save}")


if __name__ == "__main__":
    main(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
