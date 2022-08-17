# Deprecation Notice

This project is deprecated in favor of QuantConnect's official API docs, which is generated in the [QuantConnect/Lean.Reference](https://github.com/QuantConnect/Lean.Reference) repository and hosted at [https://www.lean.io/docs/v2/lean-engine/class-reference/index.html](https://www.lean.io/docs/v2/lean-engine/class-reference/index.html). Old links to [https://lean-api-docs.netlify.app/](https://lean-api-docs.netlify.app/) will automatically redirect to the same page in the official docs.

# Lean API Docs

[![Deploy Status](https://github.com/jmerle/lean-api-docs/workflows/Deploy/badge.svg)](https://github.com/jmerle/lean-api-docs/actions?query=workflow%3ADeploy)

This repository contains scripts to automatically generate API documentation for QuantConnect's [Lean](https://github.com/QuantConnect/Lean). Every night at 00:00 UTC a GitHub Actions workflow is triggered which generates API documentation for the latest version of Lean using Doxygen and deploys it to Netlify at [https://lean-api-docs.netlify.app/](https://lean-api-docs.netlify.app/).

## Usage

To run the API documentation generator locally, make sure [Doxygen](https://www.doxygen.nl/index.html)'s `doxygen` and [Graphviz](https://graphviz.org/)'s `dot` (>1.8.10) are installed and available on your `PATH`, clone this repository and run `python generate.py`.
