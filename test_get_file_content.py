from functions.get_file_content import get_file_content

print(f"lorem.txt length: {len(get_file_content("calculator", "lorem.txt"))}")
print(f"lorem.txt truncated: {'truncated' in get_file_content("calculator", "lorem.txt")}")
print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat.py"))
print(get_file_content("calculator", "pkg/does_not_exist.py"))
