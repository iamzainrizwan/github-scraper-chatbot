from pandas import DataFrame


def export_to_excel(filepath: str, repos: list[str], username: str):
    df = DataFrame({"Repos": repos})
    df.to_excel(filepath, sheet_name=username, index=False)
