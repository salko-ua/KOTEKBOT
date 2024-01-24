from data_base.create_db import BaseDBPart


class UserDB(BaseDBPart):
    async def check_sum(self):
        result = await (
            await self.cur.execute("SELECT count_interaction  from user")
        ).fetchall()
        sum = 0

        for i in range(len(result[0])):
            print(result[0][i], i)
            sum += result[0][i]
            print(sum)

    # Функція перевірки чи є користувач з данним user_id у db
    # Повертає True or False
    async def user_exists_sql(self, user_id):
        result = await (
            await self.cur.execute(
                "SELECT COUNT(`user_id`) FROM `user` WHERE `user_id` = ?", (user_id,)
            )
        ).fetchall()
        return bool(result[0][0])

    # Переглянути число всіх користувачів
    # Повертає число користувачів int
    async def count_user_sql(self):
        counts = await self.cur.execute("SELECT `user_id` FROM user")
        return len(await counts.fetchall())

    # Функція яка повертає дані за данним user_id у db
    # Повертає True or False
    async def user_show_data_sql(self, user_id):
        result = await self.cur.execute(
            "SELECT * FROM user WHERE user_id = ?", (user_id,)
        )
        return await result.fetchall()

    # Додає користувача до бази даних
    # Повертає збереження бази данних
    async def add_user_sql(
        self,
        user_id,
        first_name,
        last_name,
        username,
        date_join,
        count_message,
        last_message,
        admin,
        student_group,
        teacher_group,
    ):
        await self.cur.execute(
            """INSERT INTO user(
                user_id,    
                first_name,
                last_name,
                username,
                date_join,
                count_interaction,
                last_interaction,
                admin,
                student_group,
                teacher_group) 
            VALUES 
            (?,?,?,?,?,?,?,?,?,?)
            """,
            (
                user_id,
                first_name,
                last_name,
                username,
                date_join,
                count_message,
                last_message,
                admin,
                student_group,
                teacher_group,
            ),
        )
        return await self.base.commit()

    # Оновлює користувача в базі даних
    # Повертає збереження бази данних
    async def update_user_sql(
        self,
        user_id,
        first_name,
        last_name,
        username,
        last_interaction,
        admin,
        student_group,
        teacher_group,
    ):
        count_interaction = await self.cur.execute(
            "SELECT count_interaction FROM user WHERE user_id = ?", (user_id,)
        )
        count_interaction = await count_interaction.fetchall()
        count_interaction: int = count_interaction[0][0]
        count_interaction += 1

        await self.cur.execute(
            """UPDATE user 
            SET     
                first_name = ?,    
                last_name = ?,    
                username = ?,    
                count_interaction = ?,  
                last_interaction = ?,  
                admin = ?,   
                student_group = ?, 
                teacher_group = ? 
            WHERE user_id = ?
            """,
            (
                first_name,
                last_name,
                username,
                count_interaction,
                last_interaction,
                admin,
                student_group,
                teacher_group,
                user_id,
            ),
        )
        return await self.base.commit()
