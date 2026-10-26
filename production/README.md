# production · 3D 制作文件

配合 [3D 制作手册](../docs/AChR-MG_3D制作手册_Blender_MolecularNodes.md) 使用，在你自己的电脑上运行（Blender 5.2 + Molecular Nodes 520.x 扩展）。

| 路径 | 内容 |
|---|---|
| `blender/mg_project_setup.py` | 新建项目：渲染参数、配色材质、S01–S34 镜头标记、接头剖面骨架（正常版 + 受损版）、摄像机与灯光 |
| `blender/mg_import_structures.py` | 下载并导入真实蛋白结构，自动配色、定向，打印抗体表位报告 |
| `chimerax/inspect_achr_structures.cxc` | 在 ChimeraX 中并排查看 9DMH、9DMJ、5HBT，画接触界面图 |
| `chimerax/build_mir_model_9DMH_5HBT.cxc` | 把 Fab35 叠合到全长人源 AChR 上（S11 示意模型） |
| `post/subtitles_zh.srt` | 字幕，可导入剪映、Premiere、DaVinci Resolve |
| `post/narration_zh.txt` | 逐镜配音稿 |
| `post/shots.json` | 镜头时间表（含 24 fps 帧号） |
| `tools/storyboard_to_post.py` | 分镜改动后重新生成 `post/` 中的三个文件 |

## 快速开始

1. Blender 新建常规文件 → Scripting 工作区 → 打开并运行 `blender/mg_project_setup.py` → 另存为 `mg_project.blend`。
2. 在同一文件中打开并运行 `blender/mg_import_structures.py`（需联网，首次下载需几分钟）。
3. 按手册第 5 节逐镜制作、第 7 节渲染、第 8 节核对。

分镜时间改动后：

```bash
python production/tools/storyboard_to_post.py          # 更新字幕、配音稿、shots.json
python production/tools/storyboard_to_post.py --fps 25 # 改用 25 fps 时
```

## 测试情况

- 两个 Blender 脚本已在 Blender 5.2.3（bpy 模块）+ Molecular Nodes 520.2.0 中运行：场景、材质、镜头标记、正常版与受损版骨架均生成并渲染了预览；结构导入用离线结构文件测试了分类配色、自动定向（孔道轴误差为 0）和表位报告。
- **未测试**：从 RCSB / AlphaFold 联网下载结构（测试环境网络受限），以及两个 ChimeraX 命令文件（测试环境无法安装 ChimeraX）。首次在你电脑上运行时如有报错，请把报错信息反馈。
