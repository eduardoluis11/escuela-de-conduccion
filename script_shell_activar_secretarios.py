from app_horarios.models import Secretario
secretarios = Secretario.objects.all()
secretarios.update(esta_dentro_del_horario_de_trabajo=1)
