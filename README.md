# Merriam-Webster CLI Tool

## Overview
This is a command line tool that will allow the user to query the merriam-webster
dictionary and receive a formatted response with the word definition.
https://dictionaryapi.com/products/api-collegiate-dictionary
For example, given the word “exercise” your tool might return the following
`ek-sər-sīz` (noun): the act of bringing into play or realizing in action

## Features
- Fetch definitions for words from the Merriam-Webster Dictionary.
- Handle invalid inputs and API errors gracefully.
- Includes a test suite to ensure functionality.
- Packaged with a `Makefile` for easy setup and usage.

## Requirements
- Python 3.9+
- Merriam-Webster API Key (sign up at [Merriam-Webster Developer Portal]).

## Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Merriam-Webster