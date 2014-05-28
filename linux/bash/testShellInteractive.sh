#!/bin/bash
#  But, as John points out:
#    if [ -t 0 ] works ... when you're logged in locally
#    but fails when you invoke the command remotely via ssh.
#    So for a true test you also have to test for a socket.

if [[ -n $PS1 ]]
then
  echo interactive by PS1
else
  echo non-interactive by PS1
fi

if [[ -t "$fd" ]]
then
  echo interactive by fd0
else
  echo non-interactive by fd0
fi

case $- in
*i*)    # interactive shell
  echo interactive by i
;;
*)      # non-interactive shell
  echo non-interactive by i
;;
esac
