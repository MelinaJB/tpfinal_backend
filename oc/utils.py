import fitz  # PyMuPDF
import re

def extraer_datos(pdf_path):
    # Abrir el archivo PDF
    documento = fitz.open(pdf_path)
    texto = ""
    for pagina in documento:
        texto += pagina.get_text()

    # Función auxiliar para buscar con expresiones regulares
    def buscar_patron(patron, texto, flags=0):
        resultado = re.search(patron, texto, flags)
        return resultado.group(1) if resultado else None

    # Expresiones regulares ajustadas para extraer los datos
    uoc = buscar_patron(r'UOC:\s*(.*)', texto)
    numero_orden = buscar_patron(r'Número:\s*(\d+)', texto)
    fecha_orden = buscar_patron(r'Fecha:\s*(\d{2}/\d{2}/\d{4})', texto)
    numero_compulsa = buscar_patron(r'Número:\s*(\d+-\d+)', texto)
    nombre_afiliado = buscar_patron(r'AFILIADO:\s*(.*)', texto)
    detalle_orden = buscar_patron(r'DETALLE DE LA ORDEN DE COMPRA(.*)Importe Total:', texto, re.DOTALL)
    importe_total = buscar_patron(r'Importe Total:\s*ARS\s*([\d.,]+)', texto)

    # Regex para capturar las líneas de productos en "Detalle de la Orden de Compra"
   
    # productos = re.findall(
    # r'(\d+),\d+\s+U\s+[^\d]+-\s+([^\d]+?)\s+([\d.,]+),\d+',  # Ajustada para el formato específico 
    # texto
    # )
    productos = re.findall(
    r'(\d+),\d+\s+U\s+\d+\s+-\s+([A-Z\s]+)\s+([\d.,]+),\d+',  # Ajustada para capturar cantidad, descripción y precio
    texto, re.DOTALL
    )


    print(texto)

    # Convertir la lista de productos en un formato adecuado para retornar
    lista_productos = [
        {
            'cantidad': int(cantidad.replace(",", "")),
            'descripcion': descripcion.strip(),
            'precio_unitario': float(precio_unitario.replace(".", "").replace(",", "."))  # Convertir precio a float
        }
        for cantidad, descripcion, precio_unitario in productos
    ]


    return {
        'uoc': uoc,
        'numero_orden': numero_orden,
        'fecha_orden': fecha_orden,
        'numero_compulsa': numero_compulsa,
        'nombre_afiliado': nombre_afiliado,
        'detalle_orden': lista_productos,  # Lista de productos extraídos
        # 'importe_total': importe_total
        'importe_total': float(importe_total.replace(".", "").replace(",", ".")) if importe_total else None

    }



