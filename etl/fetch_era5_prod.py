import os
import sys
import argparse
import cdsapi
import boto3
from botocore.exceptions import NoCredentialsError

def download_era5(year, region, output_dir):
    try:
        c = cdsapi.Client()
    except Exception as e:
        print(f'❌ Erro ao inicializar o cliente CDSAPI: {e}')
        return None

    target_file = os.path.join(output_dir, f'era5_{region}_{year}.nc')

    # Se já existe, não faz o download de novo
    if os.path.exists(target_file):
        print(f'✅ Arquivo {target_file} já existe. Pulando download.')
        return target_file

    print(f'🔄 Iniciando download ERA5 - Ano: {year} | Região: {region} | Destino: {target_file}')

    # Define área para o Brasil se region == 'BR'
    area = None
    if region == 'BR':
        # [Norte, Oeste, Sul, Leste] (lat/lon)
        area = [-5.0, -74.0, -34.0, -34.0]
    # ...adicione outras regiões conforme necessário...

    # Dias por mês (para evitar erro de dias inexistentes)
    days_in_month = {
        1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
        7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }
    # Ajusta para ano bissexto
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        days_in_month[2] = 29

    try:
        c.retrieve(
            'reanalysis-era5-single-levels',
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
                'year': [str(year)],
                'month': [f'{m:02d}' for m in range(1, 13)],
                'day': [f'{d:02d}' for m in range(1, 13) for d in range(1, days_in_month[m]+1)],
                'time': ['00:00', '06:00', '12:00', '18:00'],
                'format': 'netcdf',
                **({'area': area} if area else {})
            },
            target_file
        )
    except Exception as e:
        print(f'❌ Erro no download do ERA5: {e}')
        return None

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
    except Exception as e:
        print(f'❌ Erro ao fazer upload para S3: {e}')

def main():
    parser = argparse.ArgumentParser(description='Download ERA5 + Upload S3')
    parser.add_argument('--start_year', type=int, required=True, help='Ano inicial (ex: 2023)')
    parser.add_argument('--end_year', type=int, required=True, help='Ano final (ex: 2023)')
    parser.add_argument('--bucket', type=str, required=True, help='Nome do bucket S3 (exemplo: meu_bucket)')
    parser.add_argument('--region', type=str, default='BR', help='Região (ex: BR)')
    args = parser.parse_args()

    local_output_dir = os.path.join(os.getcwd(), 'outputs')
    os.makedirs(local_output_dir, exist_ok=True)

    for year in range(args.start_year, args.end_year + 1):
        local_file = download_era5(year, args.region, local_output_dir)

        if local_file and os.path.exists(local_file):
            s3_key = f'era5/{year}/era5_{args.region}_{year}.nc'
            upload_to_s3(local_file, args.bucket, s3_key)

if __name__ == '__main__':
    main()
