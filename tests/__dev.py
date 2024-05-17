def main():
    import pyboiler.color as color

    print(color.Format.format("uppercase: {s:u}, lowercase: {s:l}", s="abc"))


if __name__ == "__main__":
    main()
