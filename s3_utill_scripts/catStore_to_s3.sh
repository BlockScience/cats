#!/bin/bash

aws s3 sync ./catStore/cats-public/input/df s3://cats-public/input/df
aws s3 sync ./catStore/cats-public/cad-store/cad/cai/invoices s3://cats-public/cad-store/cad/cai/invoices
aws s3 sync ./catStore/cats-public/cad-store/cad/cai/bom s3://cats-public/cad-store/cad/cai/bom
aws s3 sync ./catStore/cats-public/cad-store/cad/cao/data s3://cats-public/cad-store/cad/cao/data
aws s3 sync ./catStore/cats-public/cad-store/cad/transformation s3://cats-public/cad-store/cad/transformation
aws s3 sync ./catStore/cats-public/cad-store/cad/cao/bom s3://cats-public/cad-store/cad/cao/bom
aws s3 sync ./catStore/cats-public/cad-store/cad/cao/data s3://cats-public/cad-store/cad/cao/data
aws s3 sync ./catStore/cats-public/cad-store/cad/cai2/data s3://cats-public/cad-store/cad/cai2/data
aws s3 sync ./catStore/cats-public/cad-store/cad/cai2/invoices s3://cats-public/cad-store/cad/cai2/invoices
aws s3 sync ./catStore/cats-public/cad-store/cad/transformation s3://cats-public/cad-store/cad/transformation