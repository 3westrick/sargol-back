from typing import Any
from django.core.management.base import BaseCommand
import requests

class Command(BaseCommand):
    help = "Display hello"
    def handle(self, *args: Any, **options: Any) -> str | None:
        auth_endpoint = "http://127.0.0.1:8000/auth/"
        username = input("Username: ")
        password = input("Password: ")
        auth_response = requests.post(auth_endpoint, json={'username': username, 'password': password})
        if auth_response.status_code == 200:
            print(auth_response.json()['token'])
        else:
            print("Something went wrong")