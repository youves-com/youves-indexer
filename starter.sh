#!/bin/bash

dipdup -c $1_config.yml run || dipdup -c $1_config.yml schema wipe && dipdup -c $1_config.yml run