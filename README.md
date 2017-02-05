# Paperless without GPG

This is [Paperless](https://github.com/danielquinn/paperless) but without using GPG.


## How It Works

See the "origin" documentation [there](https://paperless.readthedocs.io/en/latest/).

You can see my changes below, adapted for this setup:
- A NAS that support Docker and SSH (example: [Synology
  DS216+II](https://www.synology.com/en-global/products/DS216+II) )
- A printer that support a transfert protocol that is also supported by your
  NAS.
- They are both disconnected from Internet (optional)


### Setup the NAS

On the NAS, you need to create:
- An `admin` user
- A `paperless` group
- Add the `admin` user into `paperless` group
- A `paperless` user (the password will be used when setting up the Printer)
- A `consumption` directory that can be accessed by the `paperless` group (Read/Write)
- An encrypted `paperless` directory that the `paperless` user cannot access,
  but the `admin` can (more informations
  [there](https://www.synology.com/en-global/knowledgebase/DSM/tutorial/File_Sharing/How_to_encrypt_and_decrypt_shared_folders_on_my_Synology_NAS))


### Setup the Printer

That depend on your Printer and the protocol you are using.


### Let's get started

1. Test that your Printer can scan a file and upload it to the `comsumption`
   directory on your NAS
1. Mount the `paperless` encrypted directory
1. Activate SSH access on your NAS
1. Activate/Install Docker
1. On your computer, generate the Docker Image you'll be using on your NAS:

  ```bash
  $ vagrant up docker
  $ vagrant ssh
  $ cd /opt/paperless
  $ docker build -t <yourname>/paperless:<todaydate> . # replace everything between <>
  $ docker save --output paperless_<todaydate>.tar <yourname>/<todaydate>
  $ exit
  ```

1. Copy the file `paperless_<todaydate>.tar` to your NAS (using ssh/scp for example)
1. Push the `docker-compose.yml.example` and `docker-compose.env.example` where
   you want on your NAS, and remove `.example` extensions
1. Modify the `docker-compose.env` file, and set:

  ```text
  # Connect as admin, and type id to get following ids
  USERMAP_UID=<admin_id>
  USERMAP_GID=<paperless_group_id>
  ```

1. Modify the `docker-compose.yml` file, and modify every occurrences of:

  ```bash
  # irmage: pitkley/paperless
  # to
  image: <yourname>/paperless
  ```

1. In the directory where you put `docker-compose.*` files, run:

  ```bash
  $ docker load --input <path/to/paperless_<todaydate>.tar>
  $ sudo docker-compose run --rm webserver migrate
  $ sudo docker-compose run --rm webserver createsuperuser
  $ sudo docker-compose up -d
  ```

1. If the consumer fail, just restart it:

  ```bash
  $ sudo docker-compose up -d
  ```

1. Now you can open your browser at `http://<nas-ip>:8000`
1. Each time you turn off and on your NAS, you'll need to:
  - decrypt the `paperless` folder
  - launch Docker processes
