from datetime import datetime

import click
import crayons
from tabulate import tabulate
import tweakers

from . import __version__


def format_date(dt):
    if dt.date() == datetime.today().date():
        return dt.strftime("%H:%M")
    elif dt.year == datetime.today().year:
        return dt.strftime("%d-%m")
    else:
        return dt.strftime("%d-%m-%Y")


def print_comment(comment):
    """Pretty print a comment"""
    print(
        crayons.yellow((comment.date.strftime("%H:%M"))),
        crayons.green(comment.user.name),
        crayons.blue(comment.url),
    )
    print(comment.text, "\n")


def choose_topic(topics):
    """Return chosen topic from a printed list of topics

    Args:
        topics (list): List of Topic objects

    Returns:
        topic (Topic): Chosen topic
    """
    table = []
    for i, t in enumerate(topics):
        row = [i + 1, t.title, format_date(t.last_reply)]
        table.append(row)
    print("\n", tabulate(table, headers=["#", "Titel", "Laatste reactie"]))

    choice = click.prompt(f"\nChoose a topic to stream (1-{len(topics)})", type=int)
    return topics[choice - 1]


@click.group()
@click.version_option(version=__version__)
@click.option("--last", default=3, help="Number of previous comments to show.")
@click.pass_context
def cli(ctx, last):
    ctx.ensure_object(dict)
    ctx.obj['last'] = last


@cli.command(name="stream", help="Stream from a specific url.")
@click.argument("url")
@click.pass_context
def stream(ctx, url):
    topic = tweakers.gathering.Topic(url=url)
    for comment in topic.comment_stream(last=ctx.obj['last']):
        print_comment(comment)


@cli.command(name="list", help="Shows a list of active topics.")
@click.option("-n", default=20, help="Number of topics to show.")
@click.pass_context
def list_active(ctx, n):
    """Choose from a list of active topics"""
    topics = tweakers.gathering.active_topics()[:n]

    topic = choose_topic(topics)
    for comment in topic.comment_stream(last=ctx.obj['last']):
        print_comment(comment)


@cli.command(name="search", help="Search for a specific topic.")
@click.argument("query", nargs=-1)
@click.option("-n", default=10, help="Number of results to show.")
@click.pass_context
def search(ctx, query, n):
    query = " ".join(query)
    topics = tweakers.gathering.search(query)

    if len(topics) == 0:
        click.echo("No topics found!")
        raise SystemExit

    topic = choose_topic(topics)
    for comment in topic.comment_stream(last=ctx.obj['last']):
        print_comment(comment)


if __name__ == "__main__":
    cli(obj={})
