import json


def write_json(data, file):
    with open(file, "w") as json_file:
        json.dump(data, json_file, indent=4)


def add_word(chat_id, word, file):
    with open(file) as json_file:
        data = json.load(json_file)
        chats = data["chat_id"]
        if chat_id not in chats.keys():
            chats[chat_id] = [word]
            write_json(data, file)
            return f"Word {word} has been added to favorites"
        else:
            if word not in chats[chat_id]:
                chats[chat_id].append(word)
                write_json(data, file)
                return f"'{word}' has been added to favorites"
            else:
                return "You've already added this word to favorites"

def remove_words(chat_id, file="words_db.json"):
    with open(file) as json_file:
        data = json.load(json_file)
        chats = data["chat_id"]
        if str(chat_id) in chats.keys():
            chats[str(chat_id)].clear()
            write_json(data, file)
            return "All words have been erased. Press /add_word to add some words."
        else:
            return "It seems that you don't have any saved words."

print(remove_words('23513541'))













