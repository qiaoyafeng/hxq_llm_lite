#!/bin/sh -e
set -x

ruff check hxq_llm_lite --fix
ruff format hxq_llm_lite
