opsworks-cli
======================

A simple python module to work with aws opsworks

[![Build Status](https://travis-ci.org/chaturanga50/opsworks-cli.svg?branch=master)](https://travis-ci.org/chaturanga50/opsworks-cli)

How to install
--------------

You can download the updated release version from pypi repo

``` bash
pip install opsworks-cli
```

Usage
-----

You can see the list of parameters available via `opsworks-cli --help`

#### run update_custom_cookbook

```bash
opsworks-cli update-custom-cookbooks --region eu-west-1 \
             --stack 2e7f6dd5-e4a3-4389-bc95-b4bacc234df0 \
             --layer ac0df176-104b-46ae-946e-7cf7367b816e \
             --instances 2
```

#### run execute-recipes

```bash
opsworks-cli execute-recipes --region eu-west-1 \
             --stack 2e7f6dd5-e4a3-4389-bc95-b4bacc234df0 \
             --layer ac0df176-104b-46ae-946e-7cf7367b816e \
             --instances 2 \
             --cookbook apache::default \
             --custom-json [{"lamp":{ "packages": { "app--sso": "17.1.6" } } }] # optional
```

```bash
opsworks-cli execute-recipes --region eu-west-1 \
             --stack 2e7f6dd5-e4a3-4389-bc95-b4bacc234df0 \
             --layer ac0df176-104b-46ae-946e-7cf7367b816e \
             --instances 2 \
             --cookbook apache
```

#### run setup

```bash
opsworks-cli setup --region eu-west-1 \
             --stack 2e7f6dd5-e4a3-4389-bc95-b4bacc234df0 \
             --layer ac0df176-104b-46ae-946e-7cf7367b816e \
             --instances 2
```

### How it works

- sending opsworks commands via aws api to specific stack ID and layer ID
- add the correct instance count as it's checking the success responce count according to that.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* ***Chathuranga Abeyrathna*** - *Initial work* - [github](https://github.com/chaturanga50/)

## Contributors

* ***Iruka Rupasinghe*** - *Feature Improvements* - [github](https://github.com/Rupasinghe2012/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details