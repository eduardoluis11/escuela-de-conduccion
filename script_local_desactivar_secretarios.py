# This Python file uses the following encoding: utf-8

# Script para cambiar el campo "es secretario" de todos los usuarios de la tabla "Secretario"

# Esta es la funcion que voy a llamar para cambiar el estado de los secretarios
def main():

    # Query set que selecciona a los secretarios de la tabla Secretario
    # gloria_secretaria = Secretario.objects.filter(id_de_usuario_id=5)
    secretarios = Secretario.objects.all()
    
    # Esto cambia el campo de los secretarios a "No"
    # for secretario in secretarios:
    # secretarios.update(el_usuario_es_secretario='No')
    secretarios.update(esta_dentro_del_horario_de_trabajo=0)
    
    # Esto cambia el estado del campo "es secretario" a "No"
    #gloria_secretaria.update(el_usuario_es_secretario='No')
    
    # Mensaje de confirmacion
    print("Todos los secretarios han sido desactivados.")
    
    # print("El estado de Gloria como secretaria ha cambiado.")

# Esto va a llamar a la funcion "main"
if __name__ == "__main__":
    import os
    from django.core.wsgi import get_wsgi_application
    
    # No se si en "variable.settings" tiene que ir la carpeta "proyecto" o "app"
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proyecto_conduccion.settings")
    application = get_wsgi_application()
    
    # Esto accede a la tabla Secretario
    from app_horarios.models import Secretario
    
    # Esto ejecuta la funcion main()
    main()
