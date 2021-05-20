# hpc-project
Distributed HyperParameter Tuning using HPC

# Instructions to run a node

## Change dir after cloning
```cd slave```

## Build the docker
```docker build . -t hpc-slave```

## Run the docker container
```docker run hpc-slave --rm ```

## Kill running nodes 
```docker container kill $(docker ps -q)```