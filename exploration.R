library(tidyverse)
library(jsonlite)
library(purrr)

raw_playlists <- read_json("data/Playlist1.json")

View(raw_playlists)
