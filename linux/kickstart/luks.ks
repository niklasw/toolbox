# set boot drive to sda
bootloader --location=mbr --timeout=5 --boot-drive=sda
# only use the sda disk
ignoredisk --only-use=sda
# clear the Master Boot Record
zerombr
# don't use clearpart as that would wipe the partitions created in %pre
part /boot --asprimary --fstype="ext4" --ondisk=sda --onpart=sda1 --size=500 --grow --label=/boot
part / --asprimary --fstype="ext4" --ondisk=sda --onpart=sda2 --size=50000 --grow --label=/
%include /tmp/part-include
%pre --interpreter /bin/sh

# switch to tty3 so we can see what happens
exec < /dev/tty3 > /dev/tty3 2>&1
chvt 3

# find disk device in system - first found, first used
disk_device=""
for file in 'sda' 'hda' 'vda'; do
        if [ -e "/sys/block/$file" ]; then
                disk_device="$file"
                break
        fi
echo "Found disk device: $disk_device"
done

# wipe partitions
for partition in `parted -s /dev/$disk_device print|awk '/^ / {print $1}'`; do
        echo "Deleting $disk_device partition: $partition"
        parted -s /dev/$disk_device rm $partition
done

# create new optimally aligned partitions - use MiB or GiB!
parted -s -a optimal /dev/$disk_device mklabel msdos
parted -s -a optimal /dev/$disk_device mkpart primary ext4 1MiB 501MiB
parted -s -a optimal /dev/$disk_device mkpart primary ext4 501MiB 51GiB
parted -s -a optimal /dev/$disk_device mkpart primary ext4 51GiB 100%

echo "Parted - check alignment of partition 1:"
parted /dev/$disk_device align-check optimal 1
echo "Parted - check alignment of partition 2:"
parted /dev/$disk_device align-check optimal 2
echo "Parted - check alignment of partition 3:"
parted /dev/$disk_device align-check optimal 3

# wipe the partition to be used as a luks encrypted partition
# slow method is more secure but very slow
dd if=/dev/urandom of=/dev/sda3
# faster but less secure
#badblocks -c 10240 -s -w -t random -v /dev/sda3

# set passphrase for encrypted luks device
# could also use something like https://myhost/genpass.php
mypass="testpass"
echo "mypass: $mypass"
echo ""

echo "Setup /dev/sda3 as luks device"
echo -ne "$mypass" | cryptsetup -v -q luksFormat /dev/sda3 -
cryptsetup -v isLuks /dev/sda3 && echo cryptsetup luksFormat: Success

echo ""
luksuuid=`cryptsetup luksUUID /dev/sda3`
echo "luks UUID: $luksuuid"
diskuuid=`blkid -s UUID -o value /dev/sda3`
echo "disk UUID: $diskuuid"

# generate the proper part line with the luks uuid
echo "part /home/niklas --asprimary --fstype=luks --ondisk=sda --onpart=UUID=$luksuuid --size=150000 --grow --noformat --label=/home/niklas --encrypted --passphrase='$mypass'" > /tmp/part-include

echo "Opening device luks-sda3"
echo -ne "$mypass" | cryptsetup -v -q luksOpen /dev/sda3 luks-sda3 -

echo "Info about device luks-sda3"
dmsetup info luks-sda3

echo "Create ext4 filesystem on luks-sda3"
mkfs.ext4 -q -v -L /home/niklas /dev/mapper/luks-sda3

# create entry in /etc/crypttab:
echo 'echo "" >> /etc/crypttab' > /tmp/luks-include
echo 'echo "# kickstart: add luks device" >> /etc/crypttab' >> /tmp/luks-include
echo "echo "luks-sda3 UUID=$diskuuid none allow-discards luks" >> /etc/crypttab" >> /tmp/luks-include
echo 'chmod 744 /etc/crypttab' >> /tmp/luks-include
echo 'chown root:root /etc/crypttab' >> /tmp/luks-include

# create entry in /etc/fstab
echo 'echo "" >> /etc/fstab' >> /tmp/luks-include
echo 'echo "# kickstart: add luks device" >> /etc/fstab' >> /tmp/luks-include
echo "echo "/dev/mapper/luks-sda3 /home/niklas ext4 defaults 0 0" >> /etc/fstab" >> /tmp/luks-include

# change back to tty1
chvt 1
%end
