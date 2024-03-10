# Vagrant only for development and tests

Vagrant is a tool for building and managing virtual machine environments
in pyvyos we use vagrant to deploy vyos virtual machines
for development and automated tests

If you want to only use pyvyos you dont need to install vagrant

# Vagrant install instructions

1. Install Vagrant
2. Install VirtualBox
3. Install Vagrant plugins
```
vagrant plugin install vagrant-vyos
vagrant plugin install vagrant-dotenv

```
4. Install mkisofs
```
sudo apt install genisoimage
```

5. Run vagrant up
```
vagrant up
```
6. Run vagrant ssh
```
vagrant ssh
```

# For Windows with wsl2:
```
export VAGRANT_WSL_ENABLE_WINDOWS_ACCESS="1"
export PATH="$PATH:/mnt/c/Program Files/Oracle/VirtualBox"
```