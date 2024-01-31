# No change in user_dto.py

import requests
from user_dto import UserDTO

class UserClient:
    def __init__(self) -> None:
        """
        Initialize the class with an empty meta dictionary.
        """
        self.meta = {}
    def get_users(self, page=1, per_page=20):
        """
        Sends a GET request to the 'https://reqres.in/api/users' API to retrieve a list of users.

        Args:
            self: The object instance
            page (int, optional): The page number for pagination. Defaults to 1.
            per_page (int, optional): The number of users per page. Defaults to 20.

        Returns:
            list: A list of UserDTO objects representing the users retrieved from the API.
        """
        try:
            response = requests.get(f'https://reqres.in/api/users?page={page}&per_page={per_page}', timeout=10)
            response.raise_for_status()
            users = response.json()
            self.meta['total'] = users.get('total')
            total_pages = users.get('total_pages')
            if(total_pages >= 10):
                self.meta['total_pages'] = ([total_pages, True])
            else:
                self.meta['total_pages'] = ([users.get('total_pages'), False])
            users_data = users.get('data', [])
            return [UserDTO(user['id'], user['email'], user['first_name'], user['last_name']) for user in users_data]
        except requests.exceptions.RequestException as e:
            print(f'\033[91mError fetching data: {e}\033[0m')  # Red color for errors
            return []
    def get_users_meta(self):
        """
        Retrieves the meta information for all users.

        :return: All user meta information.
        """
        try:
            return self.meta
        except requests.exceptions.RequestException as e:
            print(f'\033[91mError fetching data: {e}\033[0m')  # Red color for errors
            return []