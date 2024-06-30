# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.0] - 6/30/2024

### General

- Models now use pydantic.
- Rewrote package to no longer depend on serverjars.com.

## [1.3.0] - 4/14/2024

Sadly due to unforeseen circumstances, serverjars.com is down and will not be back online. Thankfully the CDN server is still up which this update introduces. Because of this, some functions may behave differently.

### Changes

- Renamed all functions to be snake_case.
- Some methods now require "type".

## [1.2.0] - 8-27-2023

### General

- renamed `file` argument to `fp` in downloadJar method.
- Jar `built` uses datetime.
- Renamed `thread` to `block` in downloadJar
- downloadJar will now return Jar unless block=False

## [1.1.0] - 4-20-2023

- Breaking Change! package has been renamed from `ServerJars` to `serverjars`.
- constants are no longer enums.
- \_type now uses fetchTypes instead of a data set.
- Improved method docs.
- Added `finishcommand` to downloadJar. Once jar has been downloaded it will call this function.

## [1.0.1] - 9-5-2022

- Fixed `ServerJars.fetchTypes()`
- Added example.py

## [1.0.0] - 9-5-2022

- initial release
