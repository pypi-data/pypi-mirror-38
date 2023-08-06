# jxctl
A Command line interface for Jenkins.

## Installation

    `pip install jxctl`

## Commands

| Command | Description                                         | Usage                    |
|---------|-----------------------------------------------------|--------------------------|
| version | Version and info about `jxctl`                      | `jxctl version`          |
| context | Jenkins instance called as a `context` in `jxctl`. It provides set Jenkins context and infomation about the context | `jxctl context [OPTIONS] COMMAND [ARGS]...` |
| get | `get` provides you the functionality to get the resources like *jobs*, *pluings*, *folders*, *builds* list with *count* | `jxctl get [OPTIONS] COMMAND [ARGS]...`|

### context
    Examples:
    `jxctl context set --url <Jenkins URL>`
    `jxctl context set --url <Jenkins URL> --name <Context Name> --user <Username> --token <Password/Access Token>`
    `jxctl context info`
### get
    Examples:
    `jxctl get jobs --all`
    `jxctl get jobs --maven --freestyle --count`
    `jxctl get pluings`

## Releases
| Verson | Description | Status |
|--------|-------------|--------|
| 0.0.1  | <ul><li>Initial Release</li><li>Just Started</li><li>Minumum Requirement</li></ul> | Released|

## Contribution 
We are happy to accept PR's. Those who are interested in contribution please have a look at below functional area's which are needed.

    * Testing
    * Docs
    * Fine-Tuning
