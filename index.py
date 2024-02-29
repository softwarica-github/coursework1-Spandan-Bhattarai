def main():
    print("Choose an option:")
    print("1. GUI Version")
    print("2. CLI Version")

    choice = input("Enter your choice: ")

    if choice == "1":
        import final
        final.main()
    elif choice == "2":
        import final_cli
        final_cli.main()
    else:
        print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()
