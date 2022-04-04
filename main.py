import requests
import json
import random
import string
from database import create_db_conn, close_db_conn, update_points

def get_movies_list():
    request = requests.get('https://imdb-api.com/en/API/MostPopularMovies/k_9679z0s8')
    content = request.content.decode('utf-8')
    json_data = json.loads(content)
    movies_list = set()
    for movie_details in json_data['items']:
        movies_list.add(movie_details['title'])
    return movies_list


def populate_positions(movie_name):
    positions_dict = dict()
    for index, data in enumerate(movie_name.lower()):
        if data not in positions_dict:
            positions_dict[data] = [index]
        else:
            positions_dict[data].append(index)
    return positions_dict


def select_user():
    conn, curr = create_db_conn()
    query = 'Select * from public.users_hangman'
    user_list = []
    results = curr.execute(query)
    for i in curr.fetchall():
        user_list.append(i[0])
    close_db_conn(conn, curr)
    return random.choice(user_list)


def main():
    user = select_user()
    movies_list = list(get_movies_list())
    system_movie_name = random.choice(movies_list)
    positions_dict = populate_positions(system_movie_name)
    user_movie_name = ['_']*len(system_movie_name)
    for index, data in enumerate(system_movie_name):
        if data not in string.ascii_letters:
            user_movie_name[index] = system_movie_name[index]
    print(''.join(user_movie_name))
    incorrect_count = 5
    while 1:
        char = input('Enter the character     ')
        if char.lower() in ''.join(user_movie_name).lower():
            print('This character is already inserted. Please select any new character')
            print(''.join(user_movie_name))
            continue
        elif char not in positions_dict:
            print('This character does not exist in the movie')
            print(''.join(user_movie_name))
            incorrect_count -= 1
            if incorrect_count == 0:
                print(f'You could not guess the movie name {system_movie_name} in alloted attempts')
                update_points(user, -10)
                break
        else:
            positions = positions_dict[char]
            for i in positions:
                user_movie_name[i] = char
            if '_' not in user_movie_name:
                print(f'Bingo!! You have successfully guessed the movie, {system_movie_name}')
                update_points(user, 10)
                break
            else:
                print(''.join(user_movie_name))


if __name__ == '__main__':
    main()