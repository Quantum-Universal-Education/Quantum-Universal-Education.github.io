---
title: Quantum Lab
categories:
  - Blog
tags:
  - Qiskit
  - Q#
  - Quantum computing
  - PennyLane
  - Quantum Lab
  - Docker
  - Simulator
  - Framework
  - QLM
  - Tutorial
author:
  - Michael Rollin
  - Curate Section
  - Alberto Maldonado Romo Q
---


A simple docker image to simulate a full *Quantum laboratory*

## Abstract
We are at the beginning of the run for the quantum supremacy and quantum independent of the different worldwide government. More and more companies are building their own quantum computer with their own library/language. Some of these allow to connect to multiple quantum computers and other are specializes for one type of computer. Also, some libraries are very specified for some kind of task like PennyLane for Quantum Machine Learning (QML). 

For these reason it begins  complicated to set up a clear unique environment to develop with each quantum technologies or to switch between each others. This article is about the setup of a simple multi-Docker image, allowing to build a clean environment for each technology's known and a sharable volume to share the content between the host computer and the different container.

## Table of content
1. [Pre-requisites](#prereqisites)
2. [What's Docker ?](#docker)
3. [How does it work](#working)  
	3.1. [Building image](#image)  
	3.2. [Create container](#container)  
	3.3. [Run everything together](#run)
4. [Future](#future)
5. [Annexes](#annexes)
6. [References](#ref)

## 1. Pre-requisites <a class="anchor" id="prereqisites"></a>
First to be able to run the lab, you need to install Docker[[6]](#6), that's the only requirement needed :
- <details><summary>Linux</summary>
  <pre>apt-get install docker-ce docker-ce-cli containerd.io
  Refer to https://docs.docker.com/engine/install/ubuntu/</pre>
</details>

- <details><summary>Mac / Windows</summary>
  https://www.docker.com/products/docker-desktop
</details>


## 2. What is Docker <a class="anchor" id="docker"></a>

<table border=0>
	<tbody>
		<tr>
			<td width=66%><a href="https://www.docker.com/">Docker</a> is a technology allowing OS virtualization and system simulation. It allows to generalize a simple application with its whole environment into a deployable package to be share and run everywhere on every computer supporting Docker. This package is calling a container, the container is OS-level virtualization and every container share their own kernel. Moreover, the container is fully isolated from the host application.</td>
			<td align="center">![/assets/images/Mica_QLab/container-what-is-container.png](/assets/images/Mica_QLab/container-what-is-container.png)</td>	
	</tbody>
</table>

## 3. How does it work <a class="anchor" id="working"></a>

<table border=0>
	<tbody>
		<tr>
			<td>![/assets/images/Mica_QLab/ql.PNG(/assets/images/Mica_QLab/ql.PNG)</td>
			<td>The role of the image is to simulate a virtual environment as a Quantum lab for a specialized library/language. Another need is to synchronize the data between the container of the host computer. <br /> Like this, we could develop our code on our favorite IDE on our classical computer and run the code directly in the container. <br /><br /> Download the code : <b><a href="https://github.com/mickahell/quantum_lab">Github</a></b></td>
		</tr>
	</tbody>
</table>

### 3.1. Build the image <a class="anchor" id="image"></a>
First we need to build the image, we have to generate a docker image from our `Dockerfile` by using : 
<pre>docker build --build-arg quantum_env=qiskit.sh -t quantum_lab .</pre>
Feel free to replace `qiskit.sh` with `qml.sh`, `qsharp.sh`, `simulaqron.sh` or `myqlm.sh`. That'll set up a specialized environment for each library/language. This command can take several minutes, do not stop it until the command gave you the hand back.

#### Pre-build images
Pre-build images for each environment are available in the [Docker Hub](https://hub.docker.com/search?q=mickahell%2Fquantum&type=image) :
- `quantum_lab_qiskit`
- `quantum_lab_qml`
- `quantum_lab_qsharp`
- `quantum_lab_simulaqron`
- `quantum_lab_myqlm`

You can download them by using : `docker pull mickahell/[IMAGE_NAME]` (ex. `quantum_lab_qiskit`)  
To not have any problem with the following tutorial I suggest you to rename the image as `quantum_lab` by using : <pre>docker image tag mickahell/[IMAGE_NAME]:latest quantum_lab:latest</pre>

Now if you tape `docker images` you'll be able to see your image :
<pre>
REPOSITORY                     TAG       IMAGE ID       CREATED       SIZE
quantum_lab                    latest    73cc092474d1   3 weeks ago   1.48GB
mickahell/quantum_lab_qiskit   latest    73cc092474d1   3 weeks ago   1.48GB
ubuntu                         18.04     329ed837d508   4 weeks ago   63.3MB
</pre>

### 3.2. Create container <a class="anchor" id="container"></a>
Now we have our image `quantum_lab`, you can see it by taping `docker images`. Next we need to set up a container who we be our virtual environment. We can create as much container as the stockage of our computer allows it.

#### Volume
To sync data between the container and the host computer we need to create a volume, by default in the image a simple volume is created between the default docker sharing folder of the host and the `/opt/quantum_lab/data/share` folder. To make things easier we can specify which folder of our host we want to sync by using `-v [YOUR_FOLDER]:/opt/quantum_lab/data/share` during the creation of the container.

#### Jupyter
In each environment Jupyter notebook is available, to synchronize it with our host browser we need to sync port network to do this just use the option `-p 8888:8888` in the container creation. Then a script allow you to start a Jupyter server : `/opt/quantum_lab/data/start_jupyter.sh`.  
Finally, just go in your browser and tap : `http://127.0.0.1:8888/`


### 3.3. Run everything together <a class="anchor" id="run"></a>
To create our container and to be allowed using volume sync and jupyter you can use this simple command line :
<pre>docker run -it -v $(pwd)/data:/opt/quantum_lab/data/share --entrypoint=/bin/bash -p 8888:8888 -e LANG=C.UTF-8 quantum_lab</pre>

## 4. Future <a class="anchor" id="future"></a>
We are at the very beginning of the quantum era, so that means the already installed quantum technologies will have updated very often and more and more libraries and languages will be coming soon. So the image will be updated as often as possible and more environment will be soon available as a new option.

The goal is to make everything possible to keep the image as simple as possible to use and to set up. Pre-build  image are already available in the [Docker Hub](https://hub.docker.com/search?q=mickahell%2Fquantum&type=image), allowing to just download the image and create container, so no need to clone the project and build entirely the images anymore.

Also, the experiences part will be externalized in another GitHub repository and download automatically in the build phase, in order to keep the Docker image clean without too much _random_ data.

If you have an idea of features do not hesitate and create an **[issue](https://github.com/mickahell/quantum_lab/issues/new)**.

## 5. Annexes <a class="anchor" id="annexes"></a>
### Environment details

- Library's (libs) common for every env :  ```networkx, numpy, matplotlib, notebook, pandas, scipy, tk, vim```
- 4 libs setup are available, one for installating Qiskit[[1]](#1), one for using Pannylane[[2]](#2), one for using Q#[[3]](#3), one for SimulaQron[[4]](#4), and one for myQLM[[5]](#5)
  - `qml.sh`
    - Libs : ```autograd, pennylane, pennylane-sf, pennylane-qiskit```
  - `qiskit.sh`
    - Libs : ```qiskit, qiskit[visualization]```
  - `qsharp.sh`
    - Libs : ```qsharp, iqsharp```
  - `simulaqron.sh`
    - Libs : ```simulaqron```
  - `myqlm.sh`
    - Libs : ```myqlm, libmagickwand-dev, myqlm-interop[qiskit_binder]```

All the libs setup scripts are available in the folder `/opt/quantum_lab/build` inside the image, some of the libs can live together and some cannot (ex. `qiskit` and `pennylane-qiskit` can't).

#### Protocols for experiencing Quantum
**COMING SOON !**

### Hello world!
*Hello world* program for each environment are available inside the image in the data folder and allow to test the quantum laboratory.

### Simple docker commands
- List the existed images : `docker images`
- List the existed container : `docker ps -a`
  - The `-a` is used to show every existed containers, that's include the stopped one
- To start a container : `docker start [CONTAINEUR_ID]`
- To go inside a started container : `docker exec -it -u root [CONTAINEUR_ID] /bin/bash`
- Delete container : `docker rm [CONTAINEUR_ID]`
- Delete stopped container : `docker container prune`
- Delete image : `docker rmi [NAME_OF_THE_IMAGE]`
  - You can use `-f` to force the suppression and delete the containers associated to the image
- List the existed volume : `docker volume ls`
- Delete volume not used anymore : `docker volume prune`

## 6. References <a class="anchor" id="ref"></a>
<a id="1">[1]</a> [Qiskit](https://qiskit.org): An Open-source Framework for Quantum Computing, 2019, [DOI: 10.5281/zenodo.2562110](10.5281/zenodo.2562110)  
<a id="2">[2]</a> [Pennylane](https://pennylane.ai): Automatic differentiation of hybrid quantum-classical computations, 2018, [DOI: arXiv:1811.04968](https://arxiv.org/abs/1811.04968)  
<a id="3">[3]</a> [Q#](https://azure.microsoft.com/fr-fr/resources/development-kit/quantum-computing/): The Microsoft Quantum Development Kit Preview, 2017   
<a id="4">[4]</a> [Simulaqron](http://www.simulaqron.org/): A simulator for developing quantum internet software, 2018, [DOI: 10.1088/2058-9565/aad56e](https://doi.org/10.1088/2058-9565/aad56e)  
<a id="5">[5]</a> [AQASM](https://atos.net/en/lp/myqlm): Atos Quantum Assembler, 2021, [DOI: arXiv:2102.12973](https://arxiv.org/abs/2102.12973)  
<a id="6">[6]</a> [Docker](https://www.docker.com), An introduction to Docker for reproducible research, 2015, [DOI: 10.1145/2723872.2723882](https://doi.org/10.1145/2723872.2723882)

## Author
Michaël Rollin, [GitHub](https://github.com/mickahell), [Twitter](https://twitter.com/mickahell89700), [Linkedin](https://www.linkedin.com/in/michaelrollin/)  
### Cite as
If you use my work, please cite as : <pre>Quantum Lab: Docker image for quantum laboratory, Michaël Rollin, 2021, DOI: <a href=https://doi.org/10.5281/zenodo.4664195>10.5281/zenodo.4664195</a></pre>
