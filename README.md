# Robo Education Recruitment

苏筱蕙（Victoria Mitsu）的机器人协会教学部纳新资料。

主题：**Python + OpenCV 视觉巡线入门：黑线在画面的哪一边？**

本仓库包含完整内训方案、约 10 分钟的授课 Demo，以及可复现的图像实验。基础环节在电脑上完成，不要求学员预先拥有机器人硬件。

## 目录

```text
topic/内训选题.md          4.5.1 完整内训方案
slides/                   4.5.2 可编辑课件、PDF 与讲稿
demo/                     参考实现、样例生成脚本、学员练习
assets/samples/           明确标注为合成数据的教学图片
tests/                    自动化逻辑检查
results/                  本次实际运行记录
requirements.txt          经过本次运行验证的依赖版本
README.md                 使用与协作说明
```

## 快速开始

推荐使用 Python 3.12；本仓库固定的 NumPy 版本要求 Python 至少为 3.11。本次实际验证使用 Python 3.12.14。在本目录执行：

```sh
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# macOS / Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python demo/check_environment.py
python demo/make_samples.py
python demo/line_detector.py --image assets/samples/right.png --output results/local/right
python -m unittest discover -s tests -v
```

程序将掩膜、标注图与 JSON 结果保存到输出目录，无须开启图形窗口。只安装 requirements 中的一种 OpenCV 包，避免多个包共用 `cv2` 名称导致冲突。

`demo/worksheet.py` 是有意保留填空的课堂练习，完整参考实现位于 `demo/line_detector.py`。

## 完成情况与边界

方案设计为两次 90 分钟内训，Demo 的逐页讲稿合计 10 分钟。代码提供正常、丢线、多候选、阴影和阈值失配案例，测试与运行记录见 `results/`。

本次验证使用合成教学图片，没有将其描述为真实摄像头数据或实车效果。课程中的左右方向依赖图像未镜像且与车体方向一致。当前程序只输出位置和方向建议，不控制电机，也未完成真实环境鲁棒性验证。

资料已整理至本公开仓库，完成远程创建、clone、add、commit 与 push，并通过 [Pull Request #1](https://github.com/victoriamitsu28/Robo-Education-Recruitment/pull/1) 合并了课前环境检查改进。实际操作与提交记录见 [results/git-workflow.md](results/git-workflow.md)。

## 4.5.3 Git 与 GitHub 操作说明

### 使用的功能

使用 Git 跟踪课程资料，将内训方案、课件与代码、环境检查改进分别提交；完成 GitHub 远程仓库创建、clone、add、commit、push、分支与 Pull Request 合并。提交历史保留了实际内容的变化，未将全部材料压成一次提交。操作记录见 `results/git-workflow.md`。

### 遇到的问题与处理

本地初始环境未安装 OpenCV，因此将验证依赖放在项目专用目录，保留已有运行环境，并记录实际运行版本。检查依赖元数据时发现，固定的 NumPy 2.3.5 要求 Python 至少为 3.11，因此修正了原先过宽的 Python 版本建议，并补充课前环境检查程序。代码将结果保存为文件，避免 headless 版本不提供窗口显示功能的问题。

Git 认证最初在非交互模式下没有输出，改用交互终端完成设备授权。随后 Git 的 HTTPS 连接停滞，而系统网络请求正常；检查发现 Git 没有自动采用 Windows 的现有代理，为本次 Git 命令指定该代理后完成 clone 和 push，没有改变全局代理设置。认证信息未写入仓库。

### 多人维护建议

方案、课件、代码和图片分别存放，README 保留入口与复现命令。每次修改先开分支，说明教学目标或修复问题，通过 Pull Request 提交。至少一位成员检查内容准确性、运行示例并确认 PPT 与 PDF 一致后再合并。依赖升级与内容修改分开提交，较大二进制文件避免频繁重命名。每次内训后将问题整理为 Issue，附环境、操作步骤和期望结果。

### 工具使用与检查

本次使用 Codex 辅助组织方案、编写代码、制作课件与整理资料。检查包括核对 OpenCV 官方文档、运行正常和异常输入测试、检查方向和偏差公式、逐页查看导出课件，并区分已经验证的合成数据结果与尚未开展的实车实验。具体检查记录保存在 `results/`。提交前仍需由申请人熟悉代码和讲稿，并确认其中的教学安排符合本人意愿。

## 资料来源

- [OpenCV 反向二值化](https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html)
- [OpenCV 轮廓基础](https://docs.opencv.org/4.x/d4/d73/tutorial_py_contours_begin.html)
- [OpenCV 轮廓矩与质心](https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html)
- [OpenCV Python 包说明](https://pypi.org/project/opencv-python-headless/)

教学示意图、合成样例、教学流程与练习按本课程目标设计，未使用外部人物照片或竞赛图片。
