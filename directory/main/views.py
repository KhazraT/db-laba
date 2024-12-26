from django.shortcuts import render, redirect
from . import database as db
import re
# проверка на удаление(если встречается в таблице main то удалить выбранным способом)
# обработка ошибок при добавлении и удалении и поиске
# проверка на ввод строку

connection = db.connect_to_database()

# Create your views here.
def index(request):
    return render(request, 'index.html')

def fam(request):
    context = {}
    if request.GET:
        fam = request.GET.get('fam', None)
        action = request.GET.get('action')
        if action == 'Показать все записи' or len(fam) > 20:
            return redirect('fam')
        

        is_exists = db.is_exists(connection, table='fam', condition=f'f_val=\'{fam}\'')
        # print(is_exists)
        if action == 'Добавить' and is_exists == False:
            db.insert_into_sub_tables(connection, 'fam', "f_val", "'" + fam + "'")
        elif action == 'Удалить' and is_exists == True:
            try:
                db.delete_value_from_table(connection, 'fam', f'f_val = \'{fam}\'')
            except: pass
        elif action == 'Найти':
            rows = db.select_from_sub_table(connection, 'fam', condition=f'f_val LIKE \'%{fam}%\'')
            context['rows'] = rows
            return render(request, 'fam.html', context=context)

        return redirect('fam')

    rows = db.select_from_sub_table(connection, 'fam')
    context['rows'] = rows

    return render(request, 'fam.html', context=context)

def name(request):
    context = {}
    if request.GET:
        name = request.GET.get('name', None)
        action = request.GET.get('action')
        if action == 'Показать все записи' or len(name) > 20:
            return redirect('name')
        

        is_exists = db.is_exists(connection, table='name_', condition=f'nam_val=\'{name}\'')
        # print(is_exists)
        if action == 'Добавить' and is_exists == False:
            db.insert_into_sub_tables(connection, 'name_', "nam_val", "'" + name + "'")
        elif action == 'Удалить' and is_exists == True:
            try:
                db.delete_value_from_table(connection, 'name_', f'nam_val = \'{name}\'')
            except: pass
        elif action == 'Найти':
            rows = db.select_from_sub_table(connection, 'name_', condition=f'nam_val LIKE \'%{name}%\'')
            context['rows'] = rows
            return render(request, 'name.html', context=context)

        return redirect('name')

    rows = db.select_from_sub_table(connection, 'name_')
    context['rows'] = rows

    return render(request, 'name.html', context=context)

def otc(request):
    context = {}
    if request.GET:
        otc = request.GET.get('otc', None)
        action = request.GET.get('action')
        if action == 'Показать все записи' or len(otc) > 20:
            return redirect('otc')
        

        is_exists = db.is_exists(connection, table='otc', condition=f'otc_val=\'{otc}\'')
        # print(is_exists)
        if action == 'Добавить' and is_exists == False:
            db.insert_into_sub_tables(connection, 'otc', "otc_val", "'" + otc + "'")
        elif action == 'Удалить' and is_exists == True:
            try:
                db.delete_value_from_table(connection, 'otc', f'otc_val = \'{otc}\'')
            except: pass
        elif action == 'Найти':
            rows = db.select_from_sub_table(connection, 'otc', condition=f'otc_val LIKE \'%{otc}%\'')
            context['rows'] = rows
            return render(request, 'otc.html', context=context)

        return redirect('otc')

    rows = db.select_from_sub_table(connection, 'otc')
    context['rows'] = rows

    return render(request, 'otc.html', context=context)

def street(request):
    context = {}
    if request.GET:
        street = request.GET.get('street', None)
        action = request.GET.get('action')
        if action == 'Показать все записи' or len(street) > 20:
            return redirect('street')
        

        is_exists = db.is_exists(connection, table='street', condition=f's_val=\'{street}\'')
        # print(is_exists)
        if action == 'Добавить' and is_exists == False:
            db.insert_into_sub_tables(connection, 'street', "s_val", "'" + street + "'")
        elif action == 'Удалить' and is_exists == True:
            try:
                db.delete_value_from_table(connection, 'street', f's_val = \'{street}\'')
            except: pass
        elif action == 'Найти':
            rows = db.select_from_sub_table(connection, 'street', condition=f's_val LIKE \'%{street}%\'')
            context['rows'] = rows
            return render(request, 'street.html', context=context)

        return redirect('street')

    rows = db.select_from_sub_table(connection, 'street')
    context['rows'] = rows

    return render(request, 'street.html', context=context)

def main(request):
    context = {}
    fams = db.select_from_sub_table(connection, 'fam', 'f_val')
    names = db.select_from_sub_table(connection, 'name_', 'nam_val')
    otcs = db.select_from_sub_table(connection, 'otc', 'otc_val')
    streets = db.select_from_sub_table(connection, 'street', 's_val')
    context['fams'] = fams
    context['names'] = names
    context['otcs'] = otcs
    context['streets'] = streets
    if request.GET:
        # print(request.GET)
        fam = request.GET.get('fam', None)
        name = request.GET.get('name', None)
        otc = request.GET.get('otc', None)
        street = request.GET.get('street', None)
        bldn = request.GET.get('bldn', None)
        bldn_kor = request.GET.get('bldn_kor', None)
        appr = request.GET.get('appr', None)
        telef = request.GET.get('telef', None)

        action = request.GET.get('action')
        if action == 'Показать все записи':
            return redirect('main')

        where = []
        del_ = []
        arr = []
        if fam != "Выберете фамилию":
            where.append(f"fam.f_val='{fam}'")
            fam_id = db.select_from_sub_table(connection, 'fam', 'f_num', f'f_val=\'{fam}\'')
            del_.append(f"{fam_id[0][0]}")
            arr.append(f"fam={fam_id[0][0]}")
        if name != "Выберете имя":
            where.append(f"name_.nam_val='{name}'")
            name_id = db.select_from_sub_table(connection, 'name_', 'n_num', f'nam_val=\'{name}\'')
            del_.append(f"{name_id[0][0]}")
            arr.append(f"name_={name_id[0][0]}")
        if otc != "Выберете отчество":
            where.append(f"otc.otc_val='{otc}'")
            otc_id = db.select_from_sub_table(connection, 'otc', 'otc_n', f'otc_val=\'{otc}\'')
            del_.append(f"{otc_id[0][0]}")
            arr.append(f"sndname={otc_id[0][0]}")
        if street != "Выберете улицу":
            where.append(f"street.s_val='{street}'")
            street_id = db.select_from_sub_table(connection, 'street', 's_num', f's_val=\'{street}\'')
            del_.append(f"{street_id[0][0]}")
            arr.append(f"street={street_id[0][0]}")
        if bldn != '':
            where.append(f"bldn='{bldn}'")
            del_.append(f"'{bldn}'")
            arr.append(f"bldn='{bldn}'")
        if bldn_kor != '':
            where.append(f"bldn_kor='{bldn_kor}'")
            del_.append(f"'{bldn_kor}'")
            arr.append(f"bldn_kor='{bldn_kor}'")
        if appr != '':
            where.append(f"appr={appr}")
            del_.append(f"{appr}")
            arr.append(f"appr={appr}")
            
        if telef != '' and re.search("^\+[0-9]{11}", telef):
            where.append(f"telef='{telef}'")
            del_.append(f"'{telef}'")
            arr.append(f"telef='{telef}'")
            telef_ = db.is_exists(connection, 'main', condition=f"telef='{telef}'")
            if telef_:
                return redirect('main')
        # print(" AND ".join(where))

        action = request.GET.get('action')

        # is_exists = db.is_exists(connection, table='street', condition=f's_val=\'{street}\'')
        if action == 'Добавить' and len(del_) == 8:
            print(del_)
            db.insert_into_main(connection, 'main (fam, name_, sndname, street, bldn, bldn_kor, appr, telef)', "(" + ", ".join(del_) + ")")
        elif action == 'Удалить' and len(where) > 0:
            db.delete_value_from_table(connection, 'main', condition=" AND ".join(arr))
        elif action == 'Найти' and len(where) > 0:
            rows = db.select_from_main_table(connection, condition=" AND ".join(where))
            context['rows'] = rows
            return render(request, 'main.html', context=context)
        else:
            return redirect('main')

    rows = db.select_from_main_table(connection)
    context['rows'] = rows
    
    fams = db.select_from_sub_table(connection, 'fam', 'f_val')
    names = db.select_from_sub_table(connection, 'name_', 'nam_val')
    otcs = db.select_from_sub_table(connection, 'otc', 'otc_val')
    streets = db.select_from_sub_table(connection, 'street', 's_val')
    context['fams'] = fams
    context['names'] = names
    context['otcs'] = otcs
    context['streets'] = streets

    return render(request, 'main.html', context=context)

def create_tables():
    pass

def drop_tables():
    pass