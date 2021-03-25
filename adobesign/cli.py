##########################################################################
# © Copyright 2015-2021 Adobe. All rights reserved.
# Adobe holds the copyright for all the files found in this repository.
# See the LICENSE file for licensing information.
##########################################################################

"""CLI interface for Adobe Sign."""

import os
import typer
from dotenv import load_dotenv

from .sign import Sign
from .assets import Transfer
from .people import UMG

app = typer.Typer()


def build_val(val, key):
    load_dotenv()
    if val:
        return val
    if os.getenv(key):
        return os.getenv(key)
    raise Exception("You need to provide a value")


def build_integration_key(key):
    if not key:
        load_dotenv()
        key = os.getenv("INTEGRATION_KEY")
    if not key:
        key = typer.prompt("What's the integration key?", hide_input=True)
    return key


def build_uri(uri):
    if not uri:
        load_dotenv()
        uri = os.getenv("BASE_URI")
    if not uri:
        uri = typer.prompt("What's the base uri?")
    return f"{uri}api/rest/v6/"


@app.command()
def hello_world():
    print("hi")


@app.command()
def setup():
    print("hi")


@app.command()
def clone_template(
    template_id: str = typer.Option(
        ...,
        "--template",
        "-t",
        help="Template ID",
        prompt=True,
    ),
    sender_email: str = typer.Option(
        ...,
        "--sender",
        "-s",
        help="Sending user's email",
        prompt=True,
    ),
    receiver_email: str = typer.Option(
        ...,
        "--receiver",
        "-r",
        help="Recieving user's email",
        prompt=True,
    ),
    key: str = typer.Option(
        None,
        "--integration-key",
        "-k",
        help="Integration key (Defaults to the INTEGRATION_KEY env var)",
        callback=build_integration_key,
    ),
    base_uri: str = typer.Option(
        None,
        "--base-uri",
        "-u",
        help="Base URI (Defaults to the BASE_URI env var)",
        callback=build_uri,
    ),
    receiver_key: str = typer.Option(
        None,
        "--receiver-key",
        "-K",
        help="Integration key for the receiver (Defaults to sender's integration key)",
    ),
    receiver_base_uri: str = typer.Option(
        None,
        "--receiver-base-uri",
        "-U",
        help="Base URI for the receiver (Defaults to sender's base uri)",
    ),
):
    # Optional receiver info
    if not receiver_key:
        receiver_key = key
    if not receiver_base_uri:
        receiver_base_uri = base_uri

    typer.echo(f"Cloning {template_id} from {sender_email} to {receiver_email}\n")

    sender = Sign(key, base_uri, sender_email)
    receiver = Sign(receiver_key, receiver_base_uri, receiver_email)
    transfer = Transfer(sender, receiver)
    out = transfer.clone_template(template_id)

    typer.echo(f"Success!\n\nTemplate {out} created")


@app.command()
def default_primary_report(
    key: str = typer.Option(
        None,
        "--integration-key",
        "-k",
        help="Integration key (Defaults to the INTEGRATION_KEY env var)",
        callback=build_integration_key,
    ),
    base_uri: str = typer.Option(
        None,
        "--base-uri",
        "-u",
        help="Base URI (Defaults to the BASE_URI env var)",
        callback=build_uri,
    ),
):
    sign = Sign(key, base_uri)
    umg = UMG(sign)
    out = umg.users_with_default_primary()

    typer.echo(list(out))


@app.command()
def make_default_not_primary(
    key: str = typer.Option(
        None,
        "--integration-key",
        "-k",
        help="Integration key (Defaults to the INTEGRATION_KEY env var)",
        callback=build_integration_key,
    ),
    base_uri: str = typer.Option(
        None,
        "--base-uri",
        "-u",
        help="Base URI (Defaults to the BASE_URI env var)",
        callback=build_uri,
    ),
):
    sign = Sign(key, base_uri)
    umg = UMG(sign)
    out = umg.make_default_not_primary()

    typer.echo(list(out))


def main():
    app()
