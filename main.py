#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Basic Web traffic generator that probes links on a provided URL.

Copyright (c) {{current_year}} Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               
               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""

__author__ = "Russell Johnston <rujohns2@cisco.com>"
__copyright__ = "Copyright (c) 2022 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

import time
import logging
import random

import click
import requests
from bs4 import BeautifulSoup
from rich import print
from rich.logging import RichHandler


def get_links(raw_input):
    # Find all the http or https links on a given Webpage
    parsed_html = format_html(raw_input)
    links = []
    for link in parsed_html.findAll("a"):
        href = link.get("href")
        # Filter links that start with http or https and add to links
        if href.startswith("https://"):
            links.append(href)
        elif href.startswith("http://"):
            links.append(href)
    return links


def format_html(raw_html):
    parse_html = BeautifulSoup(raw_html, "html.parser")
    return parse_html


@click.command()
@click.argument("url")
@click.option("--sleep", default=5, help="wait time between probing discovered links")
@click.option("-l", "--log", default="INFO", help="set logging level")
def main(url, sleep, log):

    # Define Logger
    LOG_FORMAT = "%(message)s"
    logging.basicConfig(
        level=log.upper(),
        format=LOG_FORMAT,
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, tracebacks_suppress=[click])],
    )
    log = logging.getLogger("rich")

    "Take the target URL and get all links present on site"
    target_html = requests.get(url)
    site_links = get_links(target_html.text)

    "Add the target URL to the returned list of links"
    site_links.append(url)

    log.info("Links found >>> \n {0}".format(site_links))

    try:
        # Loop infinite over returned links. Links tried randomly
        while True:
            query = requests.get(random.choice(site_links))
            log.info("{0} > {1}".format(query.url, query.status_code))
            time.sleep(sleep)
    except KeyboardInterrupt:
        log.info("TERMINIATING: Ctrl-C entered")
        pass


if __name__ == "__main__":
    print("To Terminate press CTRL-C")
    main()
