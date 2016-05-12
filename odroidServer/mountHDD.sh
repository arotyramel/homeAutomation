#!/bin/bash
#~ sudo umount /home/odroid/mount
sudo mount -t ext4 /dev/sda2 /home/odroid/mount || sudo mount -t ext4 /dev/sdb2 /home/odroid/mount
