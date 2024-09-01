import time

def main():
    from pyboiler.cli import progress

    sp = progress.Simple()
    spc = progress.SimpleColored()

    dur = 10
    inc = 0.05

    if False:
        cur = 0
        while cur < dur:
            cur += inc
            sp.bar(cur / dur, f"testing")
            time.sleep(inc)
        print()

    if False:
        cur = 0
        while cur < dur:
            cur += inc
            spc.bar(cur / dur, f"testing")
            time.sleep(inc)
        print()

    if False:
        with progress.Context("Testing") as p:
            cur = 0
            while cur < dur:
                cur += inc
                p.show(cur / dur, f"testing")
                time.sleep(inc)

    if True:
        with progress.ContextColored("Testing") as p:
            cur = 0
            while cur < dur:
                cur += inc
                p.show(cur / dur, f"testing")
                time.sleep(inc)


if __name__ == "__main__":
    main()
