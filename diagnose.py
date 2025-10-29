"""
Script de diagnóstico para depurar problemas de carga de imágenes.

Prueba directamente la carga de imágenes sin la interfaz gráfica.
"""

import sys
import requests
from pathlib import Path
from io import BytesIO
import pandas as pd

# Añadir el directorio raíz al path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

import config


def test_csv_download():
    """Prueba la descarga del CSV."""
    print("=" * 80)
    print("TEST 1: Descarga del CSV")
    print("=" * 80)
    
    try:
        print(f"URL: {config.CSV_URL}")
        response = requests.get(config.CSV_URL, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type')}")
        print(f"Tamaño: {len(response.text)} caracteres")
        
        response.raise_for_status()
        
        # Parsear CSV
        from io import StringIO
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data, encoding='utf-8')
        
        print(f"\n✓ CSV descargado exitosamente")
        print(f"  Registros: {len(df)}")
        print(f"  Columnas: {list(df.columns)}")
        
        return df
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return None


def test_image_urls(df):
    """Prueba las URLs de imágenes."""
    print("\n" + "=" * 80)
    print("TEST 2: Verificación de URLs de imágenes")
    print("=" * 80)
    
    if df is None:
        print("✗ No hay DataFrame para analizar")
        return
    
    url_column = config.CSV_COLUMNS["url_imagen"]
    
    if url_column not in df.columns:
        print(f"✗ Columna '{url_column}' no encontrada en el CSV")
        print(f"  Columnas disponibles: {list(df.columns)}")
        
        # Buscar columnas que contengan "url" o "imagen"
        posibles = [col for col in df.columns if 'url' in col.lower() or 'imagen' in col.lower()]
        if posibles:
            print(f"  Posibles columnas: {posibles}")
        return
    
    print(f"Columna de URL: {url_column}")
    
    # Estadísticas
    total = len(df)
    con_url = df[url_column].notna().sum()
    sin_url = total - con_url
    
    print(f"\nEstadísticas:")
    print(f"  Total de cámaras: {total}")
    print(f"  Con URL: {con_url}")
    print(f"  Sin URL: {sin_url}")
    
    # Mostrar algunas URLs
    print(f"\nPrimeras 5 URLs:")
    for idx, url in enumerate(df[url_column].head(5)):
        print(f"  {idx}: {url}")
    
    return df[url_column].dropna().tolist()


def test_image_download(urls):
    """Prueba descargar algunas imágenes."""
    print("\n" + "=" * 80)
    print("TEST 3: Descarga de imágenes de prueba")
    print("=" * 80)
    
    if not urls:
        print("✗ No hay URLs para probar")
        return
    
    # Probar las primeras 3 URLs
    test_urls = urls[:3]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
        'Referer': 'https://movilidad.malaga.eu/',
        'Sec-Fetch-Dest': 'image',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-origin'
    }
    
    for idx, url in enumerate(test_urls):
        print(f"\n--- Probando imagen {idx} ---")
        print(f"URL: {url}")
        
        try:
            response = requests.get(
                url, 
                timeout=config.IMAGE_TIMEOUT,
                headers=headers,
                allow_redirects=True
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Content-Type: {response.headers.get('content-type', 'N/A')}")
            print(f"Content-Length: {len(response.content)} bytes")
            
            # Mostrar primeros bytes para debug
            print(f"Primeros 100 bytes: {response.content[:100]}")
            
            response.raise_for_status()
            
            # Verificar si es una imagen o HTML
            content_type = response.headers.get('content-type', '')
            
            if 'text/html' in content_type.lower():
                print(f"⚠ WARNING: Servidor devolvió HTML en lugar de imagen")
                print(f"   Posible error de acceso o autenticación requerida")
                # Mostrar parte del HTML
                html_preview = response.content[:300].decode('utf-8', errors='ignore')
                print(f"   Vista previa HTML: {html_preview}")
                continue
            
            if 'image' not in content_type.lower():
                print(f"⚠ WARNING: Content-Type no indica imagen: {content_type}")
            
            # Intentar cargar con PIL
            try:
                from PIL import Image
                image = Image.open(BytesIO(response.content))
                print(f"✓ Imagen válida: {image.format} {image.size} {image.mode}")
            except ImportError:
                print("ℹ PIL/Pillow no disponible, no se puede verificar formato")
            except Exception as e:
                print(f"✗ Error abriendo imagen con PIL: {e}")
            
            print(f"✓ Descarga exitosa")
            
        except requests.Timeout:
            print(f"✗ Timeout después de {config.IMAGE_TIMEOUT}s")
        except requests.RequestException as e:
            print(f"✗ Error HTTP: {e}")
        except Exception as e:
            print(f"✗ Error inesperado: {e}")


def test_qt_image_loading(urls):
    """Prueba cargar imágenes con Qt."""
    print("\n" + "=" * 80)
    print("TEST 4: Carga con Qt (QImage/QPixmap)")
    print("=" * 80)
    
    try:
        from PySide6.QtGui import QImage, QPixmap
        print("✓ PySide6 importado correctamente")
    except ImportError as e:
        print(f"✗ No se puede importar PySide6: {e}")
        return
    
    if not urls:
        print("✗ No hay URLs para probar")
        return
    
    # Probar primera URL
    url = urls[0]
    print(f"\nProbando URL: {url}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'Referer': 'https://movilidad.malaga.eu/'
        }
        
        response = requests.get(url, timeout=config.IMAGE_TIMEOUT, headers=headers)
        response.raise_for_status()
        
        content = response.content
        print(f"Descargados {len(content)} bytes")
        print(f"Content-Type: {response.headers.get('content-type')}")
        
        # Verificar si es HTML
        if b'<!DOCTYPE html>' in content[:100] or b'<html' in content[:100]:
            print(f"✗ Servidor devolvió HTML en lugar de imagen")
            print(f"   Esto indica que las imágenes requieren autenticación")
            print(f"   o están protegidas contra scraping directo")
            return
        
        # Probar con QImage
        qimage = QImage()
        success = qimage.loadFromData(content)
        
        if success:
            print(f"✓ QImage cargada exitosamente")
            print(f"  Tamaño: {qimage.width()}x{qimage.height()}")
            print(f"  Formato: {qimage.format()}")
            
            # Probar conversión a QPixmap
            pixmap = QPixmap.fromImage(qimage)
            if not pixmap.isNull():
                print(f"✓ QPixmap creado exitosamente")
            else:
                print(f"✗ QPixmap es null")
        else:
            print(f"✗ QImage.loadFromData() falló")
            print(f"  Primeros 100 bytes: {content[:100]}")
            
    except Exception as e:
        print(f"✗ Error: {e}")


def main():
    """Función principal de diagnóstico."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 15 + "DIAGNÓSTICO DE CARGA DE IMÁGENES" + " " * 31 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    # Test 1: Descargar CSV
    df = test_csv_download()
    
    # Test 2: Verificar URLs
    urls = test_image_urls(df)
    
    # Test 3: Descargar imágenes
    if urls:
        test_image_download(urls)
        
        # Test 4: Cargar con Qt
        test_qt_image_loading(urls)
    
    print("\n" + "=" * 80)
    print("DIAGNÓSTICO COMPLETADO")
    print("=" * 80)
    print("\nRevisa el log 'app.log' para más detalles cuando ejecutes la app principal.")
    print()


if __name__ == "__main__":
    main()
