FROM debian:10
RUN apt-get -y update \
  && apt-get -y install build-essential valgrind clang-tidy\
  && apt-get clean
COPY src/ /app
RUN cd /app && make clean && make build
COPY src/runTests.sh /usr/local/bin/runTests.sh
RUN chmod +x /usr/local/bin/runTests.sh
ENTRYPOINT ["/app/build/./match_engine"]