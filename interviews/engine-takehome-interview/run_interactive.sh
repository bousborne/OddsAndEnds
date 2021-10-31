#!/bin/bash
#docker build -t gemini_interview_tests . && docker run -i -t --rm gemini_interview_tests
docker build -t gemini_interview . && docker run -i -t --entrypoint /app/build/match_engine_tests --rm gemini_interview