import os
import sys
import argparse
import boto3
from datetime import datetime

def dummy_download_era5(year, region, output_path):
    print(f"Simulando download ERA5 para o ano {year}, região {region}...")
    dummy_file = os.path.join(output_path, f"era5_{year}.nc")
    with open(dummy_file, 'w') as f:
        f.write(f"Dummy ERA5 data for year {year} and region {region}\n")
    print(f"Arquivo simulado criado em: {dummy_file}")
    return dummy_file

def upload_to_s3(file_path, bucket, s3_key):
    print(f"Enviando {file_path} para s3://{bucket}/{s3_key} ...")
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket, s3_key)
    print("Upload concluído com sucesso.")

def main():
    parser = argparse.ArgumentParser(description="Fetch ERA5 Data and Upload to S3")
    parser.add_argument('--year', required=True, type=int, help='Ano (ex: 2024)')
    parser.add_argument('--bucket', required=True, help='Nome do bucket S3 (ex: spr-raw)')
    parser.add_argument('--region', required=True, help='Região (ex: BR)')
    args = parser.parse_args()

    local_output_dir = os.path.join(os.getcwd(), 'outputs')
    os.makedirs(local_output_dir, exist_ok=True)

    local_file = dummy_download_era5(args.year, args.region, local_output_dir)

    s3_key = f"era5/{args.year}/{os.path.basename(local_file)}"
    upload_to_s3(local_file, args.bucket, s3_key)

if __name__ == "__main__":
    main()
