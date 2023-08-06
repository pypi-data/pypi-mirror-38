# -*- coding: utf-8 -*-

"""Console script for github_cards."""
import datetime
import sys

import click
import github3
from jinja2 import Environment, PackageLoader, select_autoescape

from github_cards.otp_cache import OTPCache


@click.command()
@click.argument("owner")
@click.argument("repository")
@click.option("-u", "--username")
@click.option("-m", "--milestone-title")
@click.option("-m#", "--milestone-number")
@click.option("-s", "--state", default="open")
@click.option("-o", "--output")
def main(owner, repository, username, milestone_title, milestone_number, state, output):
    """Console script for github_cards."""
    gh = github3.GitHub()
    if username is not None:
        password = click.prompt(
            f"Please enter GitHub-Password for {username}", hide_input=True
        )
        gh.login(
            username=username,
            password=password,
            two_factor_callback=OTPCache().otp_callback,
        )
    try:
        repo = gh.repository(owner=owner, repository=repository)
    except github3.exceptions.NotFoundError:
        click.echo(
            f"Can't find repository {owner}/{repository}. Maybe you need to authorize",
            err=True,
        )
        return 1

    if milestone_title is not None:
        milestones = repo.milestones()
        try:
            milestone = [
                milestone
                for milestone in milestones
                if milestone.title == milestone_title
            ][0]
        except IndexError:
            click.echo(f"Can't find milestone {milestone_title}", err=True)
            return 1
        milestone_number = milestone.number
    issues = repo.issues(milestone=milestone_number, state=state)

    env = Environment(
        loader=PackageLoader("github_cards", "templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("index.html")
    rendered = template.render(issues=list(issues))

    if output is None:
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        output = f"{owner}-{repository}-{now_str}.html"
    with open(output, "w") as file:
        file.write(rendered)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
