# Build Firmware

## Toolchain Setup

To build MicroPython firmware for the ESP8266 you'll need to first build the ESP open SDK toolchain that can compile code for the ESP8266's processor.  You could manually compile and install this SDK on your computer, however it's much easier to use a small virtual machine running Linux to compile and use the toolchain.  This way you can use the ESP open SDK from any computer regardless of it running Windows, Mac OSX, or even Linux, and you can keep the SDK's tools in an environment that's isolated and won't conflict with any other development tools on your machine.

## Dependencies

1. [VirtualBox](https://www.virtualbox.org/) - This is open source virtualization software that is a free download.
1. [Vagrant](https://www.vagrantup.com/) - This is an open source wrapper around VirtualBox which makes it easy to create and run a virtual machine from the command line.  Vagrant is also free to download.
1. [Git](http://git-scm.com/) - Source control system used to download the configuration for this project.  Git is also free and open source.

## Provision Virtual Machine

To create and provision the virtual machine you'll need to download a Vagrant configuration file.  This file defines what operating system to install (Ubuntu 14.04) and some commands to prepare the operating system for building the ESP SDK.
Start by opening a command line terminal (in Windows make sure to open a 'Git Bash' command window as you'll need to use Git commands) and run the following command to clone the repository for this project and navigate inside it:

```bash
git clone https://github.com/adafruit/esp8266-micropython-vagrant.git
cd esp8266-micropython-vagrant
```

Now 'turn on' the virtual machine by running this command:

```bash
vagrant up
```

The first time the 'vagrant up' command runs it will take a bit of time as it downloads the operating system image, but later 'vagrant up' commands will be faster as the OS image is cached internally.

If you see an error go back and make sure you've installed both VirtualBox and Vagrant.  Also make sure you're executing the command from inside the cloned repository's directory, there should be a file named Vagrantfile inside the directory you're running these commands from.

Once the virtual machine is running you can enter a Linux command terminal on it by executing the command:

```bash
vagrant ssh
```

After a moment you should be at an Ubuntu Linux command prompt that looks something like:

```bash
vagrant@vagrant-ubuntu-trusty-64:~$
```

## Compile ESP Open SDK

Once inside the virtual machine you'll first need to compile the ESP open SDK.  The SDK source code has already been downloaded in the esp-open-sdk subdirectory during the virtual machine provisioning.  You just need to change to the directory and execute a command to make the project.  Run the following commands:

```bash
cd ~/esp-open-sdk
make STANDALONE=y
```

Note that the compilation will take a bit of time.  On my machine compilation took about 30 minutes, but on an older or slower machine it might take an hour or more.  Luckily you only need to compile the ESP open SDK once and then can quickly build MicroPython using the compiled SDK tools.

If you see the compilation fail with a different error then there might be a problem with the ESP open SDK.  Try checking the github issues for it to see if there is a known issue with the error you received.

Now the ESP open SDK is compiled and you're almost ready to build MicroPython (or any other ESP8266 code you'd ever like to compile).  First though you need to add the ESP open SDK tools to the virtual machine's path so MicroPython can find them.  Run this command to update the .profile file that runs whenever you log into the virtual machine:

```bash
echo "PATH=$(pwd)/xtensa-lx106-elf/bin:\$PATH" >> ~/.profile
```

To make this updated path available log out and back in to the virtual machine by running:

```bash
exit
vagrant ssh
```

Once logged in again you should see your path environment variable has the ESP open SDK tools in it.  You can check this by running the command:

```bash
echo $PATH
```

You should see a path value that looks something like this (notice the esp-open-sdk tools in the path):

`/home/vagrant/esp-open-sdk/xtensa-lx106-elf/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games`

Remember you only need to perform the ESP open SDK compilation steps above once in the virtual machine.

## Compile MicroPython Firmware

Next you can build the MicroPython firmware for the ESP8266.  Make sure you've followed all the steps above and have a virtual machine running and the ESP open SDK compiled.

The MicroPython source code has already been downloaded to the micropython folder during the virtual machine provisioning.  However you need to run a small git command to pull in external dependencies before you can build it.  To install this dependency and then start the compilation execute the following commands inside the virtual machine:

```bash
cd ~/micropython
git submodule update --init
make -C mpy-cross
cd ~/micropython/ports/esp8266
make axtls
make
```
The MicroPython library compilation should be quick and only take a few minutes at most.

Once finished the output will be the file `./build/firmware-combined.bin`.  In the next section you'll walk through how to load the firmware on an ESP8266 board, however first you'll need to copy the firmware bin file out of the virtual machine.  Luckily Vagrant has a special directory inside the virtual machine which can be used to copy files between the virtual machine and the host computer running Vagrant.  Execute the following command to copy out the firmware bin file to this shared folder:

```bash
cp ./build/firmware-combined.bin /vagrant/
```

Now exit the virtual machine by running the following command:

```bash
exit
vagrant halt
exit
```

The BIN File is in `C:\Users\User\esp8266-micropython-vagrant\`

