import subprocess

# cmd = 'sudo pacman -S | pacman -Slq danjarow'
cmd = "pacman -Slq danjarow"
s = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
packages = s.read().decode().splitlines()
packages_str = ""
for p in packages:
    packages_str += " "+p
cmd = "sudo pacman -S"+packages_str
subprocess.run(cmd.split())