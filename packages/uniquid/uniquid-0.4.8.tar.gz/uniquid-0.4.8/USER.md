# Uniquid User Guide

The command line interface for Uniquid system administration.  The Uniquid IAM
(Identity and Access Management) system leverages blockchain technology so that
your organization can efficiently control access to large pools of IoT devices.

   > **Warning**
   >
   > The Uniquid command line interface is currently in development and undergoing
   > test.  Please do not use the tool in production as information may be lost.
   > Contact Uniquid about organizing an evaluation or demonstration of this
   > innovative technology.

   > **Warning**
   >
   > The Uniquid command line interface is currently untested on ***Windows***
   > platforms.

The package currently supports Python 3.6 and later.  Please upgrade to the
latest version of Python if you are running an older version.


## Table of Contents
- [Installation Instructions](#installation-instructions)
- [Getting Started](#getting-started)
- [Viewing Devices](#viewing-devices)
- [Contracts](#contracts)
- [Sharing Access to Devices](#sharing-access-to-devices)
- [Getting Help](#getting-help)
- [Contact Uniquid](#contact-uniquid)


## Installation Instructions

Verify that *Python 3* is installed on your system. You should have at least
***version 3.6*** of Python installed.  You can query the version installed using
the command:

```
    $ python --version
```

If you do not have Python installed, please follow the instructions for your
operating system:

Operating System | Download Instructions
---------------- | ---------------------
Windows | [Python3 for Windows](https://docs.python.org/3/using/windows.html)
MacOS | [Python3 for Mac](https://docs.python.org/3/using/mac.html)
Linux | [Python3 for Unix](https://docs.python.org/3/using/unix.html)

Once *Python* is installed, you can use the `pip3` or `pip` tool to install the
latest version of the CLI client.

   > **Note**
   >
   > The `pip` packaging tool for *Python3* may be called `pip3` on your
   > system, depending on your operating system.  Please check your system
   > instructions on how to execute the `pip` tool for *Python 3*.

```
    $ sudo pip3 install uniquid
```

or

```
    $ sudo pip install uniquid
```

If correctly installed with no errors, the CLI client application can
be executed from the command line.

```
    $ uniquid --version
```

## Getting Started

The user can access a list of the available commands, using the `help`
option.

```
    $ uniquid --help
```

Each command also provides more detailed help information. For example:

```
    $ uniquid login --help
```

Some commands have a shorter alias available.  You can view the list of
available command aliases using the command:

```
    $ uniquid list-aliases
```

In order to login to the Uniquid system, the user must provide:
* a credentials file which was downloaded during registration

or:
* their registered organization name
* their Uniquid username
* the secret *Access Key* which was provided to them during registration

The `login` command will keep an authenticated session open until the user uses
the `logout` command to close the session or their session expires.

### Login using the credentials file

During account registration, the user is given the option to download a
credentials file to their system. This file contains information such as
their unique *Access Key* which enables them to connect to the Uniquid
system.  This credentials file should be stored securely on their system with
read and write privileges only granted to trusted users.

The user should save the credentials file to the following location:

Operating System | File Path
---------------- | -----------------------
Windows | `%USERPROFILE%\.uniquid\credentials.json`
MacOs | `~/.uniquid/credentials.json`
Linux | `~/.uniquid/credentials.json`

Once the credentials file is saved to the correct location, the `login` command
will automatically detect the user's credentials.  To `login`, the user should
use the command:

```
    $ uniquid login
```

If the user prefers not to save the credentials file to the default location
as described above, they can pass the location of the credentials file as
an option on the command line.  Therefore, the command to `login` is:

```
    $ uniquid login --credentials-file <credentials file path>
```

### Login without a credentials file

For the first `login`, the user must specify the organization, their username
and the *Access Key* which they were assigned.

```
    $ uniquid login <organization> --user <username> --access-key 'abcd5678'
```

The organization name must always be specified for the initial login. After the
initial `login`, the user does not need to specify the organisation unless they
want to `login` for a different organization.  They need only specify their
username and the Access key.

```
    $ uniquid login --user <username> --access-key 'abcd5678'
```

If the user prefers not to enter their username and *Access Key* every time they
use the `login` command, they can use environment variables to hold the values
of the username and *Access Key*.

In the *Bash* shell, the environment variables can be set using the following
commands:

```
    $ export UNIQUID_USER=<username>
    $ export UNIQUID_ACCESS_KEY=<access key>
```

### Login status and logout

At any point, the user can query the status of the tool's connection to the
Uniquid servers. In order to query their login status, the user can use the
command:

```
    $ uniquid status
```

When the user is finished interacting with the Uniquid system, they should then
`logout` from their open session.

```
    $ uniquid logout
```

## Viewing Devices

A list of connected devices can be viewed using the command:

```
    $ uniquid list-devices
```

This command, by default, outputs the device list in text format.  If you would
prefer to view the device list in JSON format:

```
    $ uniquid list-devices --output json
```

The entries in the list of devices can be sorted by the values of one of
the fields of the device information. The device list is sorted using the command:

```
    $ uniquid list-devices --sort <key name>
    $ uniquid list-devices --sort-desc <key name>
```

Detailed information on a specific device can be retrieved, using the device's
public key XPUB as an identifier.

```
    $ uniquid show-device <device xpub>
    $ uniquid show-device --output json <device xpub>
```

An example of a command to view detailed information about a single IoT
device:

```
    $ uniquid show-device tpubDGDkliuherf34hSGSDG57652DSFDSFDksdfkjsdf434fgD
```

## Contracts

Access contracts which permit interactions between devices can be created,
viewed and revoked using the client tool.

```
    $ uniquid list-contracts
    $ uniquid list-contracts --output json
```

More detailed information on the state of a contract can also be retrieved,
using the contract's transaction identifier to identify the contract.

```
    $ uniquid show-contract <transaction id>
    $ uniquid show-contract --output json <transaction id>
```

An example of a command to view information about a single Uniquid Access
Contract:

```
    $ uniquid show-contract ebaef8fdf1645032010e801fad010338d2048fa3e67154d660545b4eb9b01c58
```

New contracts can be specified in JSON format and created by the tool. The
JSON contract specification can either be loaded from a file or passed directly
on the command line.

```
    $ uniquid create-contracts --input-json-file <json file name>
    $ uniquid create-contracts --input-json <json contract specification>
```

The format of the JSON file to create a new contract is:

```
[
    {
        "provider": "xpub_of_provider_device",
        "user": "xpub_of_user_device",
        "functions": [40, 41]
    }
]
```

The identifier used to identify the devices, between which the contract is created,
is the Public Key XPUB of the devices.  The functions field is used to identify
the IDs of the functionality which is enabled by the contract.

An example of the JSON file to request the creation of two new contracts:

```
[
    {
        "provider": "tpubDGDkliuherf34hSGSDG57652DSFDSFDksdfkjsdf434fgD",
        "user": "tpubDAquqJlksdf342GFRG8p98sdfhjhk4FDFD434rsdfDSFan",
        "functions": [40, 41]
    },
    {
        "provider": "tpubGFSDF8485FDSSDSDF345345HGDDFHkdsfk49ihkfgDEODs",
        "user": "tpubDAquqJlksdf342GFRG8p98sdfhjhk4FDFD434rsdfDVZRN",
        "functions": [39, 42]
    }
]
```

Existing contracts can be revoked by specifying the transaction identifiers
of the contracts in one of three ways:
* passing transaction identifiers as arguments.
* passing a JSON list of identifiers on the command line.
* passing the path of a file containing a list of identifiers in JSON format.

```
    $ uniquid delete-contracts <transaction id> <transaction id>
    $ uniquid delete-contracts --input-json <json list of ids>
    $ uniquid delete-contracts --input-json-file <json file name>
```

An example of the JSON file used to define the transaction IDs of several
contracts which should be deleted.

```
[
    "ebaef8fdf1645032010e801fad010338d2048fa3e67154d660545b4eb9b01c58",
    "eb99d374aa8f620878d86e987ed1943329280668c60ec0d87de3e7182a87a659"
]
```

An example of a command to delete a Uniquid contract between two IoT devices.
The transaction Ids can be passed as arguments on the command line.

```
    $ uniquid delete-contracts ebaef8fdf1645032010e801fad010338d2048fa3e67154d660545b4eb9b01c58
```


## Sharing Access to Devices

The creation of Access Contracts between devices can be shared between
organizations.  This sharing of the access to devices between orgainizations
must be permitted by the organization which owns the devices.

The user can view all of the devices which are shared using the command:

```
    $ uniquid list-shares
    $ uniquid list-shares --output json
```

The user can view the devices which have been shared by another organization
with their organization.

```
    $ uniquid list-shares --direction in
```

The user can also view the devices which their organization has shared with
other organizations.

```
    $ uniquid list-shares --direction out
```

The user can retrieve the list of shared devices, filtered to only display
the devices either shared with or by a specific organisation.

```
    $ uniquid list-shares --org <organization name>
    $ uniquid list-shares --org <organization name> --direction in
    $ uniquid list-shares --org <organization name> --direction out
```

New shares can be specified in JSON format and created by the tool. The
JSON share specification can either be loaded from a file or passed directly
on the command line.

```
    $ uniquid create-shares --input-json-file <json file name>
    $ uniquid create-shares --input-json <json contract specification>
```

Existing shares can be revoked by specifying the share identifiers
of the shares in one of three ways:
* passing share identifiers as arguments.
* passing a JSON list of identifiers on the command line.
* passing the path of a file containing a list of identifiers in JSON format.

```
    $ uniquid delete-shares <share id> <share id>
    $ uniquid delete-shares --input-json <json list of ids>
    $ uniquid delete-shares --input-json-file <json file name>
```

## Integration with AWS IoT

The Uniquid system allows you to integrate your IoT devices into both the
Uniquid and Amazon AWS ecosystems.  Uniquid contracts can then be used
to securely enable and disable interactions between IoT devices and the
AWS IoT Hub.
The user is guided through this integration process by the `deploy` command.
Before starting with the AWS integration, the user should verify that they are
registered with AWS and that they can connect to AWS using Amazon's AWS CLI
tool (awscli).

The command to start the deployment of the Uniquid Agent to the user's
Amazon AWS account is:

```
    $ uniquid deploy aws
```

## Getting Help

Come over and join in the Uniquid community at [Gitter](https://gitter.im/uniquid).


## Contact Uniquid

If you would like to learn more about our innovative technology, please contact
us at [hello@uniquid.com](mailto:hello@uniquid.com?Subject=PyPi%20Query).
