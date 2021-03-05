import os
import typer
from dotenv import load_dotenv

from .sign import Sign
from .assets import Transfer

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
    reciever_email: str = typer.Option(
        ...,
        "--reciever",
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
    reciever_key: str = typer.Option(
        None,
        "--reciever-key",
        "-K",
        help="Integration key for the reciever (Defaults to sender's integration key)",
    ),
    reciever_base_uri: str = typer.Option(
        None,
        "--reciever-base-uri",
        "-U",
        help="Base URI for the reciever (Defaults to sender's base uri)",
    ),
):

    # Optional reciever info
    if not reciever_key:
        reciever_key = key
    if not reciever_base_uri:
        reciever_base_uri = base_uri

    typer.echo(f"Cloning {template_id} from {sender_email} to {reciever_email}\n")

    sender = Sign(key, base_uri, sender_email)
    reciever = Sign(reciever_key, reciever_base_uri, reciever_email)
    transfer = Transfer(sender, reciever)
    out = transfer.clone_template(template_id)

    typer.echo(f"Success!\n\nTemplate {out} created")


def main():
    app()
