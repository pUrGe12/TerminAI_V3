# import subprocess
# import yaml

# DESC_YAML_FILE = "/home/purge/Desktop/TerminAI/TerminAI_V3/TerminAI/data/commands.yaml"

# """
# This is the structure of the YAML file

# ```yaml
# Command: ls
# 	desc: list directory contents
# 	flags: List information about the FILEs (the current directory by default).  Sort entries alphabetically if none of -cftuvSUX nor --sort is specified.
# 		flag_1: -a
# 			desc: do not ignore entries starting with .
# 		flag_2: --author
# 			desc: with -l, print the author of each file
# Command: cd
# 	desc: ...
# 	...
# ```
# """

# all_commands = subprocess.run(
#     ["bash", "-c", "compgen -c | grep -v '^_'"],
#     stdout=subprocess.PIPE,
#     text=True
# )

# all_commands = all_commands.stdout.splitlines()

# for cmd in all_commands:
# 		print(f"This is the command: {cmd}")
# 		resp = subprocess.Popen(
# 		f"./man_page.sh {cmd}",
# 		stdout = subprocess.PIPE,
# 		text = True,
# 		shell = True
# 		)

# 		output_lines = [i.strip() for i in resp.stdout if i != ""]

# 		if "No man page found for" not in output_lines:
# 		# These might or might not be present
# 		flag_x_letter, flag_single_letter, flag_multi_letter = "", "", ""

# 		if output_lines:
# 			for ind, line in enumerate(output_lines):
# 				# print(line.strip())
# 				if line.strip().startswith("DESCRIPTION"):
# 					desc = output_lines[ind+1].strip()
# 					print(f"This is the command desc: {desc} \n\n")
# 				elif line.strip().startswith("-") or line.strip().startswith("--"):		
# 					if len(line.strip().split(",")) > 1 and line.strip().split(",")[1].strip().startswith("--"):
# 						# This confirms its like this: "-a, --all"
# 						flag_single_letter = line.strip().split(",")[0]
# 						flag_multi_letter = line.strip().split(",")[1]
# 						flag_desc = output_lines[ind+1].strip()
# 					elif len(line.strip().split(",")) > 1 and not line.strip().split(",")[1].strip().startswith("--"):
# 						# This means something like "--si   likewise, but use powers of 1000 not 1024"
# 						flag_x_letter = line.strip().split(",")[0].split(" ")[0] if " " in line.strip().split(",")[0] else line.strip().split(",")[0]
# 						flag_desc = "".join(line.strip().split(",")[0].split(" ")[1:])
# 					elif len(line.strip().split(",")) == 1:
# 						flag_x_letter = line.strip().split(",")[0]
# 						flag_desc = output_lines[ind+1].strip()

# 					if flag_x_letter:
# 						print(f"This is flag_x_letter: {flag_x_letter}")
# 					if flag_multi_letter:
# 						print(f"This is flag_multi_letter: {flag_multi_letter}")
# 					if flag_single_letter:
# 						print(f"This is single flag: {flag_single_letter}")
					
# 					print(f"This is the DESCRIPTION: {flag_desc} \n\n\n")

# 					flag_x_letter, flag_single_letter, flag_multi_letter = "", "", ""
# 		else:
# 			print(f"Ignoring command: {cmd}")

# Alright now we have this ready. Need to make a yaml file out of this


# Attempt 1

# import subprocess
# import yaml

# DESC_YAML_FILE = "/home/purge/Desktop/TerminAI/TerminAI_V3/TerminAI/data/commands.yaml"

# all_commands = subprocess.run(
#     ["bash", "-c", "compgen -c | grep -v '^_'"],
#     stdout=subprocess.PIPE,
#     text=True
# ).stdout.splitlines()

# commands_list = []

# for cmd in all_commands:
#     print(f"Checking command: {cmd}")
#     resp = subprocess.Popen(
#         f"./man_page.sh {cmd}",
#         stdout=subprocess.PIPE,
#         text=True,
#         shell=True
#     )

#     output_lines = [i.strip() for i in resp.stdout if i.strip()]
#     command_data = {"Command": cmd}
#     flags = {}

#     if output_lines and "No man page found for" not in output_lines[0]:
#         description = ""
#         for ind, line in enumerate(output_lines):
#             if line.startswith("DESCRIPTION"):
#                 if ind + 1 < len(output_lines):
#                     description = output_lines[ind + 1]
#                 command_data["desc"] = description

#             elif line.startswith("-") or line.startswith("--") and not line.startswith("---"):
#                 flag_line = line
#                 flag_desc = output_lines[ind + 1] if ind + 1 < len(output_lines) else ""

#                 if ',' in flag_line:
#                     parts = [p.strip() for p in flag_line.split(",")]
#                     for p in parts:
#                         flags[p] = {"desc": flag_desc}
#                 else:
#                     parts = flag_line.split()
#                     if len(parts) > 1:
#                         flags[parts[0]] = {"desc": " ".join(parts[1:])}
#                     else:
#                         flags[flag_line] = {"desc": flag_desc}

#         if flags:
#             command_data["flags"] = flags

#         commands_list.append(command_data)

# with open(DESC_YAML_FILE, "w") as f:
#     yaml.dump(commands_list, f, sort_keys=False, default_flow_style=False)

# print("done")

# Attempt 2

import subprocess
import yaml
import os

DESC_YAML_FILE = "/home/purge/Desktop/TerminAI/TerminAI_V3/TerminAI/data/commands.yaml"

# Dictionary to store all commands and their information
commands_data = {}

all_commands = subprocess.run(
    ["bash", "-c", "compgen -c | grep -v '^_'"],
    stdout=subprocess.PIPE,
    text=True
)
all_commands = all_commands.stdout.splitlines()

for cmd in all_commands:
    print(f"Processing command: {cmd}")
    resp = subprocess.Popen(
        f"./man_page.sh {cmd}",
        stdout=subprocess.PIPE,
        text=True,
        shell=True
    )
    output_lines = [i.strip() for i in resp.stdout if i != ""]
    
    if "No man page found for" not in " ".join(output_lines):
        command_info = {"desc": "", "flags": {}}
        flag_count = 0
        
        if output_lines:
            for ind, line in enumerate(output_lines):
                if line.strip().startswith("DESCRIPTION") and ind + 1 < len(output_lines):
                    command_info["desc"] = output_lines[ind+1].strip()
                    print(f"Found description for {cmd}: {command_info['desc']}")
                
                elif line.strip().startswith("-") or line.strip().startswith("--"):
                    flag_x_letter, flag_single_letter, flag_multi_letter = "", "", ""
                    flag_desc = ""
                    
                    if len(line.strip().split(",")) > 1 and line.strip().split(",")[1].strip().startswith("--"):
                        # Format like "-a, --all"
                        flag_single_letter = line.strip().split(",")[0].strip()
                        flag_multi_letter = line.strip().split(",")[1].strip()
                        flag_name = flag_multi_letter  # Prefer the long form for naming
                        if ind + 1 < len(output_lines):
                            flag_desc = output_lines[ind+1].strip()
                    
                    elif len(line.strip().split(",")) > 1 and not line.strip().split(",")[1].strip().startswith("--"):
                        # Format like "--si   likewise, but use powers of 1000 not 1024"
                        parts = line.strip().split(",")[0].strip().split(None, 1)
                        flag_x_letter = parts[0]
                        flag_name = flag_x_letter
                        if len(parts) > 1:
                            flag_desc = parts[1]
                        else:
                            flag_desc = ""
                    
                    elif len(line.strip().split(",")) == 1:
                        parts = line.strip().split(None, 1)
                        flag_x_letter = parts[0]
                        flag_name = flag_x_letter
                        if len(parts) > 1:
                            flag_desc = parts[1]
                        elif ind + 1 < len(output_lines):
                            flag_desc = output_lines[ind+1].strip()
                    
                    # Add flag to the command info
                    if flag_name:
                        flag_count += 1
                        flag_key = f"flag_{flag_count}"
                        command_info["flags"][flag_key] = {
                            "name": flag_name,
                            "desc": flag_desc
                        }
                        print(f"Found flag for {cmd}: {flag_name} - {flag_desc}")
        
        # Add command to the data structure if we found information
        if command_info["desc"] or command_info["flags"]:
            commands_data[cmd] = command_info
        else:
            print(f"No useful information found for command: {cmd}")
    else:
        print(f"Ignoring command: {cmd} - No man page found")

# Format the data in the desired YAML structure
formatted_data = {}
for cmd_name, cmd_info in commands_data.items():
    cmd_entry = {"desc": cmd_info["desc"]}
    
    # Add flags with proper formatting
    if cmd_info["flags"]:
        cmd_entry["flags"] = {}
        for flag_key, flag_info in cmd_info["flags"].items():
            cmd_entry["flags"][flag_key] = flag_info["name"]
            cmd_entry["flags"][f"{flag_key}_desc"] = flag_info["desc"]
    
    formatted_data[cmd_name] = cmd_entry

# Create directory if it doesn't exist
os.makedirs(os.path.dirname(DESC_YAML_FILE), exist_ok=True)

# Write to YAML file
with open(DESC_YAML_FILE, 'w') as yaml_file:
    yaml.dump(formatted_data, yaml_file, default_flow_style=False)

print(f"YAML file successfully created at {DESC_YAML_FILE}")