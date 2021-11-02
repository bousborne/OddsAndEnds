# Ben Ousborne

## Quick Glance

***cat sample_input.txt | ./run.sh*** will compile everything and run the match engine using sample_input.txt as the input.

***./test.sh*** will compile everything and run just the tests through the build/match_engine_tests binary

## Minor changes I made to stuff

Tests are now added at the end of Dockerfile. They are ran using catch2. See Tests.cpp to view the actual tests ran.
The result of these tests will be shown automatically when you run "./run.sh".
They will be right above where you are able to input BUY/SELL lines.

Running the "./run.sh" will also automatically run clang-tidy, clang-format, and valgrind.

## How to run

***cat sample_input.txt | ./run.sh*** will compile everything and run the match engine using sample_input.txt as the input.

***./test.sh*** will compile everything and run just the tests through the build/match_engine_tests binary

### Match Enginer
The match_engine can either take a piped input file via 'cat', or it can take no input.
With an input file, it will run the match engine on all lines in the file, while emitting trades.
When it is done all lines, it will then print all remaining trade lines, then terminate the program.

If you want to run it as a continuous program that allows you to individually type each line, run it without pipe.

### Tests
Simply running "./test.sh" on commandline will kick off docker and run the tests that are in Tests.cpp.
The tests are ran using catch2.

## Methodology

The bulk of the code is in OrderProcessor.cpp and OrderBook.cpp.
When main runs, it starts up the OrderProcessor which will wait for orders to come in, then run them through the matcher.
There is a vector of buys and a vector of sells.
If the current order is a buy, then it will compare to the sells vector and vice versa.
When trying to match an order, it will loop through all orders currently in the respective vector list.
It will make comparisons on the price, as well as make sure it is the same "instrument".
If there is a match, the quantities of both sides will be updated, then the current order will be placed in its'
respective vector list if there is still some quantity left.
That list will then be sorted based on a comparator function on price and time.
Being placed at the end takes care of the time precedent.
At a match, a trade will be emitted.
When everything is processed (either the file is at the end, or user types "exit"), then the sell and buy vector contents
are printed as long as there is quantity left.

I was trying real hard to think of a way to decrease time complexity.
I was considering using a map, or set, or something along those lines for the sell and buy vectors to decrease lookup time.
But, I could not think of a good key value, as using prices or instruments would write over previous objects.
Therefore, I stuck with vectors.

I also considered trees to decrease time complexity on lookup, but this is nullified from using 2 variables to sort on.
So, I still stuck with vectors.

## Time

I spent roughly 3 hours on this. The bulk of the developing the actual algorithm was about 1.5 hours.
I got stuck on "how to implement using input parameters vs none" part.
But, it can now be ran with either input.txt containing the lines, or with no paramaters for the user to type them.
Then, I also spent a chunk of time figuring out how to pass the parameters into docker.
This was acheived through the ENTRYPOINT lines in dockerfile with CMD overrides.


# engine-takehome-interview

## Prompt

Your application is a matching engine that receives orders and continuously matches them to see if they can trade. Your application must be implemented in C++ and you should use a modern revision of the C++ standard (e.g., C++17).

The orders that your matching engine shall receive are timestamped upon arrival. Orders are first ranked according to their price; orders of the same price are then ranked depending on the timestamp at entry.

Your application must read orders from stdin in the format described below. As your program reads the orders, it must emit any trades that result from the placement of an order. These trades shall be printed to stdout.

Once the input stream is fully consumed, your application must print all remaining orders that did not fully trade. These orders must also be printed to stdout.

Please note the streaming nature of this input and structure your program accordingly.

## Input Format

Each order shall be delimitted by a new line. Each line consists of an order's `OrderID`, `Side`, `Instrument`, `Quantity` and `Price`, delimitted by a varying quantity of white space. The stream of orders are sequenced chronologically.

### Sample Input

```
12345 BUY BTCUSD 5 10000
zod42 SELL BTCUSD 2 10001
13471 BUY BTCUSD 6 9971
11431 BUY ETHUSD 9 175
abe14 SELL BTCUSD 7 9800
plu401 SELL ETHUSD 5 170
45691 BUY ETHUSD 3 180
```

## Output Format

For each trade produced by your application, your application must print a string followed by a newline. This string must being with the word `TRADE` and be followed by the `Instrument`, `OrderID`, `ContraOrderID`, `Quantity`, and `Price` of the trade.

Once the input stream is fully consumed, your application shall print all orders that remain on each side of every order book. The `SELL` side of each order book shall be printed first; the `BUY` side of each order book shall be printed last. For each side of every order book, orders shall be printed in the order in which they arrived. Note that arrival order is different from each order's price/time priority.

Please ensure that you leave exactly one line of whitespace between each portion of the requested output.

### Sample Output

```
TRADE BTCUSD abe14 12345 5 10000
TRADE BTCUSD abe14 13471 2 9971
TRADE ETHUSD plu401 11431 5 175

zod42 SELL BTCUSD 2 10001
13471 BUY BTCUSD 4 9971
11431 BUY ETHUSD 4 175
45691 BUY ETHUSD 3 180
```

## Submission Requirements

Please submit an archived directory containing the following:
1. All source code and any additional tooling required to build, compile, and test your submission
2. A `README.md` containing the following:
    - your name
    - instructions on how to build and run your application
    - a description of how you approached the problem
    - how long much time you spent on this project
3. A `run.sh` that builds a Docker image and runs your application 
    - Please do not submit precompiled artifacts; your `Dockerfile` must compile your source code when building the container image
4. A `test.sh` that builds a Docker image and runs your tests 
    - Similarly, please do not submit precompiled artifacts

It is of utmost importance that your submission is complete. All submissions lacking any of the above requirements will be rejected on the basis of being incomplete.

You should also showcase your knowledge of modern best practices in application development. Some relevant areas include developing with testings frameworks (like `googletest` or `catch2`), using automatic code formatters (like `clang-format`), and integrating static code analysis tooling (like `clang-tidy`).

## Runtime Requirements

Gemini's Engine Team has provided a barebones project that includes `./run.sh`, a `Dockerfile`, a `Makefile`, and a `main.cpp` which simply echos input. Executing `./run.sh` locally must build and launch a Docker image that defaults to running your application. The `./run.sh` file must accept piped input.

You are free to modify any of this project as you see fit. However, you must provide a `./run.sh` that builds and runs your application in a Docker container. You are not bound to use `FROM debian:10`, however you must use a base image that is available in [Docker Hub](https://hub.docker.com/).

If you would like to add logging to your application please use stderr so that we can discern your log statements from the expected application output.

### Runtime Example

```
$ cat sample_input.txt | ./run.sh
Sending build context to Docker daemon  197.1kB
Step 1/4 : FROM debian:10
 ---> 1b686a95ddbf
Step 2/4 : RUN apt-get -y update   && apt-get -y install build-essential   && apt-get clean
 ---> Using cache
 ---> 165e5b61f3e9
Step 3/4 : COPY src/ /app
 ---> 1e03b684802c
Step 4/4 : RUN cd /app && make build
 ---> Running in c930e5aaa0e9
mkdir -p build
g++ -o build/match_engine main.cpp
Removing intermediate container c930e5aaa0e9
 ---> 40ca2815137b
Successfully built 40ca2815137b
Successfully tagged gemini_interview:latest

====== Match Engine =====

TRADE BTCUSD abe14 12345 5 10000
TRADE BTCUSD abe14 13471 2 9971
TRADE ETHUSD plu401 11431 5 175

zod42 SELL BTCUSD 2 10001
13471 BUY BTCUSD 4 9971
11431 BUY ETHUSD 4 175
45691 BUY ETHUSD 3 180
```
