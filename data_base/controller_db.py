import sqlite3
from contextvars import ContextVar


kb_user_reg = ContextVar("keyskb", default= [])
user_id_group = ContextVar("ids", default=0)
all_user = ContextVar('all_user_id',default=[])
photka  = ContextVar("photo", default="")
id_photka = ContextVar("id_photka", default="")
count_us = ContextVar('count',default=0)
count_gr = ContextVar('count_gr',default=0)
get_list = ContextVar("get_list", default="")
date_coupes = ContextVar('date_cop', default='')
date_calls= ContextVar('date_calls', default='')



def bd_Start():
    global base
    global cur
    base = sqlite3.connect('data/database.db')
    cur = base.cursor()
    if base:
        print('DATA BASE CONNECTED')
    base.execute(
        """
        CREATE TABLE IF NOT EXISTS user(
            id         INTEGER PRIMARY KEY,
            user_id    INTEGER UNIQUE,
            Name       TEXT,
            Nickname   TEXT,
            group_user TEXT
        );

        CREATE TABLE IF NOT EXISTS groupa(
            id        INTEGER PRIMARY KEY,
            user_id   INTEGER NOT NULL,
            groupname TEXT NOT NULL,
            photos    TEXT,
            date      TEXT
        );

        CREATE TABLE IF NOT EXISTS all_photo(
            id         INTEGER PRIMARY KEY,
            id_photo   TEXT,
            type       TEXT,
            date_photo TEXT
        );

        CREATE TABLE IF NOT EXISTS admin(
            id       INTEGER PRIMARY KEY NOT NULL,
            user_id  INTEGER UNIQUE NOT NULL,
            Name     TEXT,
            Nickname TEXT
        )
        """
    )
    base.commit()





async def user_exists_sql(user_id):
    result = cur.execute("SELECT `id` FROM `user` WHERE `user_id` = ?", (user_id,))
    return bool(len(result.fetchall()))


async def admin_exists_sql(user_id):
    result = cur.execute("SELECT `id` FROM `admin` WHERE `user_id` = ?", (user_id,))
    return bool(len(result.fetchall()))

async def group_exists_sql(groupname):
    result = cur.execute("SELECT `groupname` FROM `groupa` WHERE `groupname` = ?", (groupname,))
    return bool(len(result.fetchall()))

async def user_group_exists_sql(text):
    result = cur.execute("SELECT `id` FROM `user` WHERE `group_user` = ?", (text,))
    return bool(len(result.fetchall()))

async def group_photo_update_sql(photo, groupname,transl):
    cur.execute("UPDATE `groupa` SET photos = ?, date = ? WHERE groupname = ?", (photo,transl,groupname,))
    return base.commit()


async def id_from_group_exists_sql(groupname):
    result = user_id_group.get()
    result = cur.execute("SELECT `user_id` FROM `user` WHERE `group_user` = ?", (groupname,)).fetchall()
    user_id_group.set(result)
    return user_id_group.get()

async def all_user_id_sql():
    rest = all_user.get()
    rest = cur.execute("SELECT `user_id` FROM `user`").fetchall()
    all_user.set(rest)
    return all_user.get()


async def add_user_sql(user_id, Name, Nickname, groupe):
    cur.execute("INSERT INTO `user` (`user_id`, `Name`, `Nickname`, `group_user`) VALUES (?,?,?,?)", (user_id, Name, Nickname, groupe))
    return base.commit()

async def add_calls_sql(types,id_photo,date_photo):
    id = 1
    ress = cur.execute("SELECT `id` FROM all_photo WHERE id = ?", (id,))
    res = ress.fetchall()
    if bool(len(res)) == False or res[0][0] != 1:
        cur.execute("INSERT INTO `all_photo` (`id`) VALUES(?)", (id,))
        cur.execute("UPDATE `all_photo` SET `type` = ?,`id_photo` = ?, date_photo = ? WHERE `id` = ?", (types,id_photo,date_photo,id,))
    elif  res[0][0] == 1:
        cur.execute("UPDATE `all_photo` SET `type` = ?,`id_photo` = ?, date_photo = ? WHERE `id` = ?", (types,id_photo,date_photo,id,))
    return base.commit()

async def add_admin_sql(user_id, Name, Nickname):
    cur.execute("INSERT INTO `admin` (`user_id`, `Name`, `Nickname`) VALUES (?,?,?)", (user_id, Name, Nickname))
    return base.commit()


async def add_group_sql(user_id, group):
    cur.execute("INSERT INTO `groupa` (`user_id`,`groupname`) VALUES (?,?)", (user_id, group))
    return base.commit()


async def group_exists_sql(groupname):
    result = cur.execute("SELECT `id` FROM `groupa` WHERE `groupname` = ?", (groupname,))
    return bool(len(result.fetchall()))

async def clear_sql():
    clears = kb_user_reg.get()
    clears.clear()
    kb_user_reg.set(clears)


async def group_list_sql():
    keys = kb_user_reg.get()
    for i in cur.execute('SELECT `groupname` FROM `groupa`'):
        keys.append(i[0])
    keys.sort()
    kb_user_reg.set(keys)
    return kb_user_reg.get()

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

async def delete_users_sql(user_id):
    cur.execute("DELETE FROM user WHERE user_id = ?", (user_id,))
    return base.commit()


async def delete_admins_sql(user_id):
    cur.execute("DELETE FROM admin WHERE user_id = ?", (user_id,))
    return base.commit()


async def delete_groups_sql(text):
    cur.execute("DELETE FROM groupa WHERE groupname = ?", (text,))
    return base.commit()

async def delete_user_groups_sql(text):
    cur.execute("DELETE FROM user WHERE group_user = ?", (text,))
    return base.commit()

async def delete_calls_sql():
    id = 1
    ress = cur.execute("SELECT `id` FROM all_photo WHERE id = ?", (id,))
    res = ress.fetchall()
    if bool(len(res)) == False or res[0][0] != 1:
        return False
    elif res[0][0] == 1:
        cur.execute("DELETE FROM all_photo WHERE id = ?", (id,))
        base.commit()
        return True
    

async def see_rod_sql(user_id):
    #назва групи користувача
    groups = cur.execute("SELECT `group_user` FROM `user` WHERE `user_id` = ?", (user_id,)).fetchall()
    
    h = groups[0][0]
    
    photo = cur.execute("SELECT photos FROM groupa WHERE groupname = ?",(h,)).fetchall()
    date = cur.execute("SELECT `date` FROM groupa WHERE groupname = ?",(h,)).fetchall()
    try:
        lens = len(photo[0][0])
    except TypeError:
        lens = 1
    if lens <= 5:
        return False
    elif lens >=6:
        datka = date_coupes.get()
        reslt = photka.get()
        reslt = photo[0][0]
        datka = date[0][0]
        date_coupes.set(datka)
        photka.set(reslt)
        return True

async def see_calls_sql():
    id = 1
    ress = cur.execute("SELECT `id` FROM all_photo WHERE id = ?", (id,))
    res = ress.fetchall()
    date = cur.execute("SELECT `date_photo` FROM all_photo WHERE id = ?",(id,)).fetchall()
    if bool(len(res)) == False or res[0][0] != 1:
        return False
    elif  res[0][0] == 1:
        datka = date_calls.get()
        datka = date[0][0]
        date_calls.set(datka)
        resulta = id_photka.get()
        res = cur.execute("SELECT id_photo FROM all_photo WHERE id = ?", (id,)).fetchall()
        resulta = res[0][0]
        id_photka.set(resulta)
        return True

async def count_user_sql():
    reslt = count_us.get()
    counts = cur.execute("SELECT `id` FROM user").fetchall()
    if len(counts) == 0:
        return False
    else:
        reslt = len(counts)
        count_us.set(reslt)
        return True

async def count_group_sql():
    reslt = count_gr.get()
    counts = cur.execute("SELECT `id` FROM groupa").fetchall()
    if len(counts) == 0:
        return False
    else:
        reslt = len(counts)
        count_gr.set(reslt)
        return True

#ONLYSUPERADMIN
list_all_user = ContextVar("list_all_user", default=[])
list_all_groupa = ContextVar("list_all_groupa", default=[])
list_all_admin = ContextVar("list_all_admin", default=[])

async def user_all_sql():
    keys = list_all_user.get()
    keys.clear()
    list_all_user.set(keys)
    result = cur.execute("SELECT * FROM `user`")
    list_r = result.fetchall()
    if len(list_r) == 0:
        return True
    elif len(list_r) > 0:
        for i in cur.execute('SELECT * FROM `user`'):
            keys.append(i)
        reslt = ''
        for i in range(0,len(keys)):
            reslt += str(i+1)+'. '+ str(keys[i]) +'\n'
        list_all_user.set(reslt)
        return False

async def groupa_all_sql():
    keys = list_all_groupa.get()
    keys.clear()
    list_all_groupa.set(keys)
    result = cur.execute("SELECT * FROM `groupa`")
    list_r = result.fetchall()
    if len(list_r) == 0:
        return True
    elif len(list_r) > 0:
        for i in cur.execute('SELECT * FROM `groupa`'):
            keys.append(i)
        reslt = ''
        for i in range(0,len(keys)):
            reslt += str(i+1)+'. '+ str(keys[i]) +'\n'
        list_all_groupa.set(reslt)
        return False

async def admin_all_sql():
    keys = list_all_admin.get()
    keys.clear()
    list_all_admin.set(keys)
    result = cur.execute("SELECT * FROM `admin`")
    list_r = result.fetchall()
    if len(list_r) == 0:
        return True
    elif len(list_r) > 0:
        for i in cur.execute('SELECT * FROM `admin`'):
            keys.append(i)
        reslt = ''
        for i in range(0,len(keys)):
            reslt += str(i+1)+'. '+ str(keys[i]) +'\n'
        list_all_admin.set(reslt)
        return False