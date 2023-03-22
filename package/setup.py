from setuptools import setup
# from setuptools import find_packages
setup(
    name="HealthMate",
    version="1.0.0",
    author="yuanmoc",
    author_email="yuanmoc@qq.com",
    url='https://github.com/yuanmoc/HealthMate',
    description="健康160自动挂号模块",
    long_description="健康160自动挂号模块",
    # python依赖版本
    python_requires=">=3.9.0",
    # 指定许可证
    license="MIT Licence",
    # 需要安装的依赖,如["matplotlib", "talib", "pylab", "numpy", "pandas", "baostock"]
    install_requires=["requests", "click", "configparser", "pycryptodome", "pyqt6"],
    # 打包目录下的指定模块
    packages=[
        "utils",
        "utils.qt6",
        "app"
    ],
    # 打包目录下的全部模块
    # packages=find_packages(),
    # 打包除了指定模块的全部模块
    # packages=find_packages(exclude=["test", "test.*"])
    # 打包路径下的其他文件
    # include_package_data = True,
    # 资源文件
    package_data={
        'app': ['ui/login-ui.ui','ui/main-ui.ui']
    },
    # 程序适用的软件平台列表
    platforms="any",
)
