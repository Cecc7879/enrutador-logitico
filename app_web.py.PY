import streamlit as st
import time
import urllib.parse
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# Configuración de la página web
st.set_page_config(page_title="Optimizador de Rutas", page_icon="🚗", layout="centered")

st.title("🚗 Enrutador Logístico Inteligente")
st.write("Introduce las direcciones para calcular la ruta más corta para el técnico.")

# 1. Casilla para la Bodega
direccion_bodega = st.text_input("📍 Dirección de Salida (Bodega):", "Plaza de Armas, Santiago, Chile")

st.subheader("👥 Clientes del Día")
st.write("Escribe las direcciones de los clientes (puedes cambiarlas):")

# Casillas interactivas para los clientes
cliente_1 = st.text_input("Cliente 1:", "Plaza Baquedano, Providencia, Chile")
cliente_2 = st.text_input("Cliente 2:", "Costanera Center, Providencia, Chile")
cliente_3 = st.text_input("Cliente 3:", "Mall Parque Arauco, Las Condes, Chile")

# Botón mágico para calcular
if st.button("🚀 Calcular Ruta Óptima", type="primary"):
    
    buscador = Nominatim(user_agent="mi_app_logistica_finalísima")
    
    with st.spinner("Buscando direcciones en el mapa y optimizando..."):
        loc_bodega = buscador.geocode(direccion_bodega)
        
        direcciones_clientes = [cliente_1, cliente_2, cliente_3]
        clientes_coordenadas = []
        
        for clie in direcciones_clientes:
            if clie.strip():
                loc = buscador.geocode(clie)
                if loc:
                    clientes_coordenadas.append({"nombre": clie, "coor": (loc.latitude, loc.longitude)})
                time.sleep(1)

        if loc_bodega and len(clientes_coordenadas) > 0:
            coor_actual = (loc_bodega.latitude, loc_bodega.longitude)
            ruta_ordenada = []

            while len(clientes_coordenadas) > 0:
                mas_cercano = None
                distancia_minima = float('inf')
                
                for clie in clientes_coordenadas:
                    dist = geodesic(coor_actual, clie["coor"]).kilometers
                    if dist < distancia_minima:
                        distancia_minima = dist
                        mas_cercano = clie
                        
                ruta_ordenada.append((mas_cercano["nombre"], distancia_minima))
                coor_actual = mas_cercano["coor"]
                clientes_coordenadas.remove(mas_cercano)

            # --- MOSTRAR RESULTADOS EN LA PÁGINA ---
            st.success("¡Ruta optimizada con éxito! 🎉")
            st.info(f"**Punto de Partida:** {direccion_bodega}")
            st.write("### ⏱️ Orden de Visitas Sugeridas:")
            
            for i, (nombre, dist) in enumerate(ruta_ordenada, 1):
                st.write("---") # Línea divisoria
                
                # Texto de la parada
                st.markdown(f"**Parada {i}:** {nombre}  \n*(a {dist:.2f} km de la parada anterior)*")
                
                # ENLACE CORREGIDO Y SEGURO (Google Maps oficial)
                direccion_codificada = urllib.parse.quote(nombre)
                enlace_real_maps = f"https://www.google.com/maps/search/?api=1&query={direccion_codificada}"
                
                # Botón de enlace directo
                st.link_button("🗺️ Ver en Google Maps", enlace_real_maps)
                
            st.balloons()
        else:
            st.error("❌ No se pudo encontrar la bodega o no pusiste clientes válidos.")