import subprocess
import os
import glob

def clone_community_packages():
    # read the packgaes names
    with open('community.packages', 'r') as f:
        list_of_packages = []
        packages1 = f.readlines()
        for item in packages1:
            # ommit comments
            if(item[0]=="#"):
                pass
            else:
                list_of_packages.append(item.rstrip())

    # download packages
    for item in list_of_packages:
        command = "sudo pacman --noconfirm -Sw "+item
        subprocess.run(command.split())

    # list all files in cache
    cached_packages = os.listdir('/var/cache/pacman/pkg')

    # copy selected packages
    for item in list_of_packages:
        for s in cached_packages:
            if(item.lower() in s.lower()):
                command = "cp /var/cache/pacman/pkg/"+s+" ./x86_64"
                subprocess.run(command.split())

def install_packages():
    os.chdir('x86_64')
    packages = os.listdir('.')
    for package in packages:
        command = "sudo pacman --needed --noconfirm -U "+package
        subprocess.run(command.split())  

def build_aur_packages():
    os.chdir('..')
    pkg_dirs =  glob.glob('./*/')
    # remove x86_64 dir
    pkg_dirs.remove('./x86_64/')
    for repo in pkg_dirs:
        os.chdir(repo)
        # command = "makepkg -fc" # force clean
        command = "makepkg"
        subprocess.run(command.split())
        # list all pkg files
        pkg_files = os.listdir('.')
        for filename in pkg_files:
            if('.pkg.tar.xz'.upper() in filename.upper()):
                command = "cp "+filename+" ../x86_64"
                subprocess.run(command.split())
        os.chdir('..')

def update_repo_list():
    # list all files
    packages = os.listdir('.')
    packages_str = ''
    for p in packages:
        if1 = ('.pkg.tar.xz'.upper() in p.upper())
        if2 = ('.pkg.tar.zst'.upper() in p.upper())
        if if1 or if2:
                packages_str = packages_str+" "+p
    command = "repo-add danjarow.db.tar.gz "+packages_str
    subprocess.run(command.split())


if __name__ == "__main__":
    print("-> Cloning community packages")
    clone_community_packages()
    print("\n\n-> Installing packages")
    install_packages()
    print("-> Building AUR packages")
    build_aur_packages()
    print("\n\n-> Installing packages")
    install_packages()
    print("--> Udpating repository")
    update_repo_list()