#widgets.py
# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from administrador.models import IDIOMAS
from django import forms
#ESTAS LINEAS DE CODIGO SON PARA DEPURACION
# import pdb
# pdb.set_trace()

from django.contrib.admin.templatetags.admin_static import static
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.forms.util import flatatt
from django.utils.html import conditional_escape, format_html, format_html_join
from itertools import chain
from django.forms import *
from django.forms.widgets import Input,SelectMultiple,Widget

class SelectMultipleCustom(SelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
    	# output = super(SelectMultipleCustom, self).render(name,value,attrs,choices)
    	# return output
        if value is None: value = []  
        
        if name=='permissions' or name=='user_permissions':
            var='Permisos'
        elif name =='groups':
            var='Grupos'
        else:
            var=name

        attrs['class']='vTextField span4'
        attrs['style']='height:300px ;'
        attrs2={}
        attrs2.update(attrs)
        attrs2['style']+=" margin:0 60px 0 0;"
        attrs3={}
        attrs3.update(attrs2)
        attrs3['style']+=" display:none;"
        final_attrs = self.build_attrs(attrs3, name=name)
        output = []
        
        # import pdb
        # pdb.set_trace()
        
        output.append (format_html("<div class='container'>"))
        output.append (format_html("<div class='row-fluid'>"))
        output.append(format_html("<input type='text' id='search-{0}' class='span3' style='margin:0 0 10px 0;' autocomplete='off' placeholder='Buscar: {1}'>",name,var))
        output.append(format_html("</div>"))

        output.append(format_html("""<div class='row-fluid' style="background: transparent url('/static/admin/img/switch.png') no-repeat 390px 120px;">"""))
        
        output.append(format_html('<select id="selectable-copia-{0}" multiple="multiple"{1}>', name,flatatt(final_attrs)))
        options = self.render_options(choices, value,'3','selectable-elem')
        if options:
            output.append(options)
        output.append('</select>')

        # import pdb
        # pdb.set_trace()
        
        final_attrs = self.build_attrs(attrs2, name=name)
        output.append(format_html('<select id="selectable-{0}" multiple="multiple"{1}>', name,flatatt(final_attrs)))
        options = self.render_options(choices, value,'1','selectable-elem')
        if options:
            output.append(options)
        output.append('</select>')
        
        attrs['name'] = name
        final_attrs = self.build_attrs(attrs, name=name)
        output.append(format_html('<select id="selection-{0}" multiple="multiple"{1}>', name,flatatt(final_attrs)))
        options = self.render_options(choices, value,'2','selection-elem')
        if options:
            output.append(options)
        output.append('</select>')

        # output.append(mark_safe("""<script type="text/javascript">$("#searchable-%s").multiSelect({selectableHeader: "<input type='text' id='search-%s' class='span12' autocomplete='off' placeholder='Buscar: %s'>"});</script>""" % (var,var,var)))
        tupla = [name for i in range(47)]
        tupla = tuple(tupla)
        output.append(mark_safe("""<script type="text/javascript">
            $('#search-%s').on('keypress',filtrar_%s);
            $('#search-%s').on('keyup',filtrar_%s);
            function filtrar_%s(e)
            {
                filtro = $(this).val();
                $selected = $($("#selectable-%s")[0]);
                $copia = $($("#selectable-copia-%s")[0]);
                $("#selectable-%s .selectable-elem").detach()
                hijos = $copia.children();
                if(filtro!='')
                {
                    exp = /^[\w ]+$/
                    if(exp.test(filtro))
                    {
                        for(x=0;x<hijos.length;x++)
                        {
                            chr=hijos[x].innerHTML;
                            if(chr.indexOf(filtro)!=-1)
                            {
                                temp = $('#selection-%s option[value='+hijos[x].value+']');
                                if(temp.length==0)
                                {
                                    $nodo = $(hijos[x].cloneNode(true));
                                    //$nodo.on('mouseover',seleccionar_%s);
                                    //$nodo.on('click',cargar_%s);
                                    //nodo.addEventListener('onmouseover',seleccionar_%s);
                                    //nodo.onmouseover = seleccionar_%s;
                                    //nodo.addEventListener('click',cargar_%s);
                                    //nodo.click = cargar_%s;
                                    $selected.append($nodo);
                                }
                            }
                        }
                    }
                }
                else
                {
                    for(x=0;x<hijos.length;x++)
                    {
                        temp = $('#selection-%s option[value='+hijos[x].value+']');
                        if(temp.length==0)
                        {
                            $nodo = $(hijos[x].cloneNode(true));
                            $nodo.on('mouseover',seleccionar_%s);
                            $nodo.on('click',cargar_%s);
                            $selected.append($nodo);
                        }
                    }
                }

            }
            $('#selectable-%s .selectable-elem').on('click',cargar_%s);
            $("#selectable-copia-%s .selectable-elem").on('click',cargar_%s);
            function cargar_%s(e)
            {
                elemento = e.target;
                $nuevo = $(document.createElement("option"));
                $nuevo.addClass('selection-elem');
                $nuevo.attr('name','%s');
                $nuevo.val(elemento.value);
                $nuevo.html(elemento.innerHTML);
                $nuevo.on('mouseover',seleccionar2_%s);
                $nuevo.on('click',devolver_%s);
                
                $('#selectable-%s option[value='+elemento.value+']').remove();
                $('#selection-%s').append($nuevo);

            }
            $('#selectable-%s .selectable-elem').on('mouseover',seleccionar_%s);
            $("#selectable-copia-%s .selectable-elem").on('click',seleccionar_%s);
            function seleccionar_%s(e)
            {
                elems = $("#selectable-%s .selectable-elem[selected='true']");
                for(x=0; x<elems.length;x++)
                {
                    elems[x].removeAttribute("selected");
                }
                elemento = e.target;
                elemento.setAttribute("selected","true");

                parent = $("#selectable-%s")
                parent.blur()
                parent.focus()

                return false;
            }

            $('#selection-%s .selection-elem').on('mouseover',seleccionar2_%s);
            function seleccionar2_%s(e)
            {
                elems = $("#selection-%s .selection-elem[selected='true']");
                for(x=0; x<elems.length;x++)
                {
                    elems[x].removeAttribute("selected");
                }
                elemento = e.target;
                elemento.setAttribute("selected","true");

                parent = $("#selection-%s")
                parent.blur()
                parent.focus()

                return false;
            }

            $('#selection-%s .selection-elem').on('click',devolver_%s);
            function devolver_%s(e)
            {
                elemento = e.target;

                $nuevo = $(document.createElement("option"));
                $nuevo.addClass('selectable-elem');
                $nuevo.val(elemento.value);
                $nuevo.html(elemento.innerHTML);
                $nuevo.on('mouseover',seleccionar_%s);
                $nuevo.on('click',cargar_%s);
                
                $('#selection-%s option[value='+elemento.value+']').remove();
                $('#selectable-%s').append($nuevo);
            }
            </script>
            """% tupla))
    
        
        output.append(format_html("</div>"))
        output.append(format_html("</div>"))
        return mark_safe('\n'.join(output))

    def render_option(self, selected_choices, option_value, option_label,className):
        option_value = force_text(option_value)
        return format_html('<option class="{0}" value="{1}">{2}</option>',
            className,
            option_value,
            force_text(option_label))
    def render_options(self, choices, selected_choices,exclude,className):
        # Normalize to strings.
        selected_choices = set(force_text(v) for v in selected_choices)
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if exclude=='1': #Se excluyen los elementos que no esten seleccionados
                if not str(option_value) in selected_choices:
                    output.append(self.render_option(selected_choices, option_value, option_label, className))
            elif exclude=='2':#Se excluyen los elementos que esten seleccionados
                if str(option_value) in selected_choices:
                    output.append(self.render_option(selected_choices, option_value, 
                            option_label,className))
            else: #Se incluyen todos elementos
                output.append(self.render_option(selected_choices, option_value, 
                        option_label,className))

        return '\n'.join(output)
    def build_attrs(self, extra_attrs=None, **kwargs):
        "Helper function for building an attribute dictionary."
        attrs = {}
        if extra_attrs:
            attrs.update(extra_attrs)
        return attrs

class MapInput(Input):
    datos = {}
    def __init__(self, attrs=None, data=None):
        super(MapInput, self).__init__(attrs=attrs)
        if isinstance(data,dict):
            self.datos = data
        else:
            self.datos=None
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        final_attrs['type'] ='text'
        final_attrs['style'] = 'margin:0 0 10px 0;'
    
        output = [format_html("""<script src="http://maps.google.com/maps/api/js?sensor=true"></script>""")]

        output.append(format_html("""<script src="/static/js/gmaps.js"></script>"""))
        output.append(format_html("""<div class="span8">"""))
        output.append(format_html("""<div class="row">"""))
        output.append(format_html("""<div class='span5'>"""))
        output.append(format_html('<input{0} placeholder="Buscar: Ciudad, Estado, Pais" />', flatatt(final_attrs)))
        output.append(format_html("""</div>"""))
        output.append(format_html("""<div class='span3'>"""))
        output.append(format_html("""<button id='bt-eliminar' class="btn btn-danger">Eliminar marca</button>"""))
        output.append(format_html("""</div>"""))
        output.append(format_html("""</div>"""))
        output.append(format_html("""<div class="row">"""))
        output.append(format_html("""<div id='mapa' class='span10'></div>"""))
        output.append(mark_safe("""<script> map = new GMaps(
            {
            div: '#mapa', 
            height : '400px',
            lat: 24.143131 ,
            lng: -110.31106,
            click: function mapa_click(e) {
                if(map.markers.length>0)
                {
                    map.removeMarkers()
                }
                map.addMarker({
                    lat: e.latLng.lat(),
                    lng: e.latLng.lng()
                });
            },
        });
        $('#id_MAPA').on('keypress',clic);
        function clic(e)
        {
            if(e.charCode==13)
            {
                GMaps.geocode({
                  address: $('#id_MAPA').val(),
                  callback: function(results, status) {
                    if (status == 'OK') {
                      var latlng = results[0].geometry.location;
                      map.setCenter(latlng.lat(), latlng.lng());
                      map.addMarker({
                        lat: latlng.lat(),
                        lng: latlng.lng()
                      });
                    }
                    }
                });
                return false;
            }
        }
        $('#bt-eliminar').on('click',eliminar_marca)
        function eliminar_marca(e)
        {
            if(map.markers.length>0)
            {
                map.removeMarkers()
            }
            return false;
        }
        </script>
        </div>
        </div>"""))
        # import pdb
        # pdb.set_trace()
        band=False
        if self.datos is not None:
            if (self.datos.__contains__('LATITUD') and self.datos.__contains__('LONGITUD')):
                if (self.datos['LATITUD'] != "" and self.datos['LONGITUD']!=""):
                    latitud= self.datos['LATITUD']
                    longitud = self.datos['LONGITUD']
                    band=True
                else:
                    band=False
            else:
                band=False
        else:
            band=False
        
        if band:
            output.append(mark_safe("""<script>
                    map.setCenter("""+latitud+""", """+longitud+""");
                    map.addMarker({
                        lat: """+latitud+""",
                        lng: """+longitud+"""
                    });
                </script>
                """))
        return mark_safe('\n'.join(output))


class AccordionMultipleTextbox(Widget):
    datos = {}
    def __init__(self, attrs=None, data=None):
        super(AccordionMultipleTextbox, self).__init__(attrs=attrs)
        if isinstance(data,dict):
            self.datos = data
        else:
            self.datos=None

    def render(self, name, value, attrs=None):
        if value is None: value = ''
        

        attrs_finales = flatatt(self.attrs)
        output= [mark_safe("""<div class='row'>""")]
        output.append(mark_safe("""<div class='span8'>"""))
        output.append(mark_safe("""<ul class="nav nav-tabs" id="ul_%s">""" % (name)))
        output.append(mark_safe("""<li class="active"><a href="#"""+name+"""">Español</a></li>"""))
        for idioma in IDIOMAS:
            output.append(mark_safe("<li><a href='#"+name+"_"+idioma[0]+"'>"+idioma[1]+"</a></li>"))
        output.append(mark_safe("""</ul>"""))
        output.append(mark_safe("""<div class="tab-content">"""))
        
        band=False
        if self.datos is not None:
            if self.datos.__contains__(u'Español'):
                if self.datos[u'Español'] != "":
                    band=True
                else:
                    band=False
            else:
                band=False
        else:
            band=False

        # import pdb
        # pdb.set_trace()
        if band:
            output.append(mark_safe("""
                    <div class='tab-pane active' id='"""+name+"""'>
                        <textarea name='"""+name+"""' %s placeholder='Descripción en Español'>"""+self.datos[u'Español']+"""
                        </textarea>
                    </div>
                """) % attrs_finales)
        else:
            output.append(mark_safe("""
                    <div class='tab-pane active' id='"""+name+"""'>
                        <textarea name='"""+name+"""' %s placeholder='Descripción en Español'></textarea>
                    </div>
                """)% attrs_finales)
        for idioma in IDIOMAS:
            band=False
            if self.datos is not None:
                if self.datos.__contains__(idioma[0]):
                    if self.datos[idioma[0]] != "":
                        band=True
                    else:
                        band=False
                else:
                    band=False
            else:
                band=False
            if band:
                output.append(mark_safe("""
                        <div class='tab-pane' id='"""+name+"_"+idioma[0]+"""'>
                            <textarea name="""+name+"""_"""+idioma[0]+""" placeholder='Descripción en """+idioma[1]+"""'  %s>"""+self.datos[idioma[0]]+"""
                            </textarea>
                        </div>
                    """) % attrs_finales )
            else:                
                output.append(mark_safe("""
                        <div class='tab-pane' id='"""+name+"_"+idioma[0]+"""'>
                            <textarea name="""+name+"""_"""+idioma[0]+""" placeholder='Descripción en """+idioma[1]+"""' %s></textarea>
                        </div>
                    """) % attrs_finales)
        output.append(mark_safe("""</div>"""))
        output.append(mark_safe("""
            <script>
                $(function () {
                    $('#ul_%s a:first').tab('show');
                })
                $('#ul_%s a').click(function (e) {
                  e.preventDefault();
                  $(this).tab('show');
                })
                </script>
            </div>
        </div>
        """ % (name,name)))
        return mark_safe('\n'.join(output))



class AccordionMultiplesSimpleTextbox(Widget):
    datos = {}
    def __init__(self, attrs=None, data=None):
        super(AccordionMultiplesSimpleTextbox, self).__init__(attrs=attrs)
        if isinstance(data,dict):
            self.datos = data
        else:
            self.datos=None

    def render(self, name, value, attrs=None):
        if value is None: value = ''
        
        # import pdb
        # pdb.set_trace()
        attrs_finales = flatatt(self.attrs)
        output= [mark_safe("""<div class='row'>""")]
        output.append(mark_safe("""<div class='span8'>"""))
        output.append(mark_safe("""<ul class="nav nav-tabs" id="ul_%s">""" % (name)))
        output.append(mark_safe("""<li class="active"><a href="#"""+name+"""">Español</a></li>"""))
        for idioma in IDIOMAS:
            output.append(mark_safe("<li><a href='#"+name+"_"+idioma[0]+"'>"+idioma[1]+"</a></li>"))
        output.append(mark_safe("""</ul>"""))
        output.append(mark_safe("""<div class="tab-content">"""))
        
        band=False
        if self.datos is not None:
            if self.datos.__contains__(u'Español'):
                if self.datos[u'Español'] != "":
                    band=True
                else:
                    band=False
            else:
                band=False
        else:
            band=False

        if band:
            output.append(mark_safe("""
                    <div class='tab-pane active' id='"""+name+"""'>
                        <input type='text' class='vTextField span10' name='"""+name+"""' placeholder='Descripción en Español' value='"""+self.datos[u'Español']+"""' %s>
                    </div>
                """ % attrs_finales))
        else:
            output.append(mark_safe("""
                    <div class='tab-pane active' id='"""+name+"""'>
                        <input type='text' class='vTextField span10' name='"""+name+"""' value='' placeholder='Descripción en Español' %s>
                    </div>
                """ % attrs_finales))
        for idioma in IDIOMAS:
            band=False
            if self.datos is not None:
                if self.datos.__contains__(idioma[0]):
                    if self.datos[idioma[0]] != "":
                        band=True
                    else:
                        band=False
                else:
                    band=False
            else:
                band=False
            if band:
                output.append(mark_safe("""
                        <div class='tab-pane' id='"""+name+"_"+idioma[0]+"""'>
                            <input type='text' class='vTextField span10' name="""+name+"""_"""+idioma[0]+""" placeholder='Descripción en """+idioma[1]+"""' value='"""+self.datos[idioma[0]]+"""' %s>
                        </div>
                    """)% attrs_finales)
            else:                
                output.append(mark_safe("""
                        <div class='tab-pane' id='"""+name+"_"+idioma[0]+"""'>
                            <input type='text' class='vTextField span10' name="""+name+"""_"""+idioma[0]+""" value='' placeholder='Descripción en """+idioma[1]+"""' %s>
                        </div>
                    """ % attrs_finales))
        output.append(mark_safe("""</div>"""))
        output.append(mark_safe("""
            <script>
                $(function () {
                    $('#ul_%s a:first').tab('show');
                })
                $('#ul_%s a').click(function (e) {
                  e.preventDefault();
                  $(this).tab('show');
                })
                </script>
            </div>
        </div>
        """ % (name,name)))
        return mark_safe('\n'.join(output))


class VerInput(Input):
    datos = {}
    def __init__(self, attrs=None, data=None):
        super(VerInput, self).__init__(attrs=attrs)
        if isinstance(data,dict):
            self.datos = data
        else:
            self.datos=None
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        # import pdb
        # pdb.set_trace()
        final_attrs = self.build_attrs(self.attrs, name=name)
        attrs_finales = flatatt(final_attrs)
        output = []
        output.append(mark_safe("""
            <textarea %s>%s</textarea><button id='ver_comentario' class='btn btn-info' style='margin: 0 0 0 10px;'>Ver comentario</button>
        """ % (attrs_finales,value)))
        if self.datos is not None:
            if ( self.datos.__contains__('tipo_comentario') and self.datos.__contains__('id')):
                output.append(mark_safe("""
                <script>
                    $('#ver_comentario').on('click',ver_comentario);
                    function ver_comentario(e)
                    {
                        tipo='%s'
                        if(tipo=='E')
                        {
                            location.href='/admin/administrador/comentario_evento/%s/';
                        }
                        if(tipo=='R')
                        {
                            location.href='/admin/administrador/comentario_relato/%s/';
                        }
                        if(tipo=='P')
                        {
                            location.href='/admin/administrador/comentario_pueblo/%s/';
                        }
                        if(tipo=='S')
                        {
                            location.href='/admin/administrador/comentario_sitio/%s/';
                        }
                        return false;
                    }
                </script>
                """%(self.datos['tipo_comentario'],self.datos['id'],self.datos['id'],self.datos['id'],self.datos['id'])))

        return mark_safe('\n'.join(output))