FROM debian:10
RUN apt-get -y update \
  && apt-get -y install build-essential clang-tidy\
  && apt-get clean
COPY src/ /app
RUN cd /app && make clean && make build
ARG run_test_string=" ===============================================================================\n\
                                    RUNNING ALL CATCH2 TESTS                           \n\
         ===============================================================================\n"
ARG done_run_test_string=" ===============================================================================\n\
                               COMPLETED RUNNING ALL CATCH2 TESTS                      \n\
         ===============================================================================\n"
RUN echo $run_test_string && /app/build/match_engine_tests && echo $done_run_test_string
ENTRYPOINT ["/app/build/./match_engine", "/app/input.txt"]
# ENTRYPOINT ["/app/build/./match_engine"]