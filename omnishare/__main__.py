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


def main(
    file: Annotated[str, typer.Argument(help="Provide markdown file")],
    add_token: Annotated[bool | None, typer.Option(help="Add API token")] = False,
    config: Annotated[bool | None, typer.Option(help="Add API token")] = False,
    reset: Annotated[bool | None, typer.Option(help="Warning: Remove all saved tokens")] = False,
):
    # Greeter
    console: Console = Console()
    console.clear()
    # console.print("Welcome", style="yellow")

    if add_token:
        add_more: bool = True
        while add_more:
            options: list[str] = [
                "LinkedIn",
                "Mastodon",
            ]
            console.print("Select a platform (Use arrow keys)\n", style="Cyan")
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
        # TODO: Add handler
        pass

    post: Post = process_file(file)
    # print(post.metadata)
    # print(post.content)

    # print(markdown_to_plain(post.content))
    linkedin_post(markdown_to_plain(post.content))
    mastodon_post(markdown_to_plain(post.content))


if __name__ == "__main__":
    typer.run(main)
