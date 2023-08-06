
import io
import logging
import os
import yaml
import dotmap


def load(filename: str):

    logging.debug("[project] load")

    try:
        logging.debug("- looking for config file [{0}]".format(filename))
        if not os.path.exists(filename):
            logging.debug("- unable to locate the project configuration file [{0}]".format(filename))
            raise Exception("gspm Project Configuration File [{0}] was Not Found.".format(filename))

        #   get config file text
        file = io.open(filename)
        text = file.read()

        #   create contents
        contents = yaml.load(text)

        #   create project from contents
        project = dotmap.DotMap(contents)

        #   validate the project
        _validate(project)

        #   return the project
        return project

    except Exception as e:
        raise e


def _validate(project):

    if 'name' not in project:
        raise Exception("Project Configuration is Missing [name] Attribute.")

    #   default_type is git
    if 'default_type' not in project:
        project.default_type = 'git'

    if 'path' not in project:
        project.path = '.'

    if 'godot' not in project:
        raise Exception("Project Configuration is Missing [godot] Attribute")

    if 'arch' not in project.godot:
        project.godot.arch = 32

    if 'mono' not in project.godot:
        project.godot.mono = False

    if 'assets' not in project:
        raise Exception("Project Configuration is Missing [assets] Section")

    for asset_name in project.assets:

        asset = project.assets[asset_name]

        if 'location' not in asset:
            raise Exception("Asset [{0}] is Missing its [location] Attribute".format(asset.name))

        if 'type' not in asset:
            asset.type = project.default_type

        asset.name = asset_name

        if 'active' not in asset:
            asset.active = True

        _check_includes(asset)


def _check_includes(asset):

    if 'includes' not in asset:
        asset.includes = []
        inc = dotmap.DotMap()
        inc.dir = "{0}".format(asset.name)
        asset.includes.append(inc)

    for include in asset.includes:
        if 'todir' not in include:
            include.todir = "{0}".format(include.dir)
