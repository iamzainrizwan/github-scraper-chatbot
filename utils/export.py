from pandas import DataFrame


def export_to_excel(filepath: str, repos: list[str], username: str):
    """exports a list of repo names to an xlsx file

    sheet is named after the github username.
    """
    df = DataFrame({"Repos": repos})
    df.to_excel(filepath, sheet_name=username, index=False)
