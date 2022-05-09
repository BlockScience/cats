#!/bin/bash

aws s3 sync s3://cats-public/input/df ./catStore/cats-public/input/df
aws s3 sync s3://cats-public/cad-store/cad/cai/invoices ./catStore/cats-public/cad-store/cad/cai/invoices
aws s3 sync s3://cats-public/cad-store/cad/cai/bom ./catStore/cats-public/cad-store/cad/cai/bom
aws s3 sync s3://cats-public/cad-store/cad/cao/data ./catStore/cats-public/cad-store/cad/cao/data
aws s3 sync s3://cats-public/cad-store/cad/transformation ./catStore/cats-public/cad-store/cad/transformation
aws s3 sync s3://cats-public/cad-store/cad/cao/bom ./catStore/cats-public/cad-store/cad/cao/bom
aws s3 sync s3://cats-public/cad-store/cad/cao/data ./catStore/cats-public/cad-store/cad/cao/data
aws s3 sync s3://cats-public/cad-store/cad/cai2/data ./catStore/cats-public/cad-store/cad/cai2/data
aws s3 sync s3://cats-public/cad-store/cad/cai2/invoices ./catStore/cats-public/cad-store/cad/cai2/invoices
aws s3 sync s3://cats-public/cad-store/cad/transformation ./catStore/cats-public/cad-store/cad/transformation