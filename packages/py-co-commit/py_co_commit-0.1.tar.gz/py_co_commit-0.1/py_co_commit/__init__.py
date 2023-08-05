from subprocess import call


def co_author_string(co_author):
    return "-m \"Co-authored-by: {} <{}@users.noreply.github.com>\"".format(
        co_author,
        co_author.lower()
    )


def main():
    co_authors = [
        co_author.strip() for co_author in input("Co-authors names (separated by commas): ").split(",") if co_author
    ]
    commit_message = input("Commit message: ")
    command = ["git", "commit", "-m \"{}\"".format(commit_message)] + \
              [co_author_string(co_author) for co_author in co_authors]
    print(" ".join(command))
    call(command)


if __name__ == "__main__":
    main()
