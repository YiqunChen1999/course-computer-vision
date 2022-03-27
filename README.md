
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

请进入项目根目录, 并在 Linux 终端下运行 `./main`.

## 重新编译

如果需要修改配置, 创建一个虚拟环境并运行 `./run.sh`, 然后修改 `cv/cv/configs/default.py` 中的文件, 之后可以直接在**根目录下**运行 `python cv/main.py`, 或者在**根目录**下通过 `pyinstaller --onefile --distpath ./ cv/main.py` 编译可执行文件并运行 `./main`.

**注意**: 如需要编译可执行文件, 请按照 [pyinstaller]([https://](https://pyinstaller.readthedocs.io/en/stable/installation.html)) 的说明安装相应的软件包.

## TODO

- [ ] 修改为运行时读取的配置文件;
