#!/bin/bash

docker service scale test_stack_go=1

docker service scale test_stack_nestjs=1