import requests
import random
import json

with open("config.json", "r") as config_file:
    config = json.load(config_file)

base_url = "http://127.0.0.1:8000/api"


def get_jwt_token(username, password):
    response = requests.post(
        f"{base_url}/login/", data={"username": username, "password": password}
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
        return token
    else:
        print(f"Failed to get JWT token for user {username}.")
        return None


def signup_users():
    for i in range(1, config["number_of_users"] + 1):
        username = f"user{i}"
        password = f"password{i}"

        response = requests.post(
            f"{base_url}//signup/",
            json={"username": username, "password": password},
        )

        if response.status_code == 201:
            print(f"User {username} signed up successfully")
        else:
            print(f"Error signing up user {username}", response.status_code)


def simulate_user_activity(user_id, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    num_posts = random.randint(1, config["max_posts_per_user"] + 1)

    for _ in range(num_posts):
        post_content = f"Post by user {user_id} - {random.randint(1, 100)}"
        response = requests.post(
            f"{base_url}/posts/create/",
            json={"content": post_content},
            headers=headers,
        )

        if response.status_code == 201:
            print(
                f"User {user_id} created a post {post_content.split('-')[1]}"
            )
        else:
            print(f"Error creating a post for user {user_id}")


def simulate_post_likes(user_id, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    num_likes = random.randint(1, config["max_likes_per_user"] + 1)

    posts = requests.get(f"{base_url}/posts/", headers=headers).json()

    for _ in range(num_likes):
        post_id = random.randint(1, len([post for post in posts]))

        response = requests.patch(
            f"{base_url}/posts/{post_id}/like/",
            json={"user": user_id},
            headers=headers,
        )

        if response.status_code == 200:
            print(f"User {user_id} liked post {post_id}")
        else:
            print(f"Error liking post {post_id} for user {user_id}")


# Main function
if __name__ == "__main__":
    signup_users()

    for i in range(1, config["number_of_users"] + 1):
        username = f"user{i}"
        password = f"password{i}"
        token = get_jwt_token(username, password)
        simulate_user_activity(i, token)

    for i in range(1, config["number_of_users"] + 1):
        username = f"user{i}"
        password = f"password{i}"
        token = get_jwt_token(username, password)
        simulate_post_likes(i, token)
