def main():
    print("Choose an option:")
    print("1. GUI Version")
    print("2. CLI Version")

    choice = input("Enter your choice: ")

    if choice == "1":
        import finalll
        finalll.main()
    elif choice == "2":
        import finalcli
        finalcli.main()
    else:
        print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()
