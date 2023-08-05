"""
This is a git commit-hook which can be used to check if huge files
 where accidentally added to the staging area and are about to be
 committed.
If there is a file which is bigger then the given "max_file_size"-
 variable, the script will exit non-zero and abort the commit.
This script is meant to be added as a "pre-commit"-hook. See this
 page for further information:
    http://progit.org/book/ch7-3.html#installing_a_hook
In order to make the script work probably, you'll need to set the
 above path to the python interpreter (first line of the file)
 according to your system (under *NIX do "which python" to find out).
Also, the "git_binary_path"-variable should contain the absolute
 path to your "git"-executable (you can use "which" here, too).
See the included README-file for further information.
The script was developed and has been confirmed to work under
 python 3.2.2 and git 1.7.7.1 (might also work with earlier versions!)
"""
import subprocess, sys, os
import collections, operator, onepanel.utilities.git_utility

# The maximum file-size for a file to be committed:
max_file_size = 5120  # in KiB (= 1024 byte)
max_repo_size = 200*1024 # in KiB, 200 MB
units = 1024.0  # To move up and down between magnitudes of size


def check_for_large_files():
	# Now, do the checking:
	try:
		too_large_files = []
		# In Bytes
		total_size_of_commit = 0
		LargeFile = collections.namedtuple('LargeFile', ['filename', 'size_bytes'])
		print("Checking for files bigger than " + sizeof_fmt(max_file_size * 1024))
		# Check all files in the staging-area:
		text = subprocess.check_output(
			['git', "status", "--porcelain", "-uno"],
			stderr=subprocess.STDOUT).decode("utf-8")
		file_list = text.splitlines()

		# Check all files:
		for file_s in file_list:
			file_name = file_s[3:]
			stat = os.stat(file_name)
			total_size_of_commit += stat.st_size
			if stat.st_size >= (max_file_size * units):
				# File is too big, store it for later analysis
				too_large_files.append(LargeFile(file_name, stat.st_size))

		# Are they trying to commit large files?
		if len(too_large_files) > 0:
			print("You are trying to commit file(s) that are too large.")
			print("Please use a dataset instead of git to store these files.")
			print("Adjust your commit and try again.")
			print("Note that you may visit https://help.onepanel.io/command-line-interface-cli/getting-started-with"
				  "-onepanel-cli for more information.")
			num_files_to_show = 5
			print("Top {to_show} largest files...".format(to_show=num_files_to_show))
			print_top_x_large_files(num_files_to_show, too_large_files)
			sys.exit(1)

		# Is the total commit size greater than 5 mb?
		# This is to prevent thousands of small image files from being committed.
		if total_size_of_commit >= (max_file_size * units):
			print("The total size of your commit is too large, based on the total size of the files being committed.")
			print("Please use a dataset instead of git to store these files.")
			print("Adjust your commit and try again.")
			print("Note that you may visit https://help.onepanel.io/command-line-interface-cli/getting-started-with"
				  "-onepanel-cli for more information.")
			sys.exit(1)

		# Check if the repository size is too big
		git_repo_info = subprocess.check_output(
			['git', "count-objects", "-v"],
			stderr=subprocess.STDOUT).decode("utf-8")
		repo_info_output = text.splitlines()
		size_line = repo_info_output[1]
		kib_info = size_line.split(":")
		kib_val  = int(kib_info[1].strip())
		if kib_val*units >= max_repo_size*units:
			print("The total size of your repository is too large, greater than or equal to 200 MB.")
			print("Please use a dataset instead of git to store these files.")
			print("Note that you may visit https://help.onepanel.io/command-line-interface-cli/getting-started-with"
				  "-onepanel-cli for more information.")
			sys.exit(1)

		# Everything seems to be okay with file sizes
		sys.exit(0)

	except subprocess.CalledProcessError:
		# There was a problem calling "git status".
		print("Error executing git status")
		sys.exit(12)


def sizeof_fmt(num):
	"""
	This function will return a human-readable filesize-string
	 like "3.5 MB" for it's given 'num'-parameter.
	From http://stackoverflow.com/questions/1094841
	"""
	for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
		if num < units:
			return "%3.1f %s" % (num, x)
		num /= units


def print_top_x_large_files(how_many=5, list_of_files=None):
	if list_of_files is None:
		list_of_files = []
	# Sort the list of files by size
	sorted_files = sorted(list_of_files, key=operator.attrgetter('size_bytes'), reverse=True)
	for index, file in enumerate(sorted_files):
		if index == how_many:
			break
		print(
			"{file_name} - ({size_of_file})".format(file_name=file.filename, size_of_file=sizeof_fmt(file.size_bytes)))
