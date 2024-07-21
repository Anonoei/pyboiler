def main():
    from pyboiler.logger import Logger, Level

    log = Logger("dev", Level.TRACE)

    log.trace("Hello")
    log.info("World!")

    Logger().Child("Test").trace("Test!")


if __name__ == "__main__":
    main()
