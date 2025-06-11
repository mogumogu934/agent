from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

print("\n------------------------------------------------------------")
print("\nTesting 'functions/get_file_info.py'")
print(get_files_info("calculator", "."))
print(get_files_info("calculator", "pkg"))
print(get_files_info("calculator", "/bin"))
print(get_files_info("calculator", "../"))

print("\n------------------------------------------------------------")
print("\nTesting 'functions/get_file_content.py'")
print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat"))

print("\n------------------------------------------------------------")
print("\nTesting 'functions/write_file.py'")
print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

print("\n------------------------------------------------------------")
print("\nTesting 'functions/run_python_file.py'")
print(run_python_file("calculator", "main.py"))
print(run_python_file("calculator", "tests.py"))
print(run_python_file("calculator", "../main.py"))
print(run_python_file("calculator", "nonexistent.py"))
