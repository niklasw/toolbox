install
cdrom

# Root password (set to: password)
# Change that using "openssl passwd -1" to generate MD5 encrypted passwd
rootpw --iscrypted $1$aJLs93Tp$ABMS/915M1H7vqM/hcAom1
# System authorization information
auth --useshadow --enablemd5

# System locale
timezone --utc Europe/Stockholm
keyboard --vckeymap=us --xlayouts=us
lang en_US.UTF-8

# Clear the Master Boot Record
zerombr
# Partition clearing information
clearpart --all --initlabel
# Disk partitioning information
# /boot must be outside LVM
part /boot --fstype ext4 --size=500 --asprimary
part swap --size 2000 --asprimary
part pv.01 --fstype ext4 --size=1 --grow --asprimary
volgroup VolGroup00 pv.01
logvol / --fstype ext4 --name=lv_root --vgname=VolGroup00 --size=1 --grow

# check repodata/*Fedora*comps.xml online for a list
%packages
@Core
#@Basic Desktop
#@GNOME
%end
