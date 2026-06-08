import streamlit as st
import time
from geopy.geocoders import ArcGIS
from geopy.distance import geodesic

# Cambiamos al buscador de ArcGIS (más rápido y sin límites estrictos)
buscador = ArcGIS(timeout=15)

def obtener_coordenadas(direccion):
    try:
        resultado = buscador.geocode(direccion)
        return resultado
    except Exception:
        return None

# Título de la app
st.title("🚗 Optimizador de Rutas Logísticas")
st.write("Calcula la ruta más eficiente saliendo desde la bodega.")

# Inputs del usuario
direccion_bodega = st.text_input("📍 Dirección de la Bodega:", "Santiago, Chile")
st.markdown("---")

st.write("### 📍 Direcciones de los Clientes:")
dirección_1 = st.text_input("Cliente 1:")
dirección_2 = st.text_input("Cliente 2:")
dirección_3 = st.text_input("Cliente 3:")

if st.button("🚀 Calcular Ruta Óptima", type="primary"):
    direcciones_clientes = [d.strip() for d in [dirección_1, dirección_2, dirección_3] if d.strip()]
    
    if not direcciones_clientes:
        st.warning("⚠️ Por favor, ingresa al menos la dirección de un cliente.")
    else:
        with st.spinner("🔄 Buscando ubicaciones en el mapa al instante..."):
            # Buscar coordenadas de la bodega
            loc_bodega = obtener_coordenadas(direccion_bodega)
            
            if not loc_bodega:
                st.error("📌 El servidor de mapas no pudo ubicar la dirección de la Bodega. Revisa si está bien escrita.")
            else:
                puntos_validos = []
                # Buscar coordenadas de los clientes
                for i, d in enumerate(direcciones_clientes):
                    loc_cli = obtener_coordenadas(d)
                    if loc_cli:
                        puntos_validos.append({"nombre": f"Cliente {i+1}", "lat": loc_cli.latitude, "lon": loc_cli.longitude})
                    else:
                        st.warning(f"⚠️ No se pudo ubicar la dirección: '{d}'. Revisa si está bien escrita.")
                
                if not puntos_validos:
                    st.error("❌ No se pudo procesar ninguna dirección de cliente.")
                else:
                    # Ordenar por distancia
                    ruta_ordenada = []
                    pos_actual = (loc_bodega.latitude, loc_bodega.longitude)
                    
                    while puntos_validos:
                        proximo = min(puntos_validos, key=lambda p: geodesic(pos_actual, (p["lat"], p["lon"])).kilometers)
                        ruta_ordenada.append(proximo)
                        pos_actual = (proximo["lat"], proximo["lon"])
                        puntos_validos.remove(proximo)
                    
                    # Mostrar resultados
                    st.success("✨ ¡Ruta optimizada con éxito!")
                    st.write("### 📋 Orden del recorrido recomendado:")
                    st.write(f"**Salida:** Bodega ({direccion_bodega})")
                    
                    datos_mapa = [{"lat": loc_bodega.latitude, "lon": loc_bodega.longitude, "📍": "Bodega"}]
                    for idx, p in enumerate(ruta_ordenada):
                        st.write(f"➡️ **Paso {idx+1}:** {p['nombre']}")
                        datos_mapa.append({"lat": p["lat"], "lon": p["lon"], "📍": p["nombre"]})
                    
                    # Mostrar el mapa interactivo
                    st.write("### 🗺️ Mapa de la Ruta:")
                    st.map(datos_mapa, zoom=11)
                  
                    
