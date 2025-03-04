from typing import (
    List,
    Optional,
)
from colorama import (
    Fore,
    Style,
)
import threading
import json
import requests

class Logger:
    def __init__(self):
        self.c = f"{Fore.BLUE}[{Fore.LIGHTBLACK_EX}LOG{Fore.BLUE}]"

    def status(
        self, token: str, message: str, color: str, prefix: Optional[str] = None
    ) -> None:
        print(
            f"{self.c} {Fore.BLUE}{token[:30]}{Style.RESET_ALL} -> {color}{message}"
        )

    def error(self, token: str, message: str, response: str) -> None:
        print(
            f"{self.c} {Fore.BLUE}{token[:30]}{Style.RESET_ALL} -> {Fore.RED}{message}"
        )


class DiscordSpammer:
    def __init__(self):
        self.logger = Logger()
        self.tokens: List[str] = self.load_tokens()

    def load_tokens(self) -> List[str]:
        try:
            with open("tokens.txt", "r") as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(
                "tokens.txt not found"
            )
            return []

    def send_message(self, token: str, channel_id: str, message: str) -> None:
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
        }
        
        response = requests.post(
            f"https://discord.com/api/v10/channels/{channel_id}/messages", 
            headers=headers, 
            json={"content": message}
        )

        if response.status_code == 200:
            self.logger.status(
                token, "Message sent successfully", Fore.GREEN
            )
        else:
            self.logger.error(
                token, "Failed to send message", response.text
            )

    def start_spam(self, channel_id: str, message: str, amount: int, threads: int) -> None:
        def worker(start: int, end: int, tokens: List[str]):
            for i in range(start, end):
                token = tokens[i % len(tokens)]
                self.send_message(token, channel_id, message)

        chunk_size = amount // threads
        thread_list = []

        for i in range(threads):
            start = i * chunk_size
            end = start + chunk_size if i != threads - 1 else amount
            thread = threading.Thread(
                target=worker, 
                args=(start, end, self.tokens)
            )
            thread_list.append(thread)
            thread.start()
        
        for thread in thread_list:
            thread.join()


if __name__ == "__main__":
    spammer = DiscordSpammer()

    channel_id = input(
        f"{Fore.BLUE}Channel > {Style.RESET_ALL}"
    )
    message = input(
        f"{Fore.BLUE}Enter Message > {Style.RESET_ALL}"
    )
    amount = int(
        input(
            f"{Fore.BLUE}Enter Amount > {Style.RESET_ALL}"
        )
    )
    threads = int(
        input(
            f"{Fore.BLUE}Threads > {Style.RESET_ALL}"
        )
    )

    spammer.start_spam(channel_id
                       message
                       amount
                       threads )
