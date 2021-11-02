CC=gcc
CFLAGS=-I. -O0 -g -Wall -std=c++17
LDFLAGS=-lm -lstdc++
SOURCES=main.cpp \
        OrderProcessor.cpp \
        OrderBook.cpp
TESTSOURCES=OrderProcessor.cpp \
            OrderBook.cpp \
            Tests.cpp
VALGRINDFLAGS=--leak-check=full \
              --error-exitcode=1 \
              --tool=memcheck \
              --track-origins=yes \
              --errors-for-leak-kinds=definite \
              --show-leak-kinds=definite \
              --quiet
%.o: %.c
	$(CC) $(CFLAGS) -o $@ -c $<

#.PHONY : build
build: build_match_engine
build_match_engine: ## Kicks off a build
	mkdir -p build
	$(CC) $(CFLAGS) -o build/match_engine $(SOURCES) $^ $(LDFLAGS)

tests: build_match_engine match_engine_tests valgrind
match_engine_tests: ## Kicks off a test
	mkdir -p build
	clang-tidy $(CPPFLAGS) -checks=*,-fuchsia*,-llvmlibc*,-modernize*,-readability*,-google*,-altera* --warnings-as-errors=* $(SOURCES) -- -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
	$(CC) $(CFLAGS) -o build/match_engine_tests $(TESTSOURCES) $^ $(LDFLAGS)

valgrind:
	valgrind $(VALGRINDFLAGS) build/match_engine input.txt

.PHONY: clean
clean: ## Cleans the build directory
	rm -rf build/*
