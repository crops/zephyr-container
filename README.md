Zephyr Build Container
========================
This repo is to create an image that is able to setup and use a Zephyr build environment.

Running the container
---------------------
* **Determine the workdir**

  The workdir you create will be used for all output from the Zephyr  build
  system as well as where your workspace will be saved. You can either
  create a new directory or use an existing one.

  *It is important that you are the owner of the directory.* The owner of the
  directory is what determines the user id used inside the container. If you
  are not the owner of the directory, you may not have access to the files
  the container creates.

  For the rest of the instructions we'll assume the workdir chosen was
  `/home/myuser/workdir`.

* **The docker command**

  Assuming you used the *workdir* from above, the command
  to run a container for the first time would be:

  ```
  docker run --rm -it -v /home/myuser/workdir:/workdir crops/zephyr-container \
  --git "-b branch_name http://some/git/repo.git target_directory"
  ```
  Let's discuss some of the options:
  * **-v /home/myuser/workdir:/workdir**: The default location of the workdir
    inside of the container is /workdir. So this part of the command says to
    use */home/myuser/workdir* as */workdir* inside the container.
  * **--git "-b branch_name http://some/git/repo.git target_directory"**:
    This is the url of the Zephyr OS git repo. The kernel source will be
    automatically downloaded and prepared to use inside of the
    target_directory.
    Substitute in the url, branche_name and target_directory  for whatever
    Zephyr OS git repo, branch and directory you want to use.

  You should see output similar to the following:

  ```
  $docker run --rm -it -v /home/user/zephyr-build/:/workdir crops/zephyr-container --git "-b master https://gerrit.zephyrproject.org/r/zephyr zephyr-src"
  Attempting to clone -b master https://gerrit.zephyrproject.org/r/zephyr zephyr-src
  Cloning into 'zephyr-src'...
  remote: Counting objects: 10518, done
  remote: Finding sources: 100% (98219/98219)
  remote: Total 98219 (delta 62422), reused 98006 (delta 62422)
  Receiving objects: 100% (98219/98219), 39.75 MiB | 2.87 MiB/s, done.
  Resolving deltas: 100% (62422/62422), done.
  Checking connectivity... done.
  zephyruser@e6fc72513005:/workdir$

  ```
  At this point you should be able to use the shell to build Zephyr apps.

  Source the project environment file to set the project environtment
  variables:

  ```
  $ cd ./zephyr-src
  ```

  Source the project environment file to set the project environtment
  variables:

  ```
  $ source zephyr-env.sh
  ```

  Build the example project, enter:

  ```
  $ cd $ZEPHYR_BASE/samples/hello_world/

  $ make
  ```

* **Using a previous workdir**

  In the case where you have previously cloned the Zephyr git repo you will
  no longer need to specify the *--git* argument when starting the container.

  So the following command:
  ```
  docker run --rm -it -v /home/myuser/workdir:/workdir crops/zephyr-container
  ```
  on a previously setup workdir, should generate output similar to:
  ```
  zephyruser@a2968550e11d:/workdir$
  ```

Building the container image
----------------------------
If for some reason you want to build your own image rather than using the one
on dockerhub, then run the command below in the directory containing the
Dockerfile:

```
docker build -t crops/zephyr-container .
```

The argument to `-t` can be whatever you choose.
