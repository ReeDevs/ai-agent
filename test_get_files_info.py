from functions.get_files_info import get_files_info

def format_result(directory_label, result):
    indented = "\n".join("    " + line for line in result.split("\n"))
    return f"Result for '{directory_label}' directory:\n{indented}"

print(format_result("current", get_files_info("calculator", ".")))
print(format_result("pkg", get_files_info("calculator", "pkg")))
print(format_result("/bin", get_files_info("calculator", "/bin")))
print(format_result("../", get_files_info("calculator", "../")))
