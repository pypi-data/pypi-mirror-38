# -*- coding: UTF-8 -*-

from backports import tempfile
import click
from halo import Halo
from mozdownload import FactoryScraper
import mozinstall
import mozlog
from mozprofile import FirefoxProfile
from mozrunner import FirefoxRunner
import mozversion
from setuptools_scm import get_version

mozlog.commandline.setup_logging("mozversion", None, {})


@click.command()
@click.option("--addon", "-a", "addons", multiple=True, help="Path to Firefox add-on")
@click.version_option(get_version())
def cli(addons):
    with tempfile.TemporaryDirectory() as tmpdir:
        build = download(dest=tmpdir)
        binary = install(src=build, dest=tmpdir)
        profile = generate_profile(addons=addons)
        launch(binary=binary, profile=profile)


def download(dest):
    scraper = FactoryScraper("daily", destination=dest)
    spinner = Halo(text="Downloading Firefox", spinner="dots")
    spinner.start()
    path = scraper.download()
    spinner.succeed("Downloaded Firefox to {}".format(path))
    return path


def install(src, dest):
    spinner = Halo(text="Installing Firefox", spinner="dots")
    spinner.start()
    path = mozinstall.install(src=src, dest=dest)
    spinner.succeed("Installed Firefox in {}".format(path))
    return mozinstall.get_binary(path, "firefox")


def generate_profile(addons):
    spinner = Halo(text="Generating profile", spinner="dots")
    spinner.start()
    profile = FirefoxProfile(addons=addons)
    spinner.succeed("Generated profile at {}".format(profile.profile))
    return profile


def launch(binary, profile):
    version = mozversion.get_version(binary)
    click.echo(
        "🦊 Running {application_display_name} "
        "{application_version} "
        "({application_buildid})".format(**version)
    )
    runner = FirefoxRunner(binary=binary, profile=profile)
    runner.start()
    runner.wait()


if __name__ == "__main__":
    cli()
