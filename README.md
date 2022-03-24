
# 计算机视觉

## 代码说明

本项目代码按照以下方式组织:

```python
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
```

## 输入图像

请将图像放置于 `cv/images` 之下, 代码运行结果将保存于 `cv/results` 之下. 当前已经实现的算法为阈值分割算法, 默认任务为 `segmentation`, 若需要增加或者修改任务, 请在 `cv/cv/configs/default.py` 中的 `configs.general.tasks` 修改.

## 运行程序

请进入项目根目录, 并在 Linux 终端下运行 `sh ./run.sh`.
