
# 计算机视觉

本代码将在 2022-04-30 开源于 [GitHub](https://github.com/YiqunChen1999/course-computer-vision).

## 运行环境

本代码已在 Ubuntu 20.04 (含 Windows Subsystem Linux 2, WSL 2) 以及 Windows 11 (Windows Powershell) 下通过测试, 实验报告中实验部分在 Ubuntu 平台上完成.

## 文件说明

本项目代码按照以下方式组织:

```txt
cv # 项目根目录
|_ configs
    |_ default.yml
|_ cv
    |_ configs
        |_ default.py
        |_ ...
    |_ ops
        |_ hist.py
        |_ ...
    |_ task
        |_ segmentation.py
        |_ ...
    |_ utilities
        |_ configs.py
        |_ env.py
        |_ registry.py
        |_ utils.py
        |_ ...
    |_ main.py
|_ images
    |_ coins.png
    |_ ...
|_ results
    |_ coins.png
    |_ ...
|_ test
    |_ utilities
        |_ test_configs.py
        |_ ...
    |_ ...
|_ .gitignore
|_ compile.sh
|_ README.md
|_ requirements.txt
|_ run.sh
|_ main.exe
|_ 实验报告.pdf
|_ setup.py
```

源代码、README.md 文件、可执行文件 (`main.exe`) 以及实验报告均位于根目录下, 其中：

- `cv/configs` 下存储着可修改的配置文件;
- `cv/cv` 文件夹存储着程序源代码;
- `cv/images` 下存储着待处理图像 (`cv/coins.png` 也是待处理图像, 程序可自动识别 `cv` 下以及 `cv/images` 下的待处理图片);
- `cv/results` 下存储着处理完毕的图像, 它们的文件命名方式为 `NAME_segmentation_METHOD.png/jpg`, 其中 NAME 是原本图片的文件名;
- `METHOD` 是使用的图像分割算法 (如 `meanshift`);
- `cv/test` 下存储着代码开发过程中的单元测试代码;
- `cv/logs` 下存储着程序运行时的日志;
- `cv/compile.sh` 为编译可执行文件的脚本;
- `cv/setup.py` 为开发过程中的安装脚本;
- `cv/run.sh` 为开发过程中运行代码的脚本.

## 输入图像

程序会自动查找 `main.exe` 同级目录下的图片并进行处理, 但为了保持文件夹的整洁性, 建议将图像放置于 `cv/images` 之下, 代码运行结果将保存于 `cv/results` 之下, 避免因产生结果过多导致文件夹混乱不堪. 当前已经实现的算法为Mean Shift 分割算法, 默认任务为 `segmentation`, 若需要增加或者修改任务, 请在 `cv/cv/configs/default.py` 中的 `configs.general.tasks` 修改.

## 运行程序

请进入项目根目录, 并在 Linux 终端下运行:

```bash
./main.exe [-h] [--id ID] [--speedup] [--parallel] [--workers WORKERS]
```

参数说明：

1. `--id`: 默认为 `deploy`, 指运行本次实验时的唯一标识符, 若已有同名标识符, 则原本的内容会被覆盖;
2. `--speedup`: 是否开启基于聚类中心合并的加速方法, 默认为否, 该设置无法与 `--parallel` 同时生效, 后者的优先级高于此选项;
3. `--parallel`: 是否开启基于并行计算的加速方法, 默认为否, 该设置无法与 `--speedup` 同时生效, 本选项优先级更高;
4. `--workers`: 当使用基于并行计算的加速方法时, 使用的 CPU 数目, 若不指定, 则默认为机器上所有的 CPU 数目;
5. `-h`: 展示帮助信息.

## 更改默认设置

如果需要修改默认设置, 请修改 `cv/configs/default.yml`, 注意, 运行可执行文件 `cv/main.exe` 时, 修改 `cv/cv/configs/configs.py` 的配置不会对该可执行文件生效.

**注意**: 关于设置的优先级: `cv/configs/default.yml` 的优先级高于 `cv/cv/configs/configs.py`, 因为后者仅用于设置某些具有执行逻辑的配置.

**警告**: 请仅在清楚自己的修改会带来的后果时修改默认配置.

## 重新编译

如果需要修改配置, 创建一个虚拟环境并运行 `./run.sh`, 然后修改 `cv/cv/configs/default.py` 中的文件, 之后可以直接在**根目录下**运行 `python cv/main.py`, 或者在**根目录**下通过 `./compile.sh` (Linux 平台, Windows 平台可参考 `./compile.sh` 中的编译命令) 编译可执行文件并运行 `./main.exe` 文件.

**注意**: 如需要编译可执行文件, 请按照 [pyinstaller]([https://](https://pyinstaller.readthedocs.io/en/stable/installation.html)) 的说明安装相应的软件包.

**注意**: 如果需要重新编译, 建议创建一个新的环境, 并使用 `pip` 安装所有依赖, 如: `pip install -r requirements.txt`, 避免生成的可执行文件过大. **请勿安装非必要的包**
