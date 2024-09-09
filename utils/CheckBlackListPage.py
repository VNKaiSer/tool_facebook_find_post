file_path = "data/black-list-page.txt"
def check_black_list_page(page):
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip() == page:
                return True
    with open(file_path, 'a') as file:
        file.write(page + '\n')
    return False