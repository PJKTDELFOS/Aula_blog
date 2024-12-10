from . import models
def context_processor_example(request):
    return {
        'example':'veio do context processor(example)',
    }


def site_setup(request):
    setup=models.SiteSetup.objects.order_by('-id').first()
    return {
        'site_setup':setup
    }

#atentar para pegar as variaveis de atributos da classe
#instanciada