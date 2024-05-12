from pyboiler.error import Error


def test_error():
    pass


if __name__ == "__main__":

    class MyError(Error):
        msg = "My custom error"

    raise MyError("because I can")
