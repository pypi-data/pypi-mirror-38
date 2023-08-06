import os
import sys
import errno
import git
import json
import yaml
import logging
import click
import shutil
from os.path import expanduser
from configobj import ConfigObj


tmuxinator_config = os.path.join(expanduser("~"), ".config", "tmuxinator")


class LocalConfig(object):
    def __init__(self):
        self.__config_path = os.path.join(
            os.path.expanduser("~"), ".config", "xiaomi", "config"
        )
        self.mkdirs(os.path.join(os.path.expanduser("~"), ".config", "xiaomi"))

        self.__data = None
        with open(self.__config_path) as f:
            self.__data = json.load(f)

    @property
    def xiaomi_username(self):
        return self.__data.get("xiaomi_username")

    @xiaomi_username.setter
    def xiaomi_username(self, value):
        if value is not None and value.strip() != "":
            self.__data["xiaomi_username"] = value
            self.dump()

    @property
    def minos1_config_location(self):
        return self.__data.get("minos1_config_location")

    @minos1_config_location.setter
    def minos1_config_location(self, value):
        if value is not None and value.strip() != "":
            self.__data["minos1_config_location"] = value
            self.dump()

    @property
    def minos2_config_location(self):
        return self.__data.get("minos2_config_location")

    @minos2_config_location.setter
    def minos2_config_location(self, value):
        if value is not None and value.strip() != "":
            self.__data["minos2_config_location"] = value
            self.dump()

    def dump(self):
        with open(self.__config_path, "w") as outfile:
            json.dump(
                self.__data, outfile, sort_keys=True, indent=4, separators=(",", ": ")
            )

    def mkdirs(self, path):
        try:
            if not os.path.isdir(path):
                os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(
                os.path.join(os.path.expanduser("~"), ".config", "xiaomi")
            ):
                pass


@click.group()
@click.pass_context
def cli(ctx):
    """
    A handy tool for generating tmuxinator configurations from minos
    """
    conf = LocalConfig()
    ctx.ensure_object(dict)
    ctx.obj["conf"] = conf
    if (
        conf.xiaomi_username is None
        or conf.minos1_config_location is None
        or conf.minos2_config_location is None
    ):
        ctx.invoke(config)


def update_minos_git_repository(config_path):
    click.echo("Updating {}...".format(config_path))
    repo = git.Repo(config_path)
    o = repo.remotes.origin
    o.pull()
    click.echo("Done")


@cli.command()
@click.pass_context
def update(ctx):
    '''
    Update minos git repositories
    '''
    update_minos_git_repository(ctx.obj["conf"].minos1_config_location)
    update_minos_git_repository(ctx.obj["conf"].minos2_config_location)    


def clean_tmuxinator_configurations():
    click.echo("Cleaning tmuxinator configurations...")
    shutil.rmtree(tmuxinator_config)
    os.makedirs(tmuxinator_config)
    click.echo("Done")


@cli.command()
@click.pass_context
def clean(ctx):
    """
    Clean(remove) the tmuxinator configurations
    """
    clean_tmuxinator_configurations()


@cli.command()
@click.option(
    "--update", is_flag=True, help="Generate with updating minos git repositories"
)
@click.option(
    "--clean", is_flag=True, help="Clean(remove) the tmuxinator configurations"
)
@click.pass_context
def generate(ctx, update, clean):
    """
    Generate tmuxinator configuration files from your minos configurations
    """
    if update:
        update_minos_git_repository(ctx.obj["conf"].minos1_config_location)
        update_minos_git_repository(ctx.obj["conf"].minos2_config_location)
    
    if clean:
        clean_tmuxinator_configurations()

    paths = [
        os.path.join(ctx.obj["conf"].minos1_config_location, "xiaomi-config/conf/fds/"),
        os.path.join(ctx.obj["conf"].minos2_config_location, "xiaomi-config/conf/fds/"),
    ]
    regions = check_and_get_regions(paths)
    click.echo("Will generate configurations for tmuxinator")
    for k, v in regions.items():
        generate_4region(k, v, ctx.obj["conf"])


@cli.command()
@click.pass_context
def config(ctx):
    """
    Configurate the files needed by muxminos
    """
    conf = ctx.obj["conf"]
    default_xiaomi_username = conf.xiaomi_username
    default_minos1_config_location = conf.minos1_config_location
    default_minos2_config_location = conf.minos2_config_location

    conf.xiaomi_username = input(
        "Enter xiaomi username(default: {}) >> ".format(default_xiaomi_username)
    )
    conf.minos1_config_location = input(
        "Enter minos1 config location(default: {}) >> ".format(
            default_minos1_config_location
        )
    )
    conf.minos2_config_location = input(
        "Enter minos2 config location(default: {}) >> ".format(
            default_minos2_config_location
        )
    )


def check_and_get_regions(paths):
    regions = {}
    for path in paths:
        path = os.path.expanduser(path)
        for root, dirs, files in os.walk(path):
            for file in files:
                if os.path.splitext(file)[1] == ".cfg":
                    restserver = ConfigObj(os.path.join(path, file)).get("restserver")
                    hosts = []
                    if restserver is not None:
                        for key in restserver:
                            if key.startswith("host"):
                                hosts.append(restserver[key])
                        regions[os.path.splitext(file)[0]] = hosts
                elif os.path.splitext(file)[1] == ".yaml":
                    try:
                        with open(os.path.join(path, file)) as f:
                            hosts = (
                                yaml.load(f).get("jobs").get("restserver").get("hosts")
                            )
                            regions[os.path.splitext(file)[0]] = hosts
                    except Exception as e:
                        click.echo(e.message)
            break
    return regions


def generate_4region(region_name, hostlist, conf: LocalConfig):
    print("Generating configuration file for " + region_name)
    y = {"name": "", "windows": []}
    y["name"] = region_name
    index = 0
    win_name = ""
    block = {"layout": "even-vertical", "panes": []}
    for host in hostlist:

        block["panes"].append(
            {
                host: [
                    "ssh " + conf.xiaomi_username + "@relay.xiaomi.com",
                    host,
                    "cd /home/work/app/nginx/logs/",
                ]
            }
        )
        index = index + 1
        win_name = (
            win_name
            + ("" if win_name == "" else "-")
            + host.split(".")[0].split("-")[2]
        )
        if index == 4:
            y["windows"].append({win_name: block})
            block = {"layout": "even-vertical", "panes": []}
            index = 0
            win_name = ""
    y["windows"].append({win_name: block})
    with open(os.path.join(tmuxinator_config, region_name + ".yml"), "w") as f:
        yaml.dump(y, f, default_flow_style=False)
