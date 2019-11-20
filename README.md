# Gaia Plastics Project
This README provides a brief project overview. Please go to our Wiki if you want more in-depth information about the project and how to set up a device: https://github.com/waterhog/gaia_plastics/wiki

## Introduction
The Gaia Plastics Project is an IoT project for counting plastic objects floating on the surface of rivers. The project uses a simple hardware setup including a camera, and a computer vision model to detect plastics objects. Every 15 minutes, a plastic count for that period is sent from the device to the cloud. This data can be queried from a mobile phone. In the future, we plan to add a front-end that will use a map to display near-real-time plastic counts from all devices.

**Goal of the project**

The goal of the project is to provide near-real-time data about plastics in rivers. We know that plastic washed into the ocean from rivers is a major source of ocean plastic; **around 90% of the plastic in the ocean come from only 9 or 10 major rivers** **citation needed**. Despite this, **there is a severe lack of data about plastics in rivers**. Without data, it is difficult to take action. We hope this data can be used to organize cleanups, help businesses and local government agencies handle their waste, and even help drive regulation.

**Intended users**

We have designed this project so that it is affordable, (relatively) easy to set up, and low maintainence, because we want to engage citizen scientists, teachers, students, anyone with interest. But, any individual or organization can build a device and start collecting data. Our project is under a General Public License (see below for more information).

## Requirements
This project uses the following components.
### Hardware
- Raspberry Pi 4 4G
- SIM7000X
- Wide-angle camera for RPi/Arduino projects
- **battery**
- **case**

### Software
The software used is all found under the **app** folder in this repository. The project also uses Azure SQL Database to store data, but this is already set up so users don't need to consider this.

## Setup Guide
Please see our wiki for our Setup Guide: (https://github.com/waterhog/gaia_plastics/wiki)

## License
This project is licensed under the GNU General Public License v3.0. Permissions of this strong copyleft license are conditioned on making available complete source code of licensed works and modifications, which include larger works using a licensed work, under the same license. Copyright and license notices must be preserved. Contributors provide an express grant of patent rights. 

Please see https://github.com/waterhog/gaia_plastics/blob/master/LICENSE for more information.
