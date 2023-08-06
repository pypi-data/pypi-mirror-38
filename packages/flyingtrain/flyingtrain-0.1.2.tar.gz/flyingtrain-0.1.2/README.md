# flyingtrain - Document

Package that uses an iterative parser to retrieve transport models and the total passenger capacity from a long JSON transport list in a txt file

## Installation
This package can be installed with `pip`<br>
Copy-paste and run this command in the terminal
```
pip install flyingtrain
```

## Docker
* This project is also dockerized, [Docker](https://docs.docker.com/install/) needs to be installed to run this project in containerization method.
* The [Dockerfile](Dockerfile) uses ​`python:2`​​ as base image.
* There are some feasible commands as indicated in ​[Makefile​](Makefile), or simply execute ​ `make help`, it will show the Make commands that can be used. (We will go through more in detail later)

## Tool
This project uses [__ijson__](https://pypi.org/project/ijson/) as an iterative JSON parser to avoid dumping the entire data file into memory

## Usage
After installation, the following snippet can be used inside a virtual environment which runs the data extraction
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
Edit the `test_file` in [main.py](main.py#L4) and execute `make run`, the file should be put in the same folder with `main.py`. Volume binding can be used to avoid copying the file, but taking docker as a supplementary solution, it's not implemented here.

## benchmark
The following command is used in the terminal to show how much time it takes to retrieve the data
```
python -m timeit -s "import flyingtrain" "flyingtrain.extract_data('test.txt')"
```
the result
```
1000 loops, best of 3: 684 usec per loop
```
which means for executing once, it takes around 684 usec<br><br>
_Docker solution_<br>
Edit the `test_file` in [benchmark.py](benchmark.py#L4) and execute `make runbenchmark`, the file should be put in the same folder with `benchmark.py`. Again, volume binding is not implemented here.<br>
the result
```
[0.6676740646362305, 0.6634271144866943, 0.6310489177703857]
```
which means measuring execution time with 3 repeats counts and each count with 1000 executions, and for average it takes 663 usec per execution

## Possible optimizations
* First, for __benchmarking__, the build-in module `timeit` is used here. There are also some third party packages can be used such as [__memory_profiler__](https://pypi.org/project/memory_profiler/) for monitoring memory consumption of a process as well as line-by-line analysis.
* Second, when the record amounts scale up, and the model sets of distinct transports keep increasing, that one can take tons of memory and CPU if we still do it naively by keeping a set of the counts for every model around. There's streaming approximate algorithms for this such as [HyperLogLog](https://en.wikipedia.org/wiki/HyperLogLog).
* Last but not least, the format of the datasets. Protocol buffers and recordio, or even Cap'n Proto will be a good try. It's a binary storage format which is faster to parse, and resilient to corruption (recordio files are checksummed, and can skip damaged section without losing the whole file.)
