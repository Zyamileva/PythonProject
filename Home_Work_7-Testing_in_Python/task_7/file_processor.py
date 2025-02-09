class FileProcessor:
    @staticmethod
    def write_to_file(file_path: str, data: str):
        """Returns the current balance of the account.
        This method provides the current account balance.
        """
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(data)
        except FileNotFoundError:
            return "File not found"

    @staticmethod
    def read_from_file(file_path: str) -> str:
        """Reads data from a file.
        This method attempts to read and return the contents of the specified file.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError as e:
            raise FileNotFoundError("File not found") from e
