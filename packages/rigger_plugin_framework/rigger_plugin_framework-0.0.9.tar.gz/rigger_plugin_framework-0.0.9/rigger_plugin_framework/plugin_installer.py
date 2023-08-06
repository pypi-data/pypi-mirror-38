import os
import tarfile
import shutil
import sys
from rigger_singleton.singleton import singleton

requirements_dir = "requirements"
@singleton
class PluginInstaller:
    """
    插件安装器，用于将指定插件安装到项目中
    """

    @staticmethod
    def install(file_path, dest_dir):
        assert os.path.exists(file_path)
        # 确保安装路径存在且合法
        PluginInstaller.make_sure_dir(dest_dir)

        assert os.path.exists(dest_dir)

        with tarfile.open(file_path) as fp:
            fp.extractall(path=dest_dir)
            fp.close()

        # 将解压后的文件重命名（去除掉一些可能存在的版本号,以便模块能正确引入
        # 获取解压后的文件名
        prefix, file_name = os.path.split(file_path)
        if file_name.endswith(".tar.gz"):
            file_name = file_name[: -7]

        # 从PKG-INFO中获取真实的包名
        info_file = os.path.join(dest_dir, file_name, "PKG-INFO")
        if not os.path.exists(info_file):
            raise Exception("now only support pip package style plugin")

        pkg_name = ""
        with open(info_file, "r") as fp:
            for line in fp:
                if line.startswith("Name:"):
                    pre, pkg_name = line.split(":")
                    pkg_name = pkg_name.strip()
                    break
            fp.close()

        if pkg_name != "":
            pkg_name = os.path.join(dest_dir, pkg_name)
            # 如果原来已经存在，则删除
            if os.path.exists(pkg_name):
                shutil.rmtree(pkg_name)
                # 重命名
            os.rename(os.path.join(dest_dir, file_name), pkg_name)
            # 安装插件的依赖
            PluginInstaller.install_requirements(pkg_name, dest_dir)
        else:
            raise Exception("seems not a valid PKG-INFO file")

    @staticmethod
    def install_requirements(path: str, dest: str):
        path = os.path.join(path, requirements_dir)
        if os.path.exists(path):
            for file in os.listdir(path):
                if PluginInstaller.check_file_name(file):
                    temp = os.path.join(path, file)
                    PluginInstaller.install(temp, dest)

    @staticmethod
    def make_sure_dir(directory):
        if os.path.exists(directory):
            if os.path.isdir(directory):
                pass
            else:
                raise Exception(directory + " is not a valid dir, please check!")
        else:
            os.mkdir(directory)

    @staticmethod
    def check_file_name(file_name: str):
        import os
        (part1, part2) = os.path.splitext(file_name)
        if part2 == "":
            return part1 in [".gz"]
        else:
            return part2 in [".gz"]



