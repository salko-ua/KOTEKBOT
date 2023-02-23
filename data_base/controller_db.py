import aiosqlite
from contextvars import ContextVar

num = ContextVar("num",default= [])
kb_user_reg = ContextVar("keyskb", default= [])
kb_teachers_reg = ContextVar("kb_teachers_reg", default= [])
all_user = ContextVar('all_user_id',default=[])
user_id_group = ContextVar("ids", default=0)
count_us = ContextVar('count',default=0)
count_gr = ContextVar('count_gr',default=0)
count_teach = ContextVar('count_teach',default=0)
photka  = ContextVar("photo", default='')
photka_teachers  = ContextVar("photo_t", default='')
id_photka = ContextVar("id_photka", default='')
get_list = ContextVar("get_list", default='')
date_coupes = ContextVar('date_cop', default='')
date_calls= ContextVar('date_calls', default='')


async def bd_Start():
    global base
    global cur
    base = await aiosqlite.connect('data/database.db')
    cur = await base.cursor()
    if base:
        print('DATA BASE CONNECTED')
    await base.execute(
        """
        CREATE TABLE IF NOT EXISTS user(
            id         INTEGER PRIMARY KEY,
            user_id    INTEGER UNIQUE,
            Name       TEXT,
            Nickname   TEXT,
            group_user TEXT
        )
        """
    )
    await base.execute(
        """
        CREATE TABLE IF NOT EXISTS groupa(
            id        INTEGER PRIMARY KEY,
            user_id   INTEGER NOT NULL,
            groupname TEXT NOT NULL,
            photos    TEXT,
            date      TEXT
        )
        """
    )
    await base.execute(
        """
        CREATE TABLE IF NOT EXISTS all_photo(
            id         INTEGER PRIMARY KEY,
            id_photo   TEXT,
            type       TEXT,
            date_photo TEXT
        )
        """
    )
    await base.execute(
        """
        CREATE TABLE IF NOT EXISTS admin(
            id       INTEGER PRIMARY KEY NOT NULL,
            user_id  INTEGER UNIQUE NOT NULL,
            Name     TEXT,
            Nickname TEXT
        )
        """
    )
    await base.execute(
        """
        CREATE TABLE IF NOT EXISTS teachers(
            id       INTEGER PRIMARY KEY NOT NULL,
            user_id  INTEGER UNIQUE NOT NULL,
            Name     TEXT,
            Nickname TEXT,
            teacher_name TEXT
        )
        """
    )
    await base.execute(
        """
        CREATE TABLE IF NOT EXISTS teachers_name(
            id        INTEGER PRIMARY KEY,
            user_id   INTEGER NOT NULL,
            name_teacher TEXT NOT NULL,
            photos    TEXT,
            date      TEXT
        )
        """
    )
    await base.commit()


#================= ЗМІШАНЕ =================

async def add_calls_sql(types,id_photo,date_photo):
    id = 1
    ress = await cur.execute("SELECT `id` FROM all_photo WHERE id = ?", (id,))
    res = await ress.fetchall()
    if bool(len(res)) == False or res[0][0] != 1:
        await cur.execute("INSERT INTO `all_photo` (`id`) VALUES(?)", (id,))
        await cur.execute("UPDATE `all_photo` SET `type` = ?,`id_photo` = ?, date_photo = ? WHERE `id` = ?", (types,id_photo,date_photo,id,))
    elif  res[0][0] == 1:
        await cur.execute("UPDATE `all_photo` SET `type` = ?,`id_photo` = ?, date_photo = ? WHERE `id` = ?", (types,id_photo,date_photo,id,))
    return await base.commit()

async def delete_calls_sql():
    id = 1
    ress = await cur.execute("SELECT `id` FROM all_photo WHERE id = ?", (id,))
    res = await ress.fetchall()
    if bool(len(res)) == False or res[0][0] != 1:
        return False
    elif res[0][0] == 1:
        await cur.execute("DELETE FROM all_photo WHERE id = ?", (id,))
        await base.commit()
        return True

#================= ПЕРЕГЛЯД В ТАБЛИЦІ =================

#exists
async def user_exists_sql(user_id):
    result = await cur.execute("SELECT COUNT(`id`) FROM `user` WHERE `user_id` = ?", (user_id,))
    result = await result.fetchall()
    result = result[0][0]
    return bool(result)

async def admin_exists_sql(user_id):
    result = await cur.execute("SELECT COUNT(`id`) FROM `admin` WHERE `user_id` = ?", (user_id,))
    result = await result.fetchall()
    result = result[0][0]
    return bool(result)

async def teachers_exists_sql(user_id):
    result = await cur.execute("SELECT COUNT(`id`) FROM `teachers` WHERE `user_id` = ?", (user_id,))
    result = await result.fetchall()
    result = result[0][0]
    return bool(result)

async def teachers_name_exists_sql(name_teacher):
    result = await cur.execute("SELECT COUNT(`id`) FROM `teachers_name` WHERE `name_teacher` = ?", (name_teacher,))
    result = await result.fetchall()
    result = result[0][0]
    return bool(result)

async def group_exists_sql(groupname):
    result = await cur.execute("SELECT `groupname` FROM `groupa` WHERE `groupname` = ?", (groupname,))
    result = await result.fetchall()
    result = result[0][0]
    return bool(result)

async def user_group_exists_sql(text):
    result = await cur.execute("SELECT COUNT(`id`) FROM `user` WHERE `group_user` = ?", (text,))
    result = await result.fetchall()
    result = result[0][0]
    return bool(result)

async def teacher_name_exists_sql(text):
    result = await cur.execute("SELECT COUNT(`id`) FROM `teachers` WHERE `teacher_name` = ?", (text,))
    result = await result.fetchall()
    result = result[0][0]
    return bool(result)

async def group_exists_sql(groupname):
    result = await cur.execute("SELECT COUNT(`id`) FROM `groupa` WHERE `groupname` = ?", (groupname,))
    result = await result.fetchall()
    result = result[0][0]
    return bool(result)

#other

async def id_from_group_exists_sql(groupname):
    result = user_id_group.get()
    result = await cur.execute("SELECT `user_id` FROM `user` WHERE `group_user` = ?", (groupname,))
    rows = await result.fetchall()
    user_id_group.set(rows)
    return user_id_group.get()

async def all_user_id_sql():
    rest = all_user.get()
    rest = await cur.execute("SELECT `user_id` FROM `user`")
    rows = await rest.fetchall()
    all_user.set(rows)
    return all_user.get()

async def count_group_sql():
    reslt = count_gr.get()
    counts = await cur.execute("SELECT `id` FROM groupa")
    row = await counts.fetchall()
    if len(row) == 0:
        return False
    else:
        reslt = len(row)
        count_gr.set(reslt)
        return True

async def clear_sql():
    clears = kb_user_reg.get()
    clears.clear()
    kb_user_reg.set(clears)

async def group_list_sql():
    keys = kb_user_reg.get()
    reslt = await cur.execute('SELECT `groupname` FROM `groupa`')
    reslt = await reslt.fetchall()
    for i in reslt:
        keys.append(i[0])
    keys.sort()
    kb_user_reg.set(keys)
    return kb_user_reg.get()

async def clear_teachers_name_sql():
    clears = kb_teachers_reg.get()
    clears.clear()
    kb_teachers_reg.set(clears)

async def teachers_name_list_sql():
    keys = kb_teachers_reg.get()
    reslt = await cur.execute('SELECT `name_teacher` FROM `teachers_name`')
    reslt = await reslt.fetchall()
    for i in reslt:
        keys.append(i[0])
    keys.sort()
    kb_teachers_reg.set(keys)
    return kb_teachers_reg.get()

async def get_list_sql():
    await clear_sql()
    await group_list_sql()
    lists = kb_user_reg.get()
    reslt = get_list.get()
    if len(lists) == 0:
        return False
    else: 
        for i in range(0,len(lists)):
            reslt += str(i+1)+'. '+lists[i] +'\n'
        get_list.set(reslt)
        return True

async def see_rod_sql(user_id):
    #назва групи користувача
    groups = await cur.execute("SELECT `group_user` FROM `user` WHERE `user_id` = ?", (user_id,))
    rows_groups = await groups.fetchall()
    h = rows_groups[0][0]
    
    photo = await cur.execute("SELECT photos FROM groupa WHERE groupname = ?",(h,))
    rows_photo = await photo.fetchall()
    date = await cur.execute("SELECT `date` FROM groupa WHERE groupname = ?",(h,))
    rows_date = await date.fetchall()
    try:
        lens = len(rows_photo[0][0])
    except TypeError:
        lens = 1
    if lens <= 5:
        return False
    elif lens >=6:
        datka = date_coupes.get()
        reslt = photka.get()
        reslt = rows_photo[0][0]
        datka = rows_date[0][0]
        date_coupes.set(datka)
        photka.set(reslt)
        return True

async def see_rod_t_sql(user_id):
    #ініціали вчителя
    name = await cur.execute("SELECT `teacher_name` FROM `teachers` WHERE `user_id` = ?", (user_id,))
    rows_name = await name.fetchall()

    h = rows_name[0][0]
    
    photo = await cur.execute("SELECT photos FROM teachers_name WHERE name_teacher = ?",(h,))
    rows_photo = await photo.fetchall()
    date = await cur.execute("SELECT `date` FROM teachers_name WHERE name_teacher = ?",(h,))
    rows_date = await date.fetchall()
    try:
        lens = len(rows_photo[0][0])
    except TypeError:
        lens = 1
    if lens <= 5:
        return False
    elif lens >=6:
        datka = date_coupes.get()
        reslt = photka_teachers.get()
        reslt = rows_photo[0][0]
        datka = rows_date[0][0]
        date_coupes.set(datka)
        photka_teachers.set(reslt)
        return True

async def see_calls_sql():
    id = 1
    ress = await cur.execute("SELECT `id` FROM all_photo WHERE id = ?", (id,))
    res = await ress.fetchall()
    date = await cur.execute("SELECT `date_photo` FROM all_photo WHERE id = ?",(id,))
    rows_date = await date.fetchall()
    try:
        if  res[0][0] == 1:
            datka = date_calls.get()
            datka = rows_date[0][0]
            date_calls.set(datka)
            resulta = id_photka.get()
            res = await cur.execute("SELECT id_photo FROM all_photo WHERE id = ?", (id,))
            rows_res = await res.fetchall()
            resulta = rows_res[0][0]
            id_photka.set(resulta)
            return True
    except IndexError:
        return False

async def count_user_sql():
    reslt = count_us.get()
    counts = await cur.execute("SELECT `id` FROM user")
    row_counts = await counts.fetchall()
    if len(row_counts) == 0:
        return False
    else:
        reslt = len(row_counts)
        count_us.set(reslt)
        return True
    
async def count_teacher_sql():
    reslt = count_teach.get()
    counts = await cur.execute("SELECT `id` FROM teachers")
    row_counts = await counts.fetchall()
    if len(row_counts) == 0:
        return False
    else:
        reslt = len(row_counts)
        count_teach.set(reslt)
        return True


#================= ОНОВЛЕННЯ В ТАБЛИЦІ =================

async def group_photo_update_sql(photo, groupname,transl):
    await cur.execute("UPDATE `groupa` SET photos = ?, date = ? WHERE groupname = ?", (photo,transl,groupname,))
    return await base.commit()

async def teacher_photo_update_sql(photo, name_teacher,transl):
    await cur.execute("UPDATE `teachers_name` SET photos = ?, date = ? WHERE name_teacher = ?", (photo,transl,name_teacher,))
    return await base.commit()

#================= ДОДАВАННЯ В ТАБЛИЦІ =================

async def add_admin_sql(user_id, Name, Nickname):
    await cur.execute("INSERT INTO `admin` (`user_id`, `Name`, `Nickname`) VALUES (?,?,?)", (user_id, Name, Nickname))
    return await base.commit()

async def add_user_sql(user_id, Name, Nickname, groupe):
    await cur.execute("INSERT INTO `user` (`user_id`, `Name`, `Nickname`, `group_user`) VALUES (?,?,?,?)", (user_id, Name, Nickname, groupe))
    return await base.commit()

async def add_group_sql(user_id, group):
    await cur.execute("INSERT INTO `groupa` (`user_id`,`groupname`) VALUES (?,?)", (user_id, group))
    return await base.commit()

async def add_teachers_sql(user_id, Name, Nickname, teachers_name):
    await cur.execute("INSERT INTO `teachers` (`user_id`, `Name`, `Nickname`, `teacher_name`) VALUES (?,?,?,?)", (user_id, Name, Nickname, teachers_name))
    return await base.commit()

async def add_teachers_name_sql(user_id, name_teacher):
    await cur.execute("INSERT INTO `teachers_name` (`user_id`,`name_teacher`) VALUES (?,?)", (user_id, name_teacher))
    return await base.commit()


#================= ВИДАЛЕННЯ В ТАБЛИЦІ =================

async def delete_users_sql(user_id):
    await cur.execute("DELETE FROM user WHERE user_id = ?", (user_id,))
    return await base.commit()

async def delete_teachers_sql(user_id):
    await cur.execute("DELETE FROM teachers WHERE user_id = ?", (user_id,))
    return await base.commit()

async def delete_admins_sql(user_id):
    await cur.execute("DELETE FROM admin WHERE user_id = ?", (user_id,))
    return await base.commit()

async def delete_groups_sql(text):
    await cur.execute("DELETE FROM groupa WHERE groupname = ?", (text,))
    return await base.commit()

async def delete_name_techers_sql(text):
    await cur.execute("DELETE FROM teachers_name WHERE name_teacher = ?", (text,))
    return await base.commit()

async def delete_teachers_name_sql(text):
    await cur.execute("DELETE FROM teachers WHERE teacher_name = ?", (text,))
    return await base.commit()

async def delete_user_groups_sql(text):
    await cur.execute("DELETE FROM user WHERE group_user = ?", (text,))
    return await base.commit()


#ONLYSUPERADMIN
list_all_user = ContextVar("list_all_user", default=[])
list_all_user_for_group = ContextVar("list_all_user_for_group", default=[])
list_all_groupa = ContextVar("list_all_groupa", default=[])
list_all_admin = ContextVar("list_all_admin", default=[])

#Переглянути таблицю користувачів
async def user_all_sql():
    keys = list_all_user.get()
    keys.clear()
    list_all_user.set(keys)
    result = await cur.execute("SELECT * FROM `user`")
    list_r = await result.fetchall()
    if len(list_r) == 0:
        return True
    elif len(list_r) > 0:
        for i in list_r:
            keys.append(i)
        reslt = ''
        for i in range(0,len(keys)):
            reslt += str(i+1)+'. '+ str(keys[i]) +'\n'
        list_all_user.set(reslt)
        return False

#Переглянути таблицю користувачів за групою
async def user_for_group_sql(groupe):
    keys = list_all_user_for_group.get()
    keys.clear()
    list_all_user_for_group.set(keys)
    result = await cur.execute("SELECT * FROM `user` WHERE group_user = ?",(groupe,))
    list_r = await result.fetchall()
    if len(list_r) == 0:
        return True
    elif len(list_r) > 0:
        for i in list_r:
            keys.append(i)
        reslt = ''
        for i in range(0,len(keys)):
            reslt += str(i+1)+'. '+ str(keys[i]) +'\n'
        list_all_user_for_group.set(reslt)
        return False

#Переглянути таблицю гурп
async def groupa_all_sql():
    keys = list_all_groupa.get()
    keys.clear()
    list_all_groupa.set(keys)
    result = await cur.execute("SELECT * FROM `groupa`")
    list_r = await result.fetchall()
    if len(list_r) == 0:
        return True
    elif len(list_r) > 0:
        for i in list_r:
            keys.append(i)
        reslt = ''
        for i in range(0,len(keys)):
            reslt += str(i+1)+'. '+ str(keys[i]) +'\n'
        list_all_groupa.set(reslt)
        return False

#Переглянути таблицю адмінів
async def admin_all_sql():
    keys = list_all_admin.get()
    keys.clear()
    list_all_admin.set(keys)
    result = await cur.execute("SELECT * FROM `admin`")
    list_r = await result.fetchall()
    if len(list_r) == 0:
        return True
    elif len(list_r) > 0:
        for i in list_r:
            keys.append(i)
        reslt = ''
        for i in range(0,len(keys)):
            reslt += str(i+1)+'. '+ str(keys[i]) +'\n'
        list_all_admin.set(reslt)
        return False