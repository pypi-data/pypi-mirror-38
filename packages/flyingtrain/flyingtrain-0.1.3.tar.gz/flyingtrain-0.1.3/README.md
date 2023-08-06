# flyingtrain - Document

Use an iterative parser to retrieve transport models and total passenger capacity from long JSON transport list in a .txt file

## Installation
This project is packaged with Python 2, and can be installed with `pip`. Copy-paste and run this command in the terminal:
```
pip install flyingtrain
```

## Docker (supplementary solution)
* This project is also dockerized. [Docker](https://docs.docker.com/install/) needs to be installed to run this project in containerization method.
* The [Dockerfile](Dockerfile) uses ​`python:2`​​ as base image.
* There are some feasible commands as indicated in ​[Makefile​](Makefile), or simply execute ​ `make help`, it will show the Make commands that can be used. (We will go through more in detail later)

## Tool
This project uses [__ijson__](https://pypi.org/project/ijson/) as an iterative JSON parser to avoid dumping the entire data file into memory

## Usage
After installation, the following snippet can be used inside a virtual environment to extract the data
```py
import flyingtrain

test_file = 'test.txt'  # the full path of the file

flyingtrain.extract_data(test_file)
```
the result
```sh
(flyingtrain) chuhsuan@ubuntu:~/Desktop$ python
Python 2.7.12 (default, Nov 12 2018, 14:36:49)
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import flyingtrain
>>> flyingtrain.extract_data('test.txt')
"planes": 524
"trains": 150
"cars": 14

"distinct-cars": 3
"distinct-planes": 2
"distinct-trains": 1
```
_Docker solution_<br>
Copy the data file to the root folder, assign the file name to [test_file](main.py#L4) in `main.py` and execute `make run`. Volume binding can be used like [this line](Makefile#L10) in Makefile to avoid copying the file, but it's not implemented here while taking docker as a supplementary solution.<br>

_the result of the docker solution_
```sh
chuhsuan@ubuntu:~/git/flyingtrain$ make run
docker build \
	-t chuhsuanlee/flyingtrain \
	.
Sending build context to Docker daemon  61.44kB
Step 1/5 : FROM python:2
 ---> 3c43a5d4034a
Step 2/5 : WORKDIR /usr/src
 ---> Using cache
 ---> 37e4d0e02609
Step 3/5 : COPY requirements.txt /usr/src/
 ---> Using cache
 ---> 85ae12b2a6f6
Step 4/5 : RUN pip install -r requirements.txt
 ---> Using cache
 ---> 9d33ec10c044
Step 5/5 : ENTRYPOINT ["python", "main.py"]
 ---> Using cache
 ---> e3d261a60154
Successfully built e3d261a60154
Successfully tagged chuhsuanlee/flyingtrain:latest
docker run \
	--rm -v /etc/localtime:/etc/localtime -v /home/chuhsuan/git/flyingtrain:/usr/src \
	chuhsuanlee/flyingtrain
"planes": 524
"trains": 150
"cars": 14

"distinct-cars": 3
"distinct-planes": 2
"distinct-trains": 1
```

## Benchmark
The following command is used in the terminal to show how much time it takes to retrieve the data
```sh
python -m timeit -s "import flyingtrain" "flyingtrain.extract_data('test.txt')"
```
the result
```
1000 loops, best of 3: 684 usec per loop
```
which means it takes around 684 usec for executing once<br>

_Docker solution_<br>
Assign the file name to [test_file](benchmark.py#L4) in `benchmark.py` and execute `make runbenchmark`. Again, volume binding is not implemented here, so the file should be put under the root folder.<br>

_the result of the docker solution_
```
[0.6676740646362305, 0.6634271144866943, 0.6310489177703857]
```
which means measuring execution time with 3 repeats counts and each count with 1000 executions. For average it takes 654 usec per execution

## Possible optimizations
* First, for __benchmarking__, the build-in module `timeit` is used here. There are also some third party packages can be used such as [__memory_profiler__](https://pypi.org/project/memory_profiler/) for monitoring memory consumption of a process as well as line-by-line analysis.
* Second, when the record amounts scale up, and the __model sets of distinct transports__ keep increasing, that one can take tons of memory and CPU if we still do it naively by keeping a set of the counts for every model around. There's streaming approximate algorithms for this such as [__HyperLogLog__](https://en.wikipedia.org/wiki/HyperLogLog).
* Last but not least, the __format of the datasets__. [__Protocol buffers__](https://developers.google.com/protocol-buffers/) and [__recordio__](http://mesos.apache.org/documentation/latest/recordio/), or even [__Cap'n Proto__](https://capnproto.org/) will be a good try. It's a binary storage format which is faster to parse, and resilient to corruption. (recordio files are checksummed, and can skip damaged section without losing the whole file)
