import os
import sys
import argparse
import cdsapi
import boto3
from botocore.exceptions import NoCredentialsError

def download_era5(year, region, output_dir):
    c = cdsapi.Client()

    target_file = os.path.join(output_dir, f'era5_{region}_{year}.nc')

    if os.path.exists(target_file):
        print(f'✅ Arquivo {target_file} já existe. Pulando download.')
        return target_file

    print(f'🔄 Iniciando download ERA5 - Ano: {year} | Região: {region} | Destino: {target_file}')

    c.retrieve(
        'reanalysis-era5-single-levels',   # Dataset correto para o ERA5 no CDS
        {
            'product_type': 'reanalysis',
            'variable': [
                '2m_temperature',
                'total_precipitation',
                'surface_solar_radiation_downwards',
                'volumetric_soil_water_layer_1',
                '10m_u_component_of_wind',
                '10m_v_component_of_wind',
                'mean_sea_level_pressure'
            ],
            'year': str(year),
            'month': [f'{m:02d}' for m in range(1, 13)],
            'day': [f'{d:02d}' for d in range(1, 32)],
            'time': ['00:00', '06:00', '12:00', '18:00'],
            'format': 'netcdf'
        },
        target_file
    )

    print(f'✅ Download concluído: {target_file}')
    return target_file

def upload_to_s3(file_path, bucket, s3_key):
    session = boto3.session.Session()
    s3 = session.client('s3')

    try:
        s3.upload_file(file_path, bucket, s3_key)
        print(f'✅ Upload para S3 concluído: s3://{bucket}/{s3_key}')
    except NoCredentialsError:
        print('❌ Falha: AWS credentials não encontradas.')

def main():
    parser = argparse.ArgumentParser(description='Download ERA5 + Upload S3')
    parser.add_argument('--start_year', type=int, required=True, help='Ano inicial')
    parser.add_argument('--end_year', type=int, required=True, help='Ano final')
    parser.add_argument('--bucket', type=str, required=True, help='Nome do bucket S3')
    parser.add_argument('--region', type=str, default='BR', help='Região (ex: BR)')
    args = parser.parse_args()

    local_output_dir = os.path.join(os.getcwd(), 'outputs')
    os.makedirs(local_output_dir, exist_ok=True)

    for year in range(args.start_year, args.end_year + 1):
        local_file = download_era5(year, args.region, local_output_dir)

        if os.path.exists(local_file):
            s3_key = f'era5/{year}/era5_{args.region}_{year}.nc'
            upload_to_s3(local_file, args.bucket, s3_key)

if __name__ == '__main__':
    main()
