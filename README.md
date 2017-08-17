#### LegUp Parameter Autotuner

This repository contains an autotuner for LegUp's
parameters, using metrics obtained before and
after Quartus place-and-route.

##### Dependencies

You will need to install [Docker](https://docs.docker.com/engine/installation/) and
[OpenTuner](http://opentuner.org/tutorial/setup/) before setting up.

##### Building the Docker Image

Use our [Dockerfile](https://github.com/phrb/legup-dockerfile/blob/master/ubuntu_legup_quartus/Dockerfile)
to build the Docker image containing LegUp, GXemul and Altera Quartus Prime. The image also
contains a copy of CHStone applications ready for tuning. To use Altera Quartus Prime you will
need to modify the Dockerfile to export and configure your license. Additional instructions to configure
Docker for building the image are available at our [Dockerfile repository](https://github.com/phrb/legup-dockerfile).

##### Running the Autotuner

After installing the dependencies and building the Docker image you are ready
run the post place-and-route autotuner. To do that with default settings,
go to the `post_place_and_route/py` directory and run:

```
$ ./run.sh
```

You can change tuning run settings by modifying the `run.sh` script.
The autotuner is configured to run CHStone applications.
