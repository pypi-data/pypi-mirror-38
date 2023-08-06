# -*- coding: utf-8 -*-
# This file is part of finchan.

# Copyright (C) 2017-present qytz <hhhhhf@foxmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import sys
import json
import asyncio
import logging
import datetime
import logging.config

import click
import uvloop

from .env import Env
from .exts import ExtManager
from .options import load_configs
from .dispatcher import BackTrackDispatcher, LiveDispatcher


@click.command()
@click.option(
    "-v", "--verbose", count=True, help="Count output level, can set multipule times."
)
@click.option("-c", "--config", help="Specify config file.")
def main(verbose=0, config=None):
    """Console script for finchan

    Copyright (C) 2017-present qytz <hhhhhf@foxmail.com>

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Project url: https://github.com/qytz/finchan
    """
    env = Env()
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    env.verbose = verbose
    if not config:
        conf_path = os.path.expanduser("~/.finchan/config.yml")
    else:
        conf_path = config
    try:
        env.options = load_configs(conf_path)
    except (SyntaxError, TypeError) as e:
        print("Parse configure file failed, please check: %s" % e)
        return

    work_dir = os.path.expanduser(env.options.get("work_dir", "~/.finchan"))
    os.makedirs(work_dir, exist_ok=True)
    os.makedirs(os.path.join(work_dir, "logs"), exist_ok=True)
    os.chdir(work_dir)
    log_config = env.options.get("log_config", {})
    # patch the log filter parameters
    if "filters" in log_config and "finchan" in log_config["filters"]:
        log_config["filters"]["finchan"]["env"] = env
    logging.config.dictConfig(log_config)
    if env.options["run_mode"] == "backtrack":
        env.run_mode = "backtrack"
    else:
        env.run_mode = "live_track"

    root_logger = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(tracktime)s %(levelname)-8s %(message)s")
    )
    if verbose > 0:
        handler.setLevel("DEBUG")
    else:
        handler.setLevel("INFO")
    root_logger.addHandler(handler)

    root_logger.info("Run in %s mode", env.run_mode)
    if env.run_mode == "backtrack":
        dispatcher_config = env.options.get("dispatcher.backtrack", {})
        dispatcher = BackTrackDispatcher(env, **dispatcher_config)
        enabled_exts = env.options.get("enabled_backtrack_exts", [])
    else:
        dispatcher_config = env.options.get("dispatcher.live_track", {})
        dispatcher = LiveDispatcher(env, **dispatcher_config)
        enabled_exts = env.options.get("enabled_live_exts", [])

    extm_args = env.options["ext_manager"]
    if not extm_args:
        extm_args = {}
    ext_manager = ExtManager(env, **extm_args)
    env.set_dispatcher(dispatcher)
    env.set_ext_manager(ext_manager)

    env.load_exts(enabled_exts)
    env.run()


if __name__ == "__main__":
    main()
