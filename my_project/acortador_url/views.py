from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from models import url_type
from django.views.decorators.csrf import csrf_exempt
import urllib

# Create your views here.

def lista_url():

    lista = ""
    tabla = url_type.objects.all()
    for url in tabla:
        lista = (lista + "<p><a href='" + url.large_url + "'>" + url.large_url +
                 "</a>" + " | " + "<a href='" + url.short_url +
                 "'>" + url.short_url + "</a></p>")
    return lista

@csrf_exempt
def handler(request):

    formulario = ('<form action="" method="POST">Intruduce una URL: '
                  + '<input type="text" name="url" value="" />'
                  + '<input type="submit" value="Acortar" /></form>')
    head = ("<h1><center>Aplicacion web para acortar URLs" +
            "</center></h1>")

    if request.method == "GET":
    
        texto = "<h2> Lista de URLs acortadas: </h2>"
        urls = lista_url()

        response = head + formulario + texto + urls
        HttpResponse.status_code = 200
        return HttpResponse(response)

    elif request.method == "POST":
        if not url_type.objects.all():
            counter = 0
        else:
            DB = url_type.objects.all()
            counter = int(len(DB))
        body = request.body
        print body.split("=")
        if body.split("=")[1] == '':
            return HttpResponseNotFound(head + "Introduzca una url en el formulario")
        url = body.split("=")[1]
        url = urllib.unquote(url).decode('utf8')
        if url.split("://")[0] != "http" and url.split("://")[0] != "https":
            url = "http://" + url

        try:
            url_search = url_type.objects.get(large_url=url)
            short_url_search = url_search.short_url
        except url_type.DoesNotExist:
            short_url_search = "http://localhost:8000/" + str(counter)
            url_new = url_type(large_url=url, short_url=short_url_search)
            url_new.save()
        head = "<h1><center>Aplicacion web para acortar URLs</center></h1>"
        response = ("<html><body>" + head + "<p><a href='" + url +
                    "'>URL</a></p><p><a href='" + short_url_search +
                    "'>URL Acortada</a></p></html></body>")
        HttpResponse.status_code = 200
        return HttpResponse(response)
    else:
        response = "Estas utilizando un metodo erroneo"
        return HttpResponseNotFound(response)


def process(request, resource):

    head = ("<h1><center>Aplicacion web para acortar URLs" +
            "</center></h1>")

    if request.method == "GET":
        short_url = "http://localhost:8000/" + resource

        try:
            url_search = url_type.objects.get(short_url=short_url)
            url_larga = url_search.large_url
        except url_type.DoesNotExist:
            return HttpResponseNotFound(head + "La URL solicitada no existe")

        response = ('<html><body>' + head + '<head>Estas siendo' +
                    ' redirigido...<meta ' + 'http-equiv="refresh"' +
                    ' content="1; url=' + str(url_larga) + '" />')
        HttpResponse.status_code = 302
        return HttpResponse(response)
    else:
        return HttpResponseNotFound("Metodo no permitido")