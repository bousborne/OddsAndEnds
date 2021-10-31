#!/bin/bash
docker build -t gemini_interview . && docker run -i -t --rm gemini_interview
