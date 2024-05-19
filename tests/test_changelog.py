from pyboiler.changelog import Changelog, Commit


def test_changelog():
    pass


if __name__ == "__main__":
    cl = Changelog("Anonoei", "pyboiler")
    print(f"Total commits: {cl['total']}")
    for idx, commit in enumerate(cl["commits"]):
        print("\n\t".join(list(commit)))

    input("pause")
