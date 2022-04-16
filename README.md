
# 计算机视觉

## 代码说明

本项目代码按照以下方式组织:

```txt
cv # 项目根目录
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
|_ README.md
|_ requirements.txt
|_ run.sh
|_ main
```

## 输入图像

尽管程序也会自动查找 `run.sh` 同级目录下的图片并进行处理, 但为了保持文件夹的整洁性, 建议将图像放置于 `cv/images` 之下, 代码运行结果将保存于 `cv/results` 之下, 避免因产生结果过多导致文件夹混乱不堪. 当前已经实现的算法为阈值分割算法, 默认任务为 `segmentation`, 若需要增加或者修改任务, 请在 `cv/cv/configs/default.py` 中的 `configs.general.tasks` 修改.

## 运行程序

请进入项目根目录, 并在 Linux 终端下运行:

```bash
main [-h] [--id ID] [--speedup] [--parallel] [--workers WORKERS]
```

参数说明：

1. `--id`: 默认为 `deploy`, 指运行本次实验时的唯一标识符, 若已有同名标识符, 则原本的内容会被覆盖;
2. `--speedup`: 是否开启基于聚类中心合并的加速方法, 默认为否, 该设置无法与 `--parallel` 同时生效, 后者的优先级高于此选项;
3. `--parallel`: 是否开启基于并行计算的加速方法, 默认为否, 该设置无法与 `--speedup` 同时生效, 本选项优先级更高;
4. `--workers`: 当使用基于并行计算的加速方法时, 使用的 CPU 数目, 若不指定, 则默认为机器上所有的 CPU 数目;

## 更改默认设置

如果需要修改默认设置, 请修改 `cv/configs/default.yml`, 注意, 运行可执行文件 `cv/main` 时, 修改 `cv/cv/configs/configs.py` 的配置不会对该可执行文件生效.

**注意**: 关于设置的优先级: `cv/configs/default.yml` 的优先级高于 `cv/cv/configs/configs.py`, 因为后者仅用于设置某些具有执行逻辑的配置.

**警告**: 请仅在清楚自己的修改会带来的后果时修改默认配置.

## 重新编译

如果需要修改配置, 创建一个虚拟环境并运行 `./run.sh`, 然后修改 `cv/cv/configs/default.py` 中的文件, 之后可以直接在**根目录下**运行 `python cv/main.py`, 或者在**根目录**下通过 `pyinstaller --onefile --distpath ./ cv/main.py` 编译可执行文件并运行 `./main`.

**注意**: 如需要编译可执行文件, 请按照 [pyinstaller]([https://](https://pyinstaller.readthedocs.io/en/stable/installation.html)) 的说明安装相应的软件包.

**注意**: 如果需要重新编译, 建议创建一个新的环境, 并使用 `pip` 安装所有依赖, 如: `pip install -r requirements.txt`, 避免生成的可执行文件过大. **请勿安装非必要的包**
