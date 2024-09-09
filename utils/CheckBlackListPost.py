file_path = "data/black-list-post.txt"
def check_black_list_post(post):
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip() == post:
                return True
    with open(file_path, 'a') as file:
        file.write(post + '\n')
    return False