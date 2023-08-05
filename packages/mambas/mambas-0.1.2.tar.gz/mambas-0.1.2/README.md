# ![Mambas](/assets/logo.png?raw=true "Mambas")
[![Build Status](https://travis-ci.org/misterkevinski/mambas.svg?branch=master)](https://travis-ci.org/misterkevinski/mambas)
[![Coverage Status](https://coveralls.io/repos/github/misterkevinski/mambas/badge.svg?branch=master)](https://coveralls.io/github/misterkevinski/mambas?branch=master)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/misterkevinski/mambas/blob/master/LICENSE)

<p align="center">
  <img src="/assets/screenshot.png?raw=true" />
</p>

## What is it?
Mambas is a web based visualization tool to manage your Keras projects and monitor your training sessions.

## What is included?
As of today, the following functionalities have been implemented:
- [x] Managing different Machine Learning projects
- [x] Monitoring and managing training sessions of a single project
- [x] Adding custom training metrics to monitor
- [ ] Displaying training hyperparameters
- [ ] Exploring Neural Network layers and weights

## Installation
- Install Mambas from PyPI:
```
pip install mambas
```
- Install from Github source:
```
git clone https://github.com/misterkevinski/mambas.git
cd mambas
python setup.py install
```

## Getting started
### Run Mambas
```
mambas --port 8080
```

### Create Mambas project and get token
<table>
  <tr>
    <td width="50%" align="center">
      <b>First step</b>
    </td>
    <td width="50%" align="center">
      <b>Second step</b>
    </td>
  </tr>
  <tr>
    <td align="center">   
      <img src="/assets/add_project.png?raw=true" />
    </td>
    <td align="center">
      <img src="/assets/get_token.png?raw=true" />
    </td>
  </tr>
  <tr>
    <td align="center">
      Click on <i>ADD</i> button to create a new Mambas project and enter a project name.
    </td>
    <td align="center">
      Click on <i>TOKEN</i> button to get project's token and copy it.
    </td>
  </tr>
</table>

### Add Mambas callback to Keras
```
from mambas.keras.callback import MambasCallback
...
token = '<project_token>'
callback = MambasCallback(token)
model.fit(x_train, y_train, callbacks=[callback])
```
