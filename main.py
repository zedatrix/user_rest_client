from user_client import UserClient
"""
Main function for prompting user input for page number and number of users per page,
fetching users using UserClient, displaying fetched users with proper alignment,
and handling exceptions by printing error message and returning an empty list.
"""
def main():
    try:
        """
        The main function to interact with the UserClient API and display user information.

        This function prompts the user to input a page number and the number of users per page,
        with the option to leave either input empty to use default values. The function then
        fetches user data using the UserClient class and displays it in a colorful, formatted table.

        Variables:
        - default_page: Default value for the page number if the user input is empty or invalid.
        - default_per_page: Default value for the number of users per page if the user input is empty or invalid.
        - reset_color: ANSI escape code to reset text color back to the terminal's default.
        - promptTextColor: ANSI escape code to set the text color for prompts.
        - table_header_color: ANSI escape code to set the text color for the table header.
        - header_color: ANSI escape code to set the text color for the column headers.
        - text_color: ANSI escape code to set the text color for the user data.
        - lineColor: ANSI escape code to set the text color for the table lines.
        - bottomLine, longTopLine, longBottomLine: String variables used to create lines in the table.
        - singleTopLine, singleBottomLine: Formatted strings that include the table lines with color.
        - footer: A formatted string containing meta information about the fetched data.

        The user input is validated and converted to integers, and if no valid input is provided,
        the defaults are used. The function handles any exceptions during the API call or processing,
        and displays an error message with a red text color if an exception occurs.

        The output includes a header, the user data, and a footer, all with appropriate coloring
        and formatting. Column widths are dynamically adjusted to accommodate the longest names.

        Raises:
            Exception: Generic exception handling to catch any unexpected errors during execution.
        """
        # Default values
        default_page = 1
        default_per_page = 20
        reset_color = "\033[0m"

        # prompt color
        promptTextColor = "\033[38;2;0;255;0m"

        # Prompt for page number
        page = input(f"{promptTextColor}Page Number (empty for 1 page):{reset_color} ")
        page = int(page) if page.isdigit() and int(page) > 0 else default_page

        # Prompt for number of users per page
        per_page = input(f"{promptTextColor}Users per Page (empty for 20 users per page):{reset_color} ")
        per_page = int(per_page) if per_page.isdigit() and int(per_page) > 0 else default_per_page

        user_client = UserClient()
        users = user_client.get_users(page=page, per_page=per_page)
        metaInfo = user_client.get_users_meta()
        #rest of the variables
        table_header_color = "\033[38;2;255;51;255m"
        header_color = "\033[38;2;128;255;255m"
        text_color = "\033[38;2;255;153;0m"
        lineColor = "\033[38;2;255;255;204m"
        bottomLine = '_' * 15
        longTopLine = '-' * 31
        longBottomLine = '_' * 31
        singleTopLine = f"{lineColor}|{longTopLine}|{reset_color}"
        singleBottomLine = f"{lineColor}|{longBottomLine}|{reset_color}"
        # Conditional formatting for the footer based on the number of digits in totalPages
        totalPages, isDoubleDigit = metaInfo['total_pages']
        if(isDoubleDigit):
            # If totalPages is a double-digit number, format the footer without an additional space
            footer = f"{lineColor}|There are {metaInfo['total']} users & {totalPages} page(s)|{reset_color}"
        else:
            # If totalPages is a single-digit number, add an extra space to maintain alignment
            footer = f"{lineColor}|There are {metaInfo['total']} users & {totalPages} page(s) |{reset_color}"
        # Determine the longest first and last name for proper alignment
        longest_first_name = max(len(user.first_name) for user in users)
        longest_last_name = max(len(user.last_name) for user in users)
        longest_first_name+=4
        longest_last_name+=4
        print(f" {lineColor}{bottomLine}_{bottomLine}{reset_color}")
        print(f"{lineColor}/{table_header_color} Fetched Users:{lineColor}\t\t\\{reset_color}")
        print(f"{lineColor}\\{bottomLine}_{bottomLine}{lineColor}/{reset_color}")
        # Headers
        print(f"|{header_color}{'First Name'.ljust(longest_first_name)}\t{header_color}{'Surname'.ljust(longest_last_name)}\t{lineColor}|{reset_color}")

        for user in users:
            print(singleTopLine)
            print(f"{lineColor}|{text_color}{user.first_name.ljust(longest_first_name)}{lineColor}\t{text_color}{user.last_name.ljust(longest_last_name)}\t{lineColor}|{reset_color}")
        print(f"{singleTopLine}")
        print(footer)
        print(singleBottomLine)
    except Exception as e:
        print(f'\033[91mError fetching data: {e}\033[0m')
        return []
if __name__ == "__main__":
    main()