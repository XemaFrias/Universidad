#!/bin/bash
WHAT=$(dialog --backtitle $0 --output-fd 1 --checklist 'Select items to uncompress:\n\nSPACE: check/uncheck     TAB: changes focus     INTRO: accept\nMouse can also be used, if supported by your terminal emulator.' 16 76 26 README 'Read this before doing anything else' off ChangeLog 'History of changes' off usr/include/ 'C/C++ headers' off usr/share/backgrounds/ 'Backgrounds for X desktop environments' off usr/share/pixmaps/ 'X11 pixmaps' off usr/share/man/ 'Manual pages' off)
SIZE=$(stat --printf=%s $0)
dir1=$PWD
dir2=$(dialog --output-fd 1 --inputbox "Enter directory " 8 46)
if [ -n "$WHAT" ]; then
	if [ -n "$dir2" ]; then
	  (tail -n +8 $0 | pv -n -s $SIZE -i 0.25 | base64 -d | tar --directory=$dir2 -xzf - $WHAT) 2>&1 | dialog --gauge 'Uncompressing...' 8 46
	else
	  (tail -n +8 $0 | pv -n -s $SIZE -i 0.25 | base64 -d | tar --directory=$dir1 -xzf - $WHAT) 2>&1 | dialog --gauge 'Uncompressing...' 8 46
	fi
fi
exit 0;
H4sIAAAAAAAAA+3UwU6DQBAGYK7yFONJjbFhKVD11mg1Rr009e62jLBmZQkLqfTpXWptNMb0VJsm
/3dZAsMMC8yMR8Prx5G3VYGTRFG3ikEcfF+XRBx5oh/1RRwmQeLOi1BEiUfBdh/rU2NrWRF5r1Kb
khfZX3Gbru+pSa4sjZc/Ac2lJVXMdJNy6g6ozplMpTJVSE3P/M7VTFmOezY/ohel2QXImlrTUGrm
hTbS3dcjusplkfGDyZYJpbamy1Tx4a73Cr+tP9YWa2zq/1DE6/4fCOH6vx9EAv3/H254SmEgLi7p
jBZcqLpddm3FpZYzNwamLaXKbT2j48nT3Yl/QC5wNSTIvkmtqZRt1/vdxPg5JHx/WFZd9vMue2P5
q0JtqKzYclHT7eT+dFXB+rt+GQAAAAAAAAAAAAAAAAAAAAB76AOdzqHwACgAAA==
