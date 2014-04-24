#!/usr/bin/python
import os, sys, subprocess, getpass, stat, shutil

editor = 'vim'
dataFile = sys.argv[1]

## make a backup of the encrypted file
bakFile = dataFile+'-gpgedit_backup'
shutil.copy(dataFile, bakFile)
dstat = os.stat(dataFile)

##  create temporary directory in tmpfs to work from
tmpDir = '/dev/shm/gpgedit'
n = 0
while True:
    try:
        os.mkdir(tmpDir+str(n))
        break
    except OSError as err:
        if err.errno != 17:  ## file already exists
            raise
    n += 1
tmpDir += str(n)

os.chmod(tmpDir, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)


try:
    ## Get password
    passwd = getpass.getpass()

    ## decrypt file
    tmpFile = os.path.join(tmpDir, 'data')
    cmd = "gpg -d --passphrase-fd 0 --output %s %s" % (tmpFile, dataFile)
    proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE)
    proc.stdin.write(passwd)
    proc.stdin.close()
    if proc.wait() != 0:
        raise Exception("Error decrypting file.")

    ## record stats of tmp file
    stat = os.stat(tmpFile)

    ## invoke editor
    os.system('%s %s' % (editor, tmpFile))

    ## see whether data has changed
    stat2 = os.stat(tmpFile)
    if stat.st_mtime == stat2.st_mtime and stat.st_size == stat2.st_size:
        raise Exception("Data unchanged; not writing encrypted file.")

    ## re-encrypt, write back to original file
    cmd = "gpg --yes --symmetric --passphrase-fd 0 --output %s %s" % (dataFile, tmpFile)
    proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE)
    proc.stdin.write(passwd)
    proc.stdin.close()
    if proc.wait() != 0:
        raise Exception("Error encrypting file.")
except:
    ## If there was an error AND the data file was modified, restore the backup.
    dstat2 = os.stat(dataFile)
    if dstat.st_mtime != dstat2.st_mtime or dstat.st_size != dstat2.st_size:
        print "Error occurred, restored encrypted file from backup."
        shutil.copy(bakFile, dataFile)
    raise
finally:
    shutil.rmtree(tmpDir)
    os.remove(bakFile)
