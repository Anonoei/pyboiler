def main():
    from pyboiler.logging import Level, logging

    log = logging("dev", Level.TRACE)

    log.mk_handler("stdout")

    log.trace("Hello")
    log.info("World!")


if __name__ == "__main__":
    main()
