import streamlit as st


class NodoTarea:
    """Nodo individual que almacena la información de una tarea y el puntero al siguiente."""
    def __init__(self, id_tarea, titulo, descripcion):
        self.id = id_tarea
        self.titulo = titulo
        self.descripcion = descripcion
        self.siguiente = None  


class ListaTareasEnlazada:
    """Gestor de la Lista Simplemente Enlazada utilizando únicamente punteros."""
    def __init__(self):
        self.cabeza = None  
        self.contador_id = 1

    def agregar_tarea(self, titulo, descripcion):
        """Agrega un nuevo nodo al final de la lista enlazada recorriendo punteros."""
        nuevo_nodo = NodoTarea(self.contador_id, titulo, descripcion)
        self.contador_id += 1

        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def eliminar_tarea(self, id_tarea):
        """Elimina un nodo reajustando las referencias (punteros)."""
        if self.cabeza is None:
            return False

        if self.cabeza.id == id_tarea:
            self.cabeza = self.cabeza.siguiente  
            return True

        actual = self.cabeza
        while actual.siguiente is not None and actual.siguiente.id != id_tarea:
            actual = actual.siguiente

        if actual.siguiente is not None:
            actual.siguiente = actual.siguiente.siguiente
            return True

        return False

    def esta_vacia(self):
        return self.cabeza is None


if "lista_tareas" not in st.session_state:
    st.session_state.lista_tareas = ListaTareasEnlazada()
    # Tareas de ejemplo iniciales
    st.session_state.lista_tareas.agregar_tarea("Comprar víveres", "Ir al supermercado por frutas y verduras")
    st.session_state.lista_tareas.agregar_tarea("Estudiar Estructuras de Datos", "Repasar punteros y listas enlazadas en Python")

lista = st.session_state.lista_tareas



st.set_page_config(page_title="Gestor de Tareas - Lista Enlazada", page_icon="📝", layout="centered")

st.title("Lista de Tareas Pendientes")
st.caption("Implementación con **Estructura de Datos Enlazada (Punteros)** sin usar listas nativas de Python.")

st.divider()

with st.form(key="form_agregar_tarea", clear_on_submit=True):
    st.subheader("➕ Agregar nueva tarea")
    titulo = st.text_input("Título de la tarea")
    descripcion = st.text_area("Descripción (Opcional)")
    boton_guardar = st.form_submit_button(label="Guardar Tarea")

    if boton_guardar:
        if titulo.strip():
            lista.agregar_tarea(titulo.strip(), descripcion.strip())
            st.success(f"Tarea '{titulo}' agregada con éxito.")
            st.rerun()
        else:
            st.warning("El título de la tarea no puede estar vacío.")

st.divider()

st.subheader("Tareas Pendientes")

if lista.esta_vacia():
    st.info("No hay tareas pendientes en la lista enlazada.")
else:
    actual = lista.cabeza
    
    while actual is not None:
        with st.container(border=True):
            col_info, col_accion = st.columns([0.8, 0.2])
            
            with col_info:
                st.markdown(f"**#{actual.id} - {actual.titulo}**")
                if actual.descripcion:
                    st.text(actual.descripcion)
                st.caption(f"Direccionamiento: Nodo `[{hex(id(actual))}]` ➔ Siguiente: `{hex(id(actual.siguiente)) if actual.siguiente else 'NULL'}`")
            
            with col_accion:
                if st.button("Completar", key=f"eliminar_{actual.id}"):
                    lista.eliminar_tarea(actual.id)
                    st.rerun()

        actual = actual.siguiente