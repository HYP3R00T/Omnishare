from typing import Annotated

import typer
from beaupy import select
from frontmatter import Post
from rich.console import Console

from omnishare.file_handler import markdown_to_plain, process_file
from omnishare.linkedin import linkedin_post
from omnishare.mastodon import mastodon_post
from omnishare.token_handler import delete_token, prompt_token, save_token
from omnishare.utils import confirm

app = typer.Typer()


@app.command()
def executor(
    file: Annotated[str, typer.Argument(help="Provide markdown file")] = None,
    add_token: Annotated[bool, typer.Option(help="Add API token")] = False,
    config: Annotated[bool, typer.Option(help="Configure the tool")] = False,
    reset: Annotated[bool, typer.Option(help="Warning: Remove all saved tokens")] = False,
):
    # Greeter
    console: Console = Console()
    console.clear()

    if add_token:
        add_more: bool = True
        while add_more:
            options: list[str] = [
                "LinkedIn",
                "Mastodon",
            ]
            console.print("Select a platform (Use arrow keys)\n", style="cyan")
            option: str = select(sorted(options), cursor="\uf061", cursor_style="red")
            if option in options:
                token = prompt_token()
                save_token(option, token)
            else:
                print("\nInvalid platform selected.")
            add_more = confirm("Add more?")

    if reset:
        delete_token()

    if config:
        console.print("This is Work in Progress")
        # TODO: Add handler
        pass

    if file:
        post: Post = process_file(file)
        linkedin_post(markdown_to_plain(post.content))
        mastodon_post(markdown_to_plain(post.content))
    elif not (add_token or config or reset):
        raise typer.BadParameter("No file provided")


def main():
    app()


if __name__ == "__main__":
    app()
