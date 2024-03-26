provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

resource "aws_s3_bucket" "buckets-olaf-producao" {
  bucket = "bucket-olaf-produc"
  tags = {
    "area"       = "produtos"
    "enviroment" = "production"
  }
}

resource "aws_s3_bucket" "buckets-olaf-desenvolvimento" {
  bucket = "bucket-olaf-develop"
  tags = {
    "area"       = "produtos"
    "enviroment" = "development"
  }
}
