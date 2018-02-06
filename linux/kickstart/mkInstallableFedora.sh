#!/usr/bin/env bash

[[ -f "$1" ]] || { echo "Need iso file arg"; exit 1; }

MNT=/mnt/iso

[[ -d "$MNT" ]] || { mkdir $MNT; }

ISO_FILE=$1
ISO_DIR=$(mktemp -d /tmp/iso_XXXX)
VOLUME_NAME=C7CFDnC
ISO_NAME=${VOLUME_NAME}.iso
SNIP_FILE=/tmp/edits

mount -t iso9660 -o loop $ISO_FILE $MNT

rsync -a $MNT/ $ISO_DIR/

umount $MNT


cat << EOF > $SNIP_FILE
Add the following to isolinix/isolinux.cfg
------------------------------------------
label $VOLUME_NAME
  menu label ^Install Centos 7 with kickstart
  kernel vmlinuz
  append initrd=initrd.img ks=http://masami01.foi.se/ksC7nami.cfg inst.stage2=hd:LABEL=$VOLUME_NAME

EOF
echo ''
cat << EOF >> $SNIP_FILE

Add the following to EFI/BOOT/grub.cfg
--------------------------------------
menuentry 'Install Centos 7 CFD' --class fedora --class gnu-linux --class gnu --class os {
        linuxefi /images/pxeboot/vmlinuz inst.stage2=hd:LABEL=$VOLUME_NAME
        initrdefi /images/pxeboot/initrd.img

EOF

cat << EOF >> $SNIP_FILE
And edit the search line in EFI/BOOT/grub.cfg

search --no-floppy --set=root -l '$VOLUME_NAME'

EOF


read -p "Now, to edit files in $ISO_DIR, press enter"
gvim -o $ISO_DIR/isolinux/isolinux.cfg $ISO_DIR/EFI/BOOT/grub.cfg $SNIP_FILE
read -p "Now, to finish, press enter"

xorriso -as mkisofs -D -r -J -joliet-long -l \
        -V $VOLUME_NAME \
        -b isolinux/isolinux.bin \
        -c isolinux/boot.cat \
        -iso-level 3 \
        -no-emul-boot \
        -partition_offset 16 \
        -boot-load-size 4 \
        -boot-info-table \
        -isohybrid-mbr /usr/share/syslinux/isohdpfx.bin \
        -o $ISO_NAME \
        $ISO_DIR

echo -e "\n\n\tDONE"
echo -e "Manually remove $ISO_DIR"
echo -e "Then use 'dd if=$ISO_NAME of=/dev/sdX bs=1M && sync' to transfer image to usb"

