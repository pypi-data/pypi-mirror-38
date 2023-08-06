import logging
import platform
import gspm.utils.path_utils as path_utils
import wget
import zipfile
import os
import gspm.utils.process_utils as process_utils
from packaging.version import Version
import subprocess


host_url = "https://downloads.tuxfamily.org/godotengine/{0}/"


def edit_godot(project):

    cmd = _build_godot_cmd(project)
    cmd = "{0} -e".format(cmd)
    # cmd = "start dir"
    logging.debug("- running command {0}".format(cmd))
    process_utils.run_process(cmd, True)


def install_godot(project):

    logging.debug("[godot_utils] install_godot")
    logging.debug(
        "- checking for godot [{0}]".format(project.config.godot.version))

    dest_path = \
        "{0}/godot-{1}" \
        .format(project.repository_home, project.config.godot.version)

    if os.path.exists(dest_path):
        if not project.args.force:
            logging.debug(
                "- Godot is already available at [{0}] - skipping"
                .format(dest_path))
            return
        else:
            path_utils.clean_path(dest_path)

    path_utils.create_path(dest_path)

    uri = _build_godot_uri(project)
    logging.debug("- downloading [{0}] to [{1}]".format(uri, dest_path))
    file = wget.download(uri, dest_path)
    logging.debug("- dowload complete")
    zipf = zipfile.ZipFile(file)
    zipf.extractall(dest_path)
    zipf.close()
    if _get_platform() != "windows":
        zfile = "{0}/Godot.app".format(dest_path)
        subprocess.call(['chmod', '-R', '+x', zfile])
    os.remove(file)


def _build_godot_uri(project):
    logging.debug("[godot_utils] _build_godot_uri")

    system = _get_platform()
    uri = ""

    if system == "windows":
        uri = _build_windows_uri(project)

    if system == "darwin":
        uri = _build_darwin_uri(project)

    if system == "linux":
        uri = _build_linux_uri(project)

    if not uri:
        raise Exception("Platform [{0}] Not Supported".format(system))

    return uri


def _build_godot_cmd(project):
    logging.debug("[godot_utils] _build_godot_cmd")
    system = _get_platform()
    cmd = ""

    if system == "windows":
        cmd = _build_windows_cmd(project)

    if system == "darwin":
        cmd = _build_darwin_cmd(project)

    if cmd:
        return cmd
    else:
        raise Exception("Platform [{0}] Not Supported".format(system))


def _build_windows_uri(project):

    logging.debug("[godot_utils] _build_windows_uri")

    stable = 'stable'

    if Version('{0}'.format(project.config.godot.version)) < Version('3.1'):
        host = host_url.format(project.config.godot.version)
    else:
        host = host_url.format("{0}".format(project.config.godot.version) + "/alpha1")
        stable = 'alpha1'

    if Version('{0}'.format(project.config.godot.version)) < Version("2.1"):
        template = "{2}Godot_v{0}_{3}_win{1}.exe.zip"
    else:
        template = "{2}Godot_v{0}-{3}_win{1}.exe.zip"

    uri = template.format(project.config.godot.version, project.config.godot.arch, host, stable)
    return uri


def _build_darwin_uri(project):

    logging.debug("[godot_utils] _build_darwin_uri")

    stable = 'stable'

    if Version('{0}'.format(project.config.godot.version)) < Version('3.1'):
        host = host_url.format(project.config.godot.version)
    else:
        host = host_url.format("{0}".format(project.config.godot.version) + "/alpha1")
        stable = 'alpha1'

    if Version('{0}'.format(project.config.godot.version)) < Version("2.1"):
        template = "{2}Godot_v{0}_{3}_osx.fat.zip"
    else:
        template = "{2}Godot_v{0}-{3}_osx.fat.zip"

    uri = template.format(project.config.godot.version, project.config.godot.arch, host, stable)
    return uri


def _build_linux_uri(project):
    return ""


def _build_windows_cmd(project):
    godot_path = os.path.abspath("{0}/godot-{1}/".format(project.repository_home, project.config.godot.version))
    proj_path = os.path.abspath(project.project_path)
    cmd = "start {0}\{1} --path {2}".format(godot_path, _get_godot_runtime(project), proj_path)
    return cmd


def _build_linux_cmd():
    pass


def _build_darwin_cmd(project):
    godot_path = os.path.abspath("{0}/godot-{1}/".format(project.repository_home, project.config.godot.version))
    proj_path = os.path.abspath(project.project_path)
    cmd = "arch -{3} {0}/{1} --path {2}".format(godot_path, _get_godot_runtime(project), proj_path, project.config.godot.arch)
    return cmd


#   return the platform we are running on
def _get_platform():
    return platform.system().lower()


def _get_godot_runtime(project):
    plat = _get_platform()
    runtime = ""

    if plat == "windows":
        runtime = _get_windows_runtime(project)

    if plat == "darwin":
        runtime = _get_darwin_runtime(project)

    if runtime:
        return runtime
    else:
        raise Exception("Platform [{0}] Not Supported".format(plat))


def _get_windows_runtime(project):
    logging.debug('[godot_utils] _get_windows_runtime')
    if Version('{0}'.format(project.config.godot.version)) < Version('3.1'):
        stable = 'stable'
    else:
        stable = 'alpha1'

    runtime = "Godot_v{0}-{2}_win{1}.exe".format(project.config.godot.version, project.config.godot.arch, stable)
    return runtime


def _get_linux_runtime(project):
    pass


def _get_darwin_runtime(project):
    logging.debug('[godot_utils] _get_darwin_runtime')
    runtime = "Godot.app/Contents/MacOS/Godot"
    return runtime

