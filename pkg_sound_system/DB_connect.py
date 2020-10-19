""" connection à la base de données MySQL """

import mysql.connector
import json
import datetime as dt
from passlib.hash import sha256_crypt
from pkg_sound_system.search import search_api


class db_conect:

    mydb = mysql.connector.connect(
        host="localhost",              # host="54.37.8.108",
        user="jonathan",         # user="root",
        passwd="gnipod8*",       # passwd="dopingjo",
        database="soundsystem"   # database="soundsystem"
    )
    mycursor = mydb.cursor(buffered=True)

    @classmethod
    def set_signup(cls, *args):
        """ set signup formular to the database """
        message = ""
        print(f"{args=}")
        sql = "INSERT INTO users "
        sql += "(login, password, firstname, lastname, birth, sex)"
        sql += " VALUES (%s, %s, %s, %s, %s, %s)"
        crypt_arg = sha256_crypt.hash(args[1])
        val = (args[0], crypt_arg, args[2], args[3], args[4], args[5])
        print(f"{val=}")
        try:
            ends_sql = [
                " login='%s'",
                " firstname='%s' and lastname='%s' and birth='%s'"
            ]
            result = []
            for end_sql in ends_sql:
                if end_sql == ends_sql[0]:
                    main_sql = "SELECT login, password FROM users WHERE"
                    main_sql += end_sql
                    cls.mycursor.execute(main_sql % args[0])
                if end_sql == ends_sql[1]:
                    main_sql = "SELECT firstname, lastname, birth "
                    main_sql += "FROM users WHERE"
                    main_sql += end_sql
                    b_date = dt.datetime.strptime(args[4], "%Y-%m-%d")
                    cls.mycursor.execute(main_sql % (args[2], args[3], b_date))
                result.append(cls.mycursor.fetchone())
            print(f"{ends_sql=}")
            print(f"{result=}")
            if result[0] is None and result[1] is None:
                myresult = []
            else:
                myresult = (
                    result[0][0], result[0][1], result[1][0],
                    result[1][1], result[1][2]
                )
            print(f"{myresult=}")
            if not myresult:
                cls.mycursor.execute(sql, val)
                print(f"{cls.mycursor.rowcount=}")
                if cls.mycursor.rowcount > 0:
                    cls.mydb.commit()
                    return True
                else:
                    return False
            else:
                if myresult[0] == args[0]:
                    message += f"Login déjà existant!\n"
                    message += f"si vous en ête le propriétaire, "
                    message += f"connectez-vous.\n"
                if sha256_crypt.verify(args[1], myresult[1]):
                    message += f"Ce mot de passe est déjà pris, "
                    message += f"veuillez en choisir un autre.\n"
                if myresult[2] == args[2] and myresult[3] == args[3] \
                        and str(myresult[4]) == args[4]:
                    message += f"Cet utilisateur existe déjà.\n"
                return message
        except Exception as e:
            print(f"{e=}")
            cls.mydb.rollback()
        # finally:
        #     cls.disconect_db()

    @classmethod
    def login(cls, *args):
        """ verify the logins between the user and database """
        message = ""
        password = bool()
        sql = "SELECT password FROM users WHERE login='%s'"
        try:
            cls.mycursor.execute(sql % args[0])
            myresult = cls.mycursor.fetchone()
            if not myresult:
                message += f"Aucun compte ne correspond."
                message += f"\n\nVérifez vos identifiants.\n"
            else:
                compar = sha256_crypt.verify(args[1], myresult[0])
                if compar:
                    password = True
                else:
                    message += f"Mot de passe érroné!\n"
                    password = False
            return [message, password]
        except Exception as e:
            print(f"db login {e=}")
        # finally:
        #     cls.disconect_db()

    @classmethod
    def get_search(cls, search_elem: str):
        """ search in db if the user demand exist """
        sql = "SELECT * FROM albums WHERE artist=%s OR title_album=%s"
        val = (search_elem, search_elem)
        try:
            cls.mycursor.execute(sql, val)
            myresult = cls.mycursor.fetchall()
            if not myresult:
                sa = search_api()
                sa_album = sa.search_r(search_elem)
                album_resp = cls.set_music(sa_album)
                if type(album_resp) is not bool and not False:
                    cls.mycursor.execute(sql, (album_resp, album_resp))
                    new_result = cls.mycursor.fetchall()
                    print(f"{album_resp}\n{new_result=}")
                    if not new_result:
                        return False
                    else:
                        return new_result
            else:
                return myresult
        except Exception as e:
            print(f"get_search from DB_connect.py {e=}")
        # finally:
        #     pass

    @classmethod
    def set_music(cls, new_album: dict):
        """ set new album in db """
        na = new_album
        sql = "INSERT INTO albums "
        sql += "(image_album, artist, album_tracks, title_album, genre)"
        sql += " VALUES (%s, %s, %s, %s, %s)"
        val = []
        for album in na:
            values = (
                album['image'], album['artist'],
                json.dumps(album['tracklist']),
                album['title'], album['genre'][0]
            )
            val.append(values)
        print(f"{val=}")
        try:
            cls.mycursor.executemany(sql, val)
            print(f"{cls.mycursor.rowcount=}")
            if cls.mycursor.rowcount > 0:
                cls.mydb.commit()
                res = na[0]['artist']
                print(f"{res=}")
                return res
            else:
                return False
        except Exception as e:
            print(f"{e=}")
            cls.mydb.rollback()
        # finally:
        #    cls.disconect_db()

    @classmethod
    def set_selected_album(cls, selected_album: dict) -> int:
        """ set in data base the album you selected """
        return_val = 0
        error = ""
        sql = "SELECT user_id FROM users WHERE login='%s'"
        sql_2 = "SELECT album_id FROM albums "
        sql_2 += "WHERE artist=%s AND title_album=%s"
        sql_3 = "SELECT first_time_selected FROM selected_albums "
        sql_3 += "WHERE users_user_id=%s AND albums_album_id=%s"
        date = dt.datetime.now().strftime("%Y-%m-%d")
        try:
            cls.mycursor.execute(sql % selected_album['user'])
            user_id = cls.mycursor.fetchone()[0]
            print(f"{user_id=}")
            if not user_id:
                error += f"Error: cannot fetch user_id.\n"
            cls.mycursor.execute(sql_2, (
                selected_album['artist'],
                selected_album['title'])
            )
            album_id = cls.mycursor.fetchone()[0]
            print(f"{album_id=}")
            if not album_id:
                error += f"Error: cannot fetch album_id.\n"
            cls.mycursor.execute(sql_3, (user_id, album_id))
            first_time = cls.mycursor.fetchone()
            print(f"{first_time=}")
            if not first_time:
                sql_4 = "INSERT INTO selected_albums "
                sql_4 += "(first_time_selected, how_many_times, "
                sql_4 += "users_user_id, albums_album_id)"
                sql_4 += " VALUES(%s, %s, %s, %s)"
                val = (date, 1, user_id, album_id)
                try:
                    cls.mycursor.execute(sql_4, val)
                    msg = f"db selected_albums INSERT {cls.mycursor.rowcount=}"
                    print(msg)
                    if cls.mycursor.rowcount > 0:
                        return_val = 1
                        cls.mydb.commit()
                except Exception as first_insert:
                    er_salbum = f"db selected_album Error\n\t"
                    er_salbum += f"first INSERT impossible.\n{first_insert=}"
                    print(er_salbum)
                    cls.mydb.rollback()
            else:
                sql_5 = "UPDATE selected_albums SET last_time_selected=%s, "
                sql_5 += "how_many_times=how_many_times+1 "
                sql_5 += "WHERE users_user_id=%s AND albums_album_id=%s"
                val = (date, user_id, album_id)
                try:
                    cls.mycursor.execute(sql_5, val)
                    print(f"db selected_album UPDATE {cls.mycursor.rowcount=}")
                    if cls.mycursor.rowcount > 0:
                        return_val = 1
                        cls.mydb.commit()
                except Exception as update:
                    er_upd_salbum = f"db selected_album Error\n\t"
                    er_upd_salbum += f"UPDATE impossible.\n{update=}"
                    print(er_upd_salbum)
                    cls.mydb.rollback()
            return return_val
        except Exception as e:
            print(f"db selected_album {e=}")
            print(f"{error=}")

    @classmethod
    def get_playlist(cls, playlist_elem: int) -> list:
        """ get a tuple from 'set_playlist' function to fetch a playlist """
        error = ""
        init_sql = "SELECT playlist_name, playlist_id FROM playlist WHERE users_user_id=%s"
        sql_2 = "SELECT track_name, selected_albums_selected_album_id FROM track_listened WHERE playlist_playlist_id=%s"
        sql_3 = "SELECT albums_album_id FROM selected_albums WHERE selected_album_id=%s"
        sql_4 = "SELECT image_album, artist, album_tracks, title_album, genre "
        sql_4 += "FROM albums WHERE album_id=%s"
        try:
            cls.mycursor.execute(init_sql % playlist_elem)
            playlist_idName = cls.mycursor.fetchall()
            print(f"{playlist_idName=}")
            if not playlist_idName:
                error += f"Error: cannot fetch playlist_idName for playlist.\n"
            cls.mycursor.execute(sql_2 % playlist_idName[0][1])
            track_elem = cls.mycursor.fetchall()
            print(f"{track_elem=}")
            if not track_elem:
                error += f"Error: cannot fetch track_elem for playlist.\n"
            for name_album_id in track_elem:
                print(f"{name_album_id=}")
                cls.mycursor.execute(sql_3 % name_album_id[1])
                album_id = cls.mycursor.fetchone()[0]
                print(f"{album_id=}")
                if not album_id:
                    error += f"Error: cannot fetch album_id for playlist.\n"
            cls.mycursor.execute(sql_4 % album_id)
            album_elem = cls.mycursor.fetchall()[0]
            print(f"{album_elem=}")
            new_playlist_elem = []
            for elem in album_elem:
                elem = json.loads(elem)
                if type(elem) == list:
                    for track in elem:
                        if track['title'] == name_album_id[0]:
                            new_playlist_elem.append(track)
                else:
                    new_playlist_elem.append(elem)
            print(f"{new_playlist_elem=}")
            # cls.mycursor.execute(init_sql % album_id )
            # = cls.mycursor.fetchall()
            # print(f"{playlist_idName=}")
            # if not playlist_idName:
            #     error += f"Error: cannot fetch playlist_idName for playlist.\n"
        except Exception as get_d:
            print(f"{get_d=}")

    @classmethod
    def set_playlist(cls, new_playlist: list):
        """ set new playlist by joining SQL tables """
        error = ""
        sql = "SELECT user_id FROM users WHERE login='%s'"
        np = new_playlist
        try:
            cls.mycursor.execute(sql % np[len(np)-1]['user'])
            user_id = cls.mycursor.fetchone()[0]
            print(f"{user_id=}")
            if not user_id:
                error += f"Error: cannot fetch user_id.\n"
            sql_2 = "INSERT INTO playlist (playlist_name, users_user_id)"
            sql_2 += " VALUES(%s, %s)"
            val_2 = (np[0]['playlist_name'], user_id)
            print(f"{val_2=}")
            cls.mycursor.execute(sql_2, val_2)
            print(f"{cls.mycursor.rowcount=}")
            if cls.mycursor.rowcount > 0:
                sql_3 = "SELECT playlist_id FROM playlist "
                sql_3 += "WHERE users_user_id='%s'"
                cls.mycursor.execute(sql_3 % user_id)
                playlist_id = cls.mycursor.fetchone()[0]
                print(f"{playlist_id=}")
            else:
                error += "Error: cannot insert playlist_name and user_id.\n"
            np.remove(np[0])
            np.remove(np[-1])
            init_sql = "SELECT album_id FROM albums "
            init_sql += "WHERE title_album=%s AND artist=%s"
            init_sql_2 = "SELECT selected_album_id FROM selected_albums "
            init_sql_2 += "WHERE albums_album_id='%s'"
            init_sql_3 = "INSERT INTO track_listened (track_name, "
            init_sql_3 += "track_listened_to_end, track_listened_x_times, "
            init_sql_3 += "selected_albums_selected_album_id, "
            init_sql_3 += "playlist_playlist_id, track_data)"
            init_sql_3 += " VALUES(%s, %s, %s, %s, %s, %s)"
            print(f"{init_sql_3=}")
            for data_track in np:
                init_val = (
                    data_track['album_title'],
                    data_track['album_artist']
                )
                print(f"{init_val=}")
                cls.mycursor.execute(init_sql, init_val)
                album_id = cls.mycursor.fetchone()[0]
                print(f"{album_id=}")
                if not album_id:
                    error += f"Error: cannot fetch album_id.\n"
                cls.mycursor.execute(init_sql_2 % album_id)
                selected_album_id = cls.mycursor.fetchone()[0]
                print(f"{selected_album_id=}")
                if not selected_album_id:
                    error += f"Error: cannot fetch selected_album_id.\n"
                init_val_3 = (
                    data_track['album_track'], 'no', 1,
                    selected_album_id, playlist_id, data_track['album_data']
                )
                print(f"{init_val_3=}")
                try:
                    cls.mycursor.execute(init_sql_3, init_val_3)
                    print(f"{cls.mycursor.rowcount=}")
                    if cls.mycursor.rowcount > 0:
                        cls.mydb.commit()
                        cls.get_playlist(user_id)
                except Exception as uninsert:
                    print(f"{uninsert=}")
        except Exception as e:
            print(f"db set_playlist {e=}")
            print(f"{error=}")
            cls.mydb.rollback()

    @classmethod
    def disconect_db(cls):
        """ disconnection with database """
        if (cls.mydb.is_connected()):
            cls.mycursor.close()
            cls.mydb.close()


if __name__ == '__main__':
    print('db conexion.py')
    inst = db_conect()
    db = inst
