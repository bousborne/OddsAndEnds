#!/bin/bash
docker build -t gemini_interview . && docker run -i --rm gemini_interview
