# OJL3

**Online Judge Layer 3**

## The layers

I'm making an online judge. It will have 4 layers:

1. frontend (HTML, CSS, JS)
2. backend web-framework (probably Django)
3. layer 3 (python)
4. safeexec

This repository contains the 3rd layer. It's purpose is to take in the interpreter/compiler name, source code, input data and resource limits and run the script/program to get output. It then gives verdict (AC, WA, TLE, RTE, etc.).

The 4th layer is currently [ochko's safeexec](https://github.com/ochko/safeexec).

Currently this layer does not use chroot jails.

## DIY

This project's root directory should contain these items (or symlinks to them):

1. OJ_data (directory containing user and problem data)
2. OJ_sandbox (directory where scripts/programs will run)
3. safeexec
4. inprs (directory containing symlinks to interpreters, or wrapper programs)
5. compilers (directory containing symlinks to compilers, or wrapper programs)

More info on these can be found in the 'doc' directory.
