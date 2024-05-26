import re
import os
import json
import config

exclude_files = [
    "autofill_information",
    "community_chats_settings",
    "messenger_contacts_you've_blocked",
    "secret_conversations",
    "secret_groups",
    "support_messages",
    "your_cross-app_messaging_settings",
]


# Retrieved from https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python
def remove_emojis(data):
    emoji = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002500-\U00002BEF"  # chinese char
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u2640-\u2642"
        "\u2600-\u2B55"
        "\u200d"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"  # dingbats
        "\u3030"
        "/[!@#$%^&*]/g"
        "\n"
        "\s+"
        "]+",
        re.UNICODE,
    )
    return re.sub(emoji, "", data)


def scrape_messenger_data(path, sender_name):
    json_files = []

    for root, _, f_names in os.walk(path):
        for f in f_names:
            if not any(substr in f for substr in exclude_files):
                json_files.append(os.path.join(root, f))

    raw_dataset = []

    for json_file in json_files:
        with open(json_file, "r") as input_file:
            data = json.load(input_file)

            for message in data["messages"]:
                if message.get("content"):
                    sender = message.get("sender_name")
                    content = remove_emojis(
                        message.get("content").encode("latin_1").decode("utf-8")
                    )

                    if (
                        sender == sender_name
                        and content
                        and content not in config.exclude_texts
                        and not content.startswith("https")
                        and not content.startswith("http")
                        and not content.startswith("bit.ly")
                    ):
                        raw_dataset.append(content)

    with open("dataset.txt", "w") as output_file:
        for data in raw_dataset:
            output_file.write(f"{data}\n")
