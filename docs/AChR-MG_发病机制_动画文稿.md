# 乙酰胆碱受体抗体阳性重症肌无力（AChR-MG）发病机制 · 分子动画文稿

> 版本：v0.1（初稿）
> 受众：医学生、基础医学研究者
> 用途：作为分子动画分镜脚本的科学底稿。每一节均按"**空间位置 → 参与分子 → 动态先后 → 结果**"组织。
> 标注约定：
> - 专业名词首次出现时给出 **中文全称（英文全称，缩写）**，此后使用缩写。
> - 【需要文献验证】：表示该内容存在学术争议、数据因研究而异，或作者把握不足，制作前须核对原始文献。
> - 文中数值（距离、时间、密度）均为**数量级参考值**，用于动画比例设定，不作为精确定量依据。

---

## 目录

0. [场景总览与空间坐标设定](#0-场景总览与空间坐标设定)
1. [第一部分：正常神经肌肉接头信号传递](#第一部分正常神经肌肉接头信号传递)
2. [第二部分：AChR 自身抗体的三条核心致病机制](#第二部分achr-自身抗体的三条核心致病机制)
3. [第三部分：MuSK-MG 与 AChR-MG 机制对比](#第三部分musk-mg-与-achr-mg-机制对比)
4. [第四部分：病理结局——从分子缺陷到临床表型](#第四部分病理结局从分子缺陷到临床表型)
5. [附录 A：PubMed 检索关键词清单](#附录-apubmed-检索关键词清单)
6. [附录 B：【需要文献验证】条目汇总](#附录-b需要文献验证条目汇总)

---

## 0. 场景总览与空间坐标设定

为便于动画建模，先统一定义神经肌肉接头（neuromuscular junction, NMJ）的三层空间结构（自上而下 = 神经 → 肌肉）：

| 层次 | 结构 | 关键空间特征（数量级） | 主要驻留分子 |
|---|---|---|---|
| 上层 | **突触前神经末梢**（presynaptic nerve terminal） | 运动神经元轴突末端膨大，内含大量突触小泡；末梢被施万细胞（终末施万细胞，terminal Schwann cell）覆盖 | 突触小泡、电压门控钙通道、SNARE 复合体、活性区（active zone） |
| 中层 | **突触间隙**（synaptic cleft） | 初级间隙宽约 50 nm；内有基底膜（basal lamina）；间隙沿突触后膜皱褶向下延伸形成次级间隙 | 乙酰胆碱酯酶、聚集蛋白（agrin）、基底膜胶原/层粘连蛋白 |
| 下层 | **突触后肌膜**（postsynaptic membrane，终板 endplate） | 肌膜内陷形成**突触后皱褶**（junctional folds），每个皱褶分为**嵴顶**（crest，朝向神经）与**谷底**（trough/depth） | 嵴顶：AChR 高密度簇集（约 10⁴ 个/μm²）+ 锚定蛋白 rapsyn；谷底：电压门控钠通道 Nav1.4 |

**动画布局建议**：
- 俯视剖面采用"上神经-中间隙-下肌膜"的纵向构图；突触后膜呈"梳齿状"皱褶，嵴顶与神经末梢活性区**上下对位**（活性区正对皱褶开口处）。
- AChR 着色集中在嵴顶，Nav1.4 着色集中在谷底——这一空间分区是理解第二、四部分"皱褶破坏 → 安全系数下降"的关键视觉锚点。

---

## 第一部分：正常神经肌肉接头信号传递

### 1.1 主要分子角色表（"演员表"）

| 分子 | 全称 / 缩写 | 位置 | 功能 |
|---|---|---|---|
| ACh | 乙酰胆碱（acetylcholine, ACh） | 合成于末梢胞质，储存于突触小泡 | 神经递质 |
| ChAT | 胆碱乙酰转移酶（choline acetyltransferase, ChAT） | 突触前胞质 | 由胆碱 + 乙酰辅酶 A 合成 ACh |
| VAChT | 囊泡乙酰胆碱转运体（vesicular acetylcholine transporter, VAChT） | 突触小泡膜 | 将 ACh 泵入小泡 |
| Cav2.1 | P/Q 型电压门控钙通道（voltage-gated calcium channel, VGCC；P/Q-type, Cav2.1） | 突触前膜活性区 | 去极化时开放，Ca²⁺ 内流 |
| SNARE | 可溶性 N-乙基马来酰亚胺敏感因子附着蛋白受体（soluble N-ethylmaleimide-sensitive factor attachment protein receptor, SNARE）：突触小泡蛋白（synaptobrevin / VAMP）、突触融合蛋白（syntaxin）、SNAP-25 | 小泡膜 + 突触前膜 | 介导小泡与质膜融合 |
| Syt | 突触结合蛋白（synaptotagmin, Syt） | 小泡膜 | Ca²⁺ 感受器，触发融合 |
| AChE | 乙酰胆碱酯酶（acetylcholinesterase, AChE） | 突触间隙基底膜，经胶原尾 ColQ 锚定 | 水解 ACh 为胆碱 + 乙酸 |
| AChR | 烟碱型乙酰胆碱受体（nicotinic acetylcholine receptor, nAChR；本文简称 AChR） | 突触后皱褶嵴顶 | 配体门控阳离子通道 |
| rapsyn | 受体相关突触蛋白（receptor-associated protein of the synapse, rapsyn） | 突触后膜胞质面 | 将 AChR 锚定、簇集于嵴顶，连接细胞骨架 |
| Nav1.4 | 骨骼肌型电压门控钠通道（voltage-gated sodium channel Nav1.4） | 皱褶谷底 | 将终板电位转换为肌肉动作电位 |
| CHT1 | 高亲和力胆碱转运体（high-affinity choline transporter 1, CHT1） | 突触前膜 | 回收胆碱 |
| DHPR / RyR1 | 二氢吡啶受体（dihydropyridine receptor, DHPR, Cav1.1）/ 1 型兰尼碱受体（ryanodine receptor 1, RyR1） | 横管（T 管）膜 / 肌质网膜 | 兴奋-收缩偶联 |

**AChR 结构要点（建模用）**：
- 成人型（终板型）AChR 为五聚体：**α1₂ β1 δ ε**（化学计量 2:1:1:1），五个亚基围成中央离子孔道，形似"漏斗/玫瑰花结"，胞外段向突触间隙伸出约 6 nm。
- 胎儿型 AChR 以 **γ 亚基** 取代 ε 亚基（α1₂ β1 γ δ）。
- **两个 ACh 结合位点**位于 α/ε 和 α/δ 亚基界面的胞外段；通常需两个位点均被占据，通道才高效开放。
- **主要免疫原区**（main immunogenic region, MIR）位于 α1 亚基胞外 N 端顶部（经典定位为 α1 第 67–76 位残基附近），远离 ACh 结合口袋，朝向间隙"顶端外侧"。此位置在第二部分中至关重要。

### 1.2 动态过程分镜（按时间顺序）

> 时间轴参考：从动作电位到达末梢至肌纤维动作电位产生，整体在**约 1–2 ms** 量级内完成（突触延搁约 0.5 ms）。

**镜头 1-1｜动作电位到达神经末梢**
- 位置：运动神经轴突 → 末梢膜。
- 过程：沿有髓轴突跳跃传导的动作电位（action potential, AP）抵达无髓的末梢，末梢膜去极化。

**镜头 1-2｜Ca²⁺ 内流**
- 位置：突触前膜活性区。
- 分子：Cav2.1。
- 过程：去极化 → Cav2.1 构象改变开放 → 胞外 Ca²⁺ 顺浓度梯度涌入，在活性区附近形成局部高钙"微域"（nanodomain）。

**镜头 1-3｜突触小泡融合与量子释放**
- 位置：活性区内已锚定（docked）、已预备（primed）的小泡。
- 分子：Syt 结合 Ca²⁺ → SNARE 复合体（VAMP + syntaxin + SNAP-25）"拉链式"完全组装 → 小泡膜与质膜融合，形成融合孔。
- 过程：每个小泡释放一个"量子"（quantum），约含 5,000–10,000 个 ACh 分子；一次神经冲动释放数十个量子（人类 NMJ 的量子含量约 20–50 量级 【需要文献验证：人类 NMJ 量子含量的具体数值因方法而异】）。

**镜头 1-4｜ACh 扩散穿越间隙**
- 位置：突触间隙（约 50 nm）。
- 过程：ACh 在微秒量级内扩散至突触后膜；部分 ACh 在途中即被间隙中的 AChE 水解（动画可表现为部分 ACh 分子"中途消失"）。

**镜头 1-5｜ACh 结合 AChR，通道开放**
- 位置：皱褶嵴顶。
- 分子：AChR。
- 过程：2 个 ACh 分子分别嵌入 α/ε 与 α/δ 界面口袋 → 跨膜 M2 螺旋旋转/外移，孔道"门"打开（开放时间约 1 ms 量级）→ 非选择性阳离子通透：**Na⁺ 内流为主**，K⁺ 少量外流（以及少量 Ca²⁺）。
- 结果：局部净内向电流，产生**终板电位**（endplate potential, EPP）。单个量子自发释放产生的小电位称为**微终板电位**（miniature endplate potential, MEPP）。

**镜头 1-6｜EPP 激活谷底 Nav1.4，产生肌肉动作电位**
- 位置：电流由嵴顶向下扩布至皱褶谷底。
- 分子：Nav1.4。
- 过程：EPP 使谷底膜电位越过 Nav1.4 激活阈值 → Nav1.4 开放 → 全或无的肌纤维 AP 产生，并沿肌膜向两侧传播。
- 关键概念——**安全系数**（safety factor, SF）：正常 EPP 幅度显著超过触发 AP 所需阈值（通常描述为数倍于阈值），保证在重复刺激、递质释放逐渐减少时仍能可靠触发 AP。皱褶结构通过（a）增大膜面积、（b）在谷底高密度富集 Nav1.4，进一步提高 SF。

**镜头 1-7｜兴奋-收缩偶联（可简化为过渡镜头）**
- 位置：肌膜 → 横管（T 管）→ 肌质网（sarcoplasmic reticulum, SR）。
- 过程：AP 沿 T 管深入 → DHPR 感受电压变化 → 机械偶联开启 RyR1 → SR 释放 Ca²⁺ → Ca²⁺ 结合肌钙蛋白 C（troponin C）→ 原肌球蛋白移位 → 肌球蛋白-肌动蛋白横桥循环 → 肌纤维收缩。

**镜头 1-8｜信号终止与递质回收**
- 位置：突触间隙（基底膜）+ 突触前膜。
- 分子：AChE（通过 ColQ 锚定于基底膜）、CHT1、ChAT、VAChT。
- 过程：AChE 将 ACh 水解为胆碱 + 乙酸 → 约半数胆碱经 CHT1 回收至末梢 【需要文献验证：回收比例】→ ChAT 重新合成 ACh → VAChT 将其装入小泡 → 小泡经内吞循环再生。AChR 因 ACh 移除而关闭，膜电位复极。

### 1.3 突触后结构的"维护系统"（为第三部分 MuSK 铺垫）

- 位置：突触后膜及基底膜。
- 分子与先后顺序：
  1. 神经末梢释放**神经源性聚集蛋白**（neural agrin，以下简称 agrin）进入基底膜；
  2. agrin 结合突触后膜上的**低密度脂蛋白受体相关蛋白 4**（low-density lipoprotein receptor-related protein 4, LRP4）；
  3. LRP4 与**肌肉特异性受体酪氨酸激酶**（muscle-specific receptor tyrosine kinase, MuSK）结合，促进 MuSK 二聚化与自磷酸化；
  4. 胞内衔接蛋白**下游酪氨酸激酶 7**（downstream of tyrosine kinase 7, Dok-7）进一步增强 MuSK 活化；
  5. 下游信号使 rapsyn 将 AChR 聚集、稳定于嵴顶。
- 此外，AChE 的胶原尾 ColQ 可与 MuSK（及基底膜成分）结合，参与 AChE 在突触处的定位。
- **动画要点**：这是一个**持续进行的维护过程**——AChR 不断被内吞降解、也不断被新合成并插入簇中（成熟终板 AChR 代谢半衰期约 1–2 周量级 【需要文献验证：人类数据有限，多来自啮齿类】）。

---

## 第二部分：AChR 自身抗体的三条核心致病机制

### 2.0 背景（简述，非动画主线）

- **流行病学定位**：约 80%–85% 的全身型重症肌无力（myasthenia gravis, MG）患者血清可检出抗 AChR 抗体；眼肌型中阳性率较低（约 50% 左右）【需要文献验证：不同人群与检测方法（放射免疫沉淀法 RIPA vs. 细胞基础检测 CBA）阳性率差异较大】。
- **抗体特征**：以 **IgG1 和 IgG3 亚类**为主——这两种亚类均为二价，且能高效激活补体，这一特性直接决定了下述机制 2 与机制 3。
- **抗原表位**：多数抗体针对 α1 亚基的 MIR；少数针对其他亚基或 ACh 结合区。
- **致病性证据（经典）**：患者 IgG 被动转移至小鼠可复制神经肌肉传递缺陷；血浆置换、新生儿 Fc 受体（neonatal Fc receptor, FcRn）拮抗剂降低致病 IgG 后症状改善；补体 C5 抑制剂有效。
- **自身免疫起源**：胸腺（thymus）被认为是早发型 AChR-MG 的重要起始部位——胸腺生发中心增生、胸腺肌样细胞（myoid cells）表达 AChR、胸腺瘤（thymoma）相关 MG 等。具体的免疫耐受破坏机制（如 T 滤泡辅助细胞、调节性 T 细胞功能异常的相对权重）仍在研究中 【需要文献验证】。本文稿聚焦于**效应阶段（抗体到达 NMJ 之后）**。

> **三条机制并非互斥**：同一患者体内三者通常并存，其相对贡献因患者、抗体谱而异。一般认为补体介导的损伤与抗原调变是主要机制，直接阻断作用较次要 【需要文献验证：三者相对权重的定量证据有限】。

---

### 2.1 机制一：阻断 ACh 与 AChR 结合（功能性阻断）

**分子是谁**：阻断型抗 AChR 抗体（blocking antibodies），表位位于或邻近 α 亚基的 ACh 结合口袋（即 α/ε、α/δ 界面附近的胞外区域）。

**在哪里**：突触间隙 → 嵴顶 AChR 胞外段的 ACh 结合区。

**动态过程（分镜）**：

| 序号 | 位置 | 发生了什么 |
|---|---|---|
| 2.1-1 | 肌内毛细血管 → 间质 → 突触间隙 | 循环中 IgG 渗出血管，经间质扩散，进入突触间隙（基底膜对 IgG 通透） |
| 2.1-2 | 嵴顶 AChR 胞外段 | 阻断型抗体的 Fab 段结合于 ACh 结合位点附近，**空间占位**或诱导**构象改变** |
| 2.1-3 | 同上 | 神经冲动释放的 ACh 到达后，无法嵌入被占据/变形的结合口袋 |
| 2.1-4 | 突触后膜 | 受体在**数量上未减少、膜结构完整**，但可被激活的"功能性 AChR"减少 → 通道开放总数下降 → MEPP 和 EPP 幅度减小 |

**动画表现建议**：AChR 本体保持原位、颜色不变，但其"钥匙孔"被抗体"挡板"盖住；ACh 小球撞上后弹开。这是三种机制中**唯一不破坏受体与膜结构**的机制，因此作用可**较快出现、也可较快逆转**。

**要点与争议**：
- 在多数患者中，阻断型抗体仅占总抗 AChR 抗体的一小部分 【需要文献验证：比例】。
- 有报道认为高滴度阻断型抗体可能与急性、重度无力相关 【需要文献验证】。
- 临床常规 RIPA 检测的是"结合型"抗体，不能区分阻断性；阻断抗体需专门检测。

---

### 2.2 机制二：AChR 交联、加速内吞与溶酶体降解（抗原调变，antigenic modulation）

**分子是谁**：二价 IgG（主要为 IgG1/IgG3），多为 MIR 特异性抗体。

**在哪里**：嵴顶 AChR 簇 → 突触后膜胞内侧内吞小泡 → 肌纤维胞内内体/溶酶体系统。

**结构前提**：
- 一个 IgG 有两个 Fab 臂，可同时结合两个 AChR 分子上的 MIR。
- AChR 在嵴顶排列极为致密，相邻受体间距适合被一个 IgG"桥接"。
- 一般认为，IgG 难以同时结合**同一个** AChR 上的两个 α 亚基 MIR，因此倾向于**分子间交联**（桥接相邻受体） 【需要文献验证：基于结构模型推断】。

**动态过程（分镜）**：

| 序号 | 位置 | 发生了什么 |
|---|---|---|
| 2.2-1 | 突触间隙 → 嵴顶 | 二价 IgG 的一个 Fab 臂先结合受体 A 的 α1-MIR |
| 2.2-2 | 嵴顶 | 另一 Fab 臂结合相邻受体 B 的 α1-MIR，形成 AChR–IgG–AChR 桥；多个 IgG 进一步连接，形成**二维交联网格/微聚集** |
| 2.2-3 | 突触后膜胞内面 | 交联的受体簇被识别为内吞对象，膜向胞内内陷形成内吞小泡（内吞途径的具体分子，如是否依赖网格蛋白，【需要文献验证】） |
| 2.2-4 | 胞质 → 早期内体 → 晚期内体/溶酶体 | 内吞小泡与内体融合，最终进入溶酶体，AChR 与结合的抗体一同被蛋白酶降解 |
| 2.2-5 | 肌核 / 内质网 / 高尔基体 → 突触后膜 | 肌纤维代偿性上调 AChR 合成并插入膜中，但**插入速率不足以抵消加速的降解** |
| 2.2-6 | 嵴顶 | 净结果：嵴顶 AChR **数量下降**；体外/动物研究中，抗体可使 AChR 降解速率提高约 2–3 倍 【需要文献验证：具体倍数】 |

**关键对照实验（可作为动画旁白/字幕）**：
- 用单价 Fab 片段（只有一个结合臂）替代完整 IgG，不能加速 AChR 降解 → 证明**交联是必要条件**。
- 抗原调变**不依赖补体**。

**动画表现建议**：用"手拉手"的抗体把两个 AChR"铐"在一起，随后膜面下凹、整团被"吞"入胞内，再被溶酶体（酸性小囊泡，可用不同色调表示）"消化"。同时用一条较细的箭头表示新合成 AChR 从高尔基体输送到膜上，速度明显慢于降解，形成"入不敷出"的视觉对比。

---

### 2.3 机制三：经典补体途径激活，破坏突触后膜（补体介导的损伤）

**分子是谁**：
- 补体固定型 IgG（IgG1、IgG3）
- 经典途径补体成分：C1（C1q + C1r + C1s）、C4、C2、C3、C5、C6、C7、C8、C9
- 终产物：**膜攻击复合物**（membrane attack complex, MAC；即 C5b-9）
- 膜表面补体调节蛋白：**衰变加速因子**（decay-accelerating factor, DAF / CD55）、**膜辅助蛋白**（membrane cofactor protein, MCP / CD46）、**CD59**（protectin，抑制 C9 聚合）

**在哪里**：主要发生在突触后皱褶**嵴顶**（抗体结合最密集处），破坏向皱褶深部延伸。

**动态过程（分镜）**：

| 序号 | 位置 | 发生了什么 |
|---|---|---|
| 2.3-1 | 嵴顶 AChR 簇表面 | 大量 IgG1/IgG3 结合于密集排列的 AChR 上，其 **Fc 段朝向突触间隙**，彼此靠近 |
| 2.3-2 | IgG Fc 簇 | C1q 的多个球状头部同时结合**多个邻近 IgG 的 Fc 段**（C1q 需多价结合才能被有效激活；IgG Fc 形成六聚体平台的模型 【需要文献验证：在 NMJ 原位是否成立】） |
| 2.3-3 | C1 复合物内 | C1q 构象变化 → 激活 C1r → C1r 剪切活化 C1s |
| 2.3-4 | 膜表面 | C1s 裂解 C4 → C4b 共价附着于膜/抗体；C1s 裂解结合于 C4b 的 C2 → 形成**经典途径 C3 转化酶** C4b2a（新命名法中写作 C4b2b） |
| 2.3-5 | 膜表面 | C3 转化酶大量裂解 C3 → C3b 沉积于突触后膜（放大环节），C3a 释放入液相 |
| 2.3-6 | 膜表面 | C3b 加入形成 **C5 转化酶**（C4b2a3b）→ 裂解 C5 → C5a 释放，C5b 留于膜旁 |
| 2.3-7 | 突触后膜脂质双层 | C5b 依次结合 C6、C7（C5b-7 插入膜）、C8（初步穿膜），再招募多个 C9 分子聚合成环状孔道 → **MAC（C5b-9）** 形成 |
| 2.3-8 | 嵴顶膜 | MAC 孔道导致局部膜完整性破坏、离子失衡（包括 Ca²⁺ 内流）→ 局灶性膜损伤 |
| 2.3-9 | 嵴顶 → 突触间隙 | 含 AChR 的突触后膜碎片**脱落（shedding）进入突触间隙**；电镜下可见间隙中含 IgG、C3、MAC 的膜碎片 |
| 2.3-10 | 整个突触后区 | 结构重塑：**皱褶变浅、变少、简化**；**突触间隙增宽**；AChR 密度显著下降；位于谷底的 Nav1.4 也随皱褶丢失而减少 |

**补体调节蛋白（保护性"刹车"）的空间表现**：
- CD55、CD46、CD59 锚定于肌膜，分别在 C3/C5 转化酶层面和 MAC 形成层面抑制补体级联。
- 在动物模型中，敲除这些调节蛋白可加重实验性自身免疫性 MG 的损伤 → 说明局部补体调节能力影响损伤程度。
- 不同肌肉（如眼外肌）补体调节蛋白表达水平可能较低，被提出作为眼肌易受累的一种解释 【需要文献验证】。

**临床旁证（可用于动画结尾字幕）**：
- 抑制 C5 裂解的单克隆抗体（如依库珠单抗 eculizumab、雷夫利珠单抗 ravulizumab）及 C5 抑制性多肽（如 zilucoplan）对 AChR-MG 有效，支持补体在 AChR-MG 中的致病地位。

**动画表现建议**：
1. 镜头从单个 IgG 拉远到"抗体森林"覆盖嵴顶；
2. C1q 如"六爪"般抓住多个 Fc；
3. 级联放大用颜色扩散/粒子爆发表现（C3b 大量沉积为关键的"放大时刻"）；
4. MAC 以"环状钻孔"插入膜，局部膜出现孔洞、起泡；
5. 含 AChR 的膜片"剥落"漂入间隙；
6. 最后切换为**前后对比**：正常深而密的梳齿状皱褶 vs. 浅平、稀疏的简化皱褶，间隙变宽。

---

### 2.4 三条机制对照小结

| 维度 | 机制一：阻断 | 机制二：交联内化 | 机制三：补体破坏 |
|---|---|---|---|
| 关键抗体特性 | 表位邻近 ACh 结合位点 | 二价（可交联）；多为 MIR 抗体 | Fc 可固定补体（IgG1/IgG3）；多为 MIR 抗体 |
| 是否需补体 | 否 | 否 | 是 |
| AChR 数量 | 不减少（功能失活） | 减少（降解加速） | 减少（随膜碎片脱落） |
| 膜/皱褶结构 | 完整 | 基本完整 | **破坏、简化**；间隙增宽 |
| Nav1.4 | 不受影响 | 基本不受影响 | 随皱褶丢失而减少 |
| 时间尺度（相对） | 快速出现/快速逆转 | 中等（取决于受体周转） | 损伤较持久，修复需结构重建 |
| 一般认为的重要性 | 多数患者较次要 【需要文献验证】 | 重要 | 被认为最主要 【需要文献验证】 |

---

## 第三部分：MuSK-MG 与 AChR-MG 机制对比

### 3.1 MuSK-MG 的分子过程（简要分镜）

**背景**：抗 MuSK 抗体阳性 MG（MuSK-MG）见于部分 AChR 抗体阴性的全身型患者，占 MG 总体的少数（比例存在显著地域和种族差异 【需要文献验证】）。

| 序号 | 位置 | 发生了什么 |
|---|---|---|
| 3.1-1 | 突触间隙 → 突触后膜 MuSK 胞外段 | 抗 MuSK 抗体（以 **IgG4** 为主）结合 MuSK 胞外区，主要表位位于第一个免疫球蛋白样结构域（Ig-like domain 1） |
| 3.1-2 | MuSK–LRP4 界面 | 抗体干扰 MuSK 与 LRP4 的相互作用 → agrin-LRP4 无法有效激活 MuSK |
| 3.1-3 | 突触后膜胞质面 | MuSK 磷酸化下降 → 下游维持信号减弱 → rapsyn 介导的 AChR 簇集稳定性下降 |
| 3.1-4 | 嵴顶 | AChR 簇**分散、变小**，单位面积功能性 AChR 减少 |
| 3.1-5 | 基底膜 | 抗体可能干扰 MuSK 与 ColQ 的结合，影响 AChE 在突触处的锚定 【需要文献验证：人类疾病中的意义尚不明确】 |
| 3.1-6 | 突触前 | 动物模型中观察到突触前代偿性释放增加不足等改变 【需要文献验证】 |

**IgG4 的特殊性（动画建模关键）**：
- IgG4 可发生 **Fab 臂交换**（Fab-arm exchange）：两条"半抗体"与其他 IgG4 分子交换，形成两个 Fab 识别不同抗原的**双特异、功能性单价**抗体 → **难以交联** MuSK。
- IgG4 **几乎不激活经典补体途径**。
- 因此 MuSK-MG 的主要机制是**干扰信号通路（功能性阻断）**，而非交联内化或补体攻击。

### 3.2 对比表

| 维度 | AChR-MG | MuSK-MG |
|---|---|---|
| 靶抗原 | AChR（主要为 α1 亚基 MIR） | MuSK（主要为 Ig 样结构域 1） |
| 主要 IgG 亚类 | IgG1、IgG3 | IgG4（亦可检出少量其他亚类） |
| 抗体价态 | 二价 → 可交联 | IgG4 经 Fab 臂交换后功能性单价 → 基本不交联 |
| 补体激活 | 强，核心机制 | 极弱/可忽略 |
| 核心致病方式 | 阻断 + 交联内化 + 补体破坏 | 阻断 MuSK–LRP4 信号 → AChR 簇集维持障碍 |
| 突触后皱褶结构 | 补体破坏导致简化、碎片化 | 一般无明显补体性破坏，表现为 AChR 簇减少/分散 【需要文献验证：人体活检资料有限】 |
| 胸腺病理 | 常见胸腺增生或胸腺瘤 | 通常无明显胸腺异常 |
| 临床偏好 | 眼肌、肢体、延髓肌均可受累 | 常以延髓、面部、颈部、呼吸肌受累突出，可伴肌萎缩 |
| 治疗反应差异（机制相关） | 补体抑制剂、FcRn 拮抗剂有效；胸腺切除对部分患者获益 | 抗 CD20（利妥昔单抗 rituximab）常有较好反应；胆碱酯酶抑制剂反应常较差甚至不耐受；补体抑制剂理论上不适用 |

**动画对比建议**：并列分屏——左侧 AChR-MG 为"抗体攻击受体本身 + 补体破坏膜"，右侧 MuSK-MG 为"抗体切断维护信号 → AChR 簇逐渐散开"。右侧的视觉核心是"维护失效、慢慢瓦解"，而非"直接破坏"。

> 补充：另有抗 LRP4 抗体阳性 MG，其机制同样涉及 agrin-LRP4-MuSK 通路，但抗体亚类与致病性证据仍在积累 【需要文献验证】。本文稿不展开。

---

## 第四部分：病理结局——从分子缺陷到临床表型

### 4.1 因果链总览

```
抗 AChR 抗体（IgG1/IgG3）
   ├─ 阻断 ACh 结合 ──────────┐
   ├─ 交联 → 内吞 → 降解 ──────┼─→ 功能性 AChR 数量↓
   └─ 补体 → MAC → 膜破坏 ─────┤        ＋ 皱褶简化 / Nav1.4↓ / 间隙增宽
                               ↓
                 MEPP 与 EPP 幅度↓（量子大小↓；量子释放基本正常）
                               ↓
                  安全系数（SF）↓ → EPP 更接近/低于阈值
                               ↓
          部分肌纤维传递失败（"阻滞"）→ 参与收缩的肌纤维数↓
                               ↓
                      肌肉收缩力↓ = 肌无力
                               ↓
         重复活动 → 递质释放生理性递减 → 更多纤维失败 → 病理性易疲劳
```

### 4.2 逐级解释（附动画分镜）

**镜头 4-1｜量子大小下降，而非释放减少**
- 位置：突触后膜。
- AChR-MG 的原发缺陷在**突触后**：每个量子的 ACh 数量正常，但可被结合并开放的 AChR 减少 → 单个量子产生的电流减小（MEPP 幅度降低）。
- 突触前每次冲动释放的量子数基本正常，甚至可有代偿性增加 【需要文献验证】。
- 动画：同样数量的 ACh 落到膜上，但只有少数 AChR"亮起"。

**镜头 4-2｜安全系数下降**
- EPP = 量子含量 × 量子大小。量子大小下降 → EPP 下降。
- 补体破坏还使谷底 Nav1.4 减少 → **AP 阈值升高**，加剧 SF 下降（"双重打击"：电位变小 + 门槛变高）。
- 间隙增宽可能使 ACh 在到达受体前更多被水解/扩散流失 【需要文献验证：对人类 NMJ 的定量贡献】。
- 动画：用"水位线（EPP）"与"堤坝（阈值）"比喻——正常时水位远高于堤坝；MG 时水位下降、堤坝升高，二者接近。

**镜头 4-3｜单纤维水平：全或无的传递失败**
- 一个运动单位内各肌纤维 NMJ 受损程度不一。
- 当某纤维 EPP 低于阈值 → 该纤维本次不产生 AP → 不收缩（神经肌肉**阻滞**，blocking）。
- 接近阈值的纤维，EPP 到达阈值所需时间不稳定 → 单纤维肌电图（single-fiber electromyography, SFEMG）上的**颤抖**（jitter）增大。
- 动画：同一运动单位中，部分肌纤维"闪烁"、部分"熄灭"。

**镜头 4-4｜整块肌肉水平：收缩力下降**
- 参与收缩的肌纤维总数减少 → 整块肌肉产生的力减少 → 临床表现为肌无力。
- 复合肌肉动作电位（compound muscle action potential, CMAP）为所有被成功激活肌纤维 AP 的总和。

### 4.3 症状波动性（易疲劳性）的机制对应

| 临床现象 | 分子/生理基础 | 动画建议 |
|---|---|---|
| **持续或重复用力后无力加重（病理性易疲劳）** | 重复神经刺激时，突触前可立即释放的小泡池逐渐耗竭，量子含量在最初数次冲动内生理性递减。正常 NMJ 因 SF 充足而不受影响；MG 中 SF 已降低，递减使越来越多纤维 EPP 跌破阈值 | 连续发放动画：每次冲动 ACh"雨"逐渐变稀，亮起的肌纤维越来越少 |
| **休息后好转** | 休息使小泡池补充，量子含量恢复 | 暂停后小泡重新充满，纤维重新亮起 |
| **低频重复神经刺激（repetitive nerve stimulation, RNS）递减** | 常用 2–5 Hz（多为 3 Hz）刺激，第 1 至第 4/5 个 CMAP 幅度递减 >10% 被视为异常；即上述机制的电生理体现 | 用 CMAP 波形逐个变矮的示波器画面 |
| **一日之内晨轻暮重** | 日间持续活动累积疲劳 【需要文献验证：是否存在独立的昼夜节律因素尚不明确】 | 时间轴叠加 |
| **体温升高时加重、局部冷却时改善**（冰袋试验） | 低温降低 AChE 活性，使 ACh 在间隙停留更久，可能还有其他机制参与 【需要文献验证】 | 冰袋场景下 AChE 动作放慢 |
| **胆碱酯酶抑制剂（如溴吡斯的明 pyridostigmine）可暂时改善** | 抑制 AChE → ACh 在间隙停留时间延长、可多次结合剩余 AChR → EPP 部分恢复 | AChE"剪刀"被锁住，ACh 停留更久 |
| **较长时间尺度的病情波动（数日至数月）** | 抗体水平变化、感染等免疫触发、某些药物（如部分抗生素、镁剂等）降低 SF、补体损伤与修复的动态平衡 | 可作片尾文字说明 |
| **眼外肌易受累** | 可能与眼外肌高放电频率、SF 本身较低、皱褶较少、补体调节蛋白表达较低、部分纤维表达胎儿型 AChR 等有关 【需要文献验证：多为假说性解释，各因素权重未定】 | 可选：并列眼外肌与肢体肌 NMJ |

### 4.4 一句话总结（适合作为动画结尾字幕）

> AChR-MG 是一种以突触后膜为靶点的抗体介导自身免疫病：IgG1/IgG3 抗 AChR 抗体通过**阻断、交联降解和补体破坏**三条途径减少功能性 AChR 并破坏突触后皱褶结构，使终板电位与安全系数下降；在重复活动导致递质释放生理性递减时，越来越多肌纤维传递失败，从而表现为**可波动的、活动后加重、休息后缓解的骨骼肌无力**。

---

## 附录 A：PubMed 检索关键词清单

> 使用建议：将 MeSH 主题词与自由词组合；可附加过滤器 `Review[pt]`、近 10 年、`humans` / `animals`。示例语法见每组末行。

### A1. 正常 NMJ 生理
- `"Neuromuscular Junction"[MeSH] AND physiology`
- `"Receptors, Nicotinic"[MeSH] AND structure` ；`muscle-type nicotinic acetylcholine receptor cryo-EM structure`
- `neuromuscular transmission safety factor`
- `quantal content human neuromuscular junction`
- `junctional folds voltage-gated sodium channel Nav1.4 endplate`
- `acetylcholinesterase ColQ anchoring basal lamina`
- `agrin LRP4 MuSK Dok-7 rapsyn acetylcholine receptor clustering`
- `acetylcholine receptor turnover half-life endplate`

### A2. AChR 抗体致病机制
- `"Myasthenia Gravis"[MeSH] AND "Autoantibodies"[MeSH] AND pathogenesis`
- `main immunogenic region acetylcholine receptor alpha subunit`
- `acetylcholine receptor antibody antigenic modulation cross-linking degradation`
- `blocking antibodies acetylcholine receptor myasthenia gravis`
- `complement membrane attack complex neuromuscular junction myasthenia gravis`
- `C5b-9 endplate electron microscopy myasthenia gravis`
- `CD55 CD59 decay accelerating factor experimental autoimmune myasthenia gravis`
- `IgG1 IgG3 subclass acetylcholine receptor antibodies`
- `passive transfer myasthenia gravis IgG mice`
- `"Myasthenia Gravis, Autoimmune, Experimental"[MeSH]`
- 示例：`("Myasthenia Gravis"[MeSH]) AND (complement OR "antigenic modulation" OR "blocking antibodies") AND Review[pt]`

### A3. 免疫起源（背景核对）
- `thymus myasthenia gravis germinal center myoid cells`
- `thymoma associated myasthenia gravis pathogenesis`
- `T follicular helper cells regulatory T cells myasthenia gravis`

### A4. MuSK-MG 与其他亚型
- `MuSK antibody myasthenia gravis IgG4 Fab-arm exchange`
- `MuSK LRP4 interaction anti-MuSK antibodies Ig-like domain`
- `MuSK ColQ acetylcholinesterase anchoring antibodies`
- `LRP4 antibody myasthenia gravis`
- `seronegative myasthenia gravis cell-based assay clustered AChR`
- `rituximab MuSK myasthenia gravis`

### A5. 病理生理与临床对应
- `repetitive nerve stimulation decrement myasthenia gravis mechanism`
- `single fiber electromyography jitter blocking myasthenia gravis`
- `miniature endplate potential amplitude myasthenia gravis`
- `extraocular muscle susceptibility myasthenia gravis`
- `ice pack test myasthenia gravis acetylcholinesterase temperature`
- `fatigability myasthenia gravis safety factor`

### A6. 机制相关治疗旁证
- `eculizumab OR ravulizumab OR zilucoplan generalized myasthenia gravis`
- `efgartigimod OR rozanolixizumab FcRn myasthenia gravis`
- `complement inhibitor acetylcholine receptor antibody positive myasthenia gravis trial`

---

## 附录 B：【需要文献验证】条目汇总

| # | 位置 | 待核对内容 |
|---|---|---|
| 1 | 1.2 镜头 1-3 | 人类 NMJ 量子含量具体数值 |
| 2 | 1.2 镜头 1-8 | 胆碱经 CHT1 回收的比例 |
| 3 | 1.3 | 人类终板 AChR 代谢半衰期 |
| 4 | 2.0 | AChR 抗体在全身型/眼肌型中的阳性率（随检测方法变化） |
| 5 | 2.0 | 胸腺内耐受破坏的细胞机制权重 |
| 6 | 2.0 / 2.4 | 三条致病机制的相对贡献 |
| 7 | 2.1 | 阻断型抗体所占比例及其与急性重症的关联 |
| 8 | 2.2 | IgG 不能结合同一 AChR 两个 MIR 的结构依据 |
| 9 | 2.2 | 交联 AChR 内吞的具体分子途径 |
| 10 | 2.2 | 抗体加速 AChR 降解的倍数 |
| 11 | 2.3 | IgG Fc 六聚体平台模型在 NMJ 原位是否适用 |
| 12 | 2.3 / 4.3 | 眼外肌补体调节蛋白低表达假说 |
| 13 | 3.1 | MuSK-MG 在不同人群中的比例 |
| 14 | 3.1 | 抗 MuSK 抗体干扰 ColQ 结合的人类疾病意义 |
| 15 | 3.1 | MuSK-MG 突触前代偿不足（动物模型证据外推） |
| 16 | 3.2 | MuSK-MG 人类 NMJ 超微结构资料 |
| 17 | 3.2 补充 | LRP4 抗体致病性证据 |
| 18 | 4.2 | AChR-MG 中突触前量子释放的代偿性改变 |
| 19 | 4.2 | 突触间隙增宽对 ACh 有效浓度的定量影响 |
| 20 | 4.3 | 晨轻暮重是否存在独立的昼夜节律机制 |
| 21 | 4.3 | 冰袋试验改善的完整机制 |
| 22 | 4.3 | 眼外肌易感性的各假说权重 |

---

*免责声明：本文稿为科研与教学用途的机制梳理初稿，不构成临床诊疗建议。所有数值与带标注的内容在用于正式出版或动画发布前，须对照原始文献与最新综述核实。*
