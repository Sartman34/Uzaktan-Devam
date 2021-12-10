# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python38_app]
from flask import Flask
from google.cloud import datastore
import os
import random, string

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

messages = {
    "basic_error" : "Bir hata oluştu. Kod: {}",
    "bad_login" : "Hatalı Kullanıcı Adı veya Şifre.",
    "wrong_panel" : "Kullanıcı ile yanlış panele giriş yapıldı.",
    "bad_classroom" : "Böyle bir sınıf bulunmamakta.",
    "bad_user" : "Böyle bir kullanıcı bulunmamakta."
    }

split_char = "~"

#U06
bucket_name = os.environ.get("THE_BUCKET")
datastore_client = datastore.Client()

def prepare_message(*messages):
    response = ""
    for message in messages:
        response = response + str(message) + split_char
    return response[:-1]

def get_random_string(length):
    random_list = []
    for i in range(length):
        random_list.append(random.choice(string.ascii_uppercase + string.digits))
    return ''.join(random_list)

class User():
    raw_data_keys = {
        "password" : 0,
        "is_admin" : 1,
        "validations" : 2,
        "teacher" : 3,
        "classroom_ids" : 4,
        "attandee_sheet_info_dict_id" : 5,
        "class_names" : 6
        }
    validation_keys = {
        "teacher" : 0,
        "classroom_ids" : 1,
        "attandee_sheet_info_dict" : 2,
        "class_names" : 3
        }
    validation_keys_admin = {
        "user_infos" : 0,
        "classrooms" : 1,
        "teacher" : 2,
        "messages" : 3
        }
    
    def __init__(self):
        self.attandee_sheet_info_elements = dict()

    def get_user_info(self):
        user_info = ""
        user_info = self.entity.key.id_or_name + "%"
        user_info += ("1" if self.is_admin else "0") + "%"
        user_info += self.teacher + "%"
        if not self.is_admin:
            user_info += "-".join(self.classroom_ids) + "%"
            user_info += self.class_names
        else:
            user_info = user_info[:-1]
        return user_info
        
    def decode_entity(self, entity):
        self.entity = entity
        try:
            raw_data = self.entity["data"].split("%")
        except TypeError:
            return True
        self.password = raw_data[User.raw_data_keys["password"]]
        self.is_admin = bool(int(raw_data[User.raw_data_keys["is_admin"]]))
        self.validations = raw_data[User.raw_data_keys["validations"]].split("-")
        self.teacher = raw_data[User.raw_data_keys["teacher"]]
        if not self.is_admin:
            self.classroom_ids = raw_data[User.raw_data_keys["classroom_ids"]].split("-")
            self.attandee_sheet_info_dict_id = raw_data[User.raw_data_keys["attandee_sheet_info_dict_id"]]
            self.class_names = raw_data[User.raw_data_keys["class_names"]]

    def encode_entity(self):
        raw_data = self.password + "%"
        raw_data += ("1" if self.is_admin else "0") + "%"
        raw_data += "-".join(self.validations) + "%"
        raw_data += self.teacher + "%"
        if not self.is_admin:
            raw_data += "-".join(self.classroom_ids) + "%"
            raw_data += self.attandee_sheet_info_dict_id + "%"
            raw_data += self.class_names
        self.entity["data"] = raw_data
        return self.entity
        
    def decode_attandee_sheet_info_dict_entity(self, entity):
        self.attandee_sheet_info_dict_entity = entity
        raw_attandee_sheet_info_elements = self.attandee_sheet_info_dict_entity["attandee_sheet_info_elements"].split("%")
        if not raw_attandee_sheet_info_elements[0]:
            return
        for raw_attandee_sheet_info_element in raw_attandee_sheet_info_elements:
            raw_attandee_sheet_info_element = raw_attandee_sheet_info_element.split("?")
            date = raw_attandee_sheet_info_element.pop(0)
            raw_attandee_sheet_infos = raw_attandee_sheet_info_element.pop(0).split("&")
            self.attandee_sheet_info_elements[date] = [raw_attandee_sheet_info.split("-") for raw_attandee_sheet_info in raw_attandee_sheet_infos]
        
    def encode_attandee_sheet_info_dict_entity(self):
        raw_attandee_sheet_info_elements = ""
        for date in self.attandee_sheet_info_elements.keys():
            attandee_sheet_infos = self.attandee_sheet_info_elements[date]
            if not len(attandee_sheet_infos):
                continue
            raw_attandee_sheet_info_elements += date + "?"
            for attandee_sheet_info in attandee_sheet_infos:
                raw_attandee_sheet_info_elements += "-".join(attandee_sheet_info) + "&"
            raw_attandee_sheet_info_elements = raw_attandee_sheet_info_elements[:-1] + "%"
        raw_attandee_sheet_info_elements = raw_attandee_sheet_info_elements[:-1]
        
        self.attandee_sheet_info_dict_entity["attandee_sheet_info_elements"] = raw_attandee_sheet_info_elements
        return self.attandee_sheet_info_dict_entity

    def encode_classroom_ids(self):
        return "-".join(self.classroom_ids)

class Classroom():
    raw_data_keys = {
        "year" : 0,
        "name" : 1,
        "students" : 2
        }
    def decode_entity(self, entity):
        self.entity = entity
        try:
            raw_data = self.entity["data"].split("%")
        except TypeError:
            return True
        self.year = raw_data[Classroom.raw_data_keys["year"]]
        self.name = raw_data[Classroom.raw_data_keys["name"]]
        self.students = raw_data[Classroom.raw_data_keys["students"]]
##        str(classroom_entity.id) + "%" + classroom_entity["data"] + "%"

    def encode_entity(self):
        raw_data = self.year + "%"
        raw_data += self.name + "%"
        raw_data += self.students
        self.entity["data"] = raw_data
        return self.entity
        
@app.route('/command/<command>')
def main_request_handler(command):
    command = command.split(split_char)
    try:
        action = command[0]
        parameters = command[1:]
    except:
        return prepare_message("message", messages["basic_error"].format("U 00"))
    if action == "login":
        try:
            username = parameters[0]
            password = parameters[1]
            validations = parameters[2].split("-")
        except:
            return prepare_message("message", messages["basic_error"].format("U 01"))
        key = datastore_client.key("User", username)
        user_entity = datastore_client.get(key)
        user = User()
        if user.decode_entity(user_entity):
            return prepare_message("message", messages["bad_login"])

        if user.is_admin:
            return prepare_message("message", messages["wrong_panel"])
        
        if password == user.password:
            message = ["success"]
            if not validations[User.validation_keys["teacher"]] == user.validations[User.validation_keys["teacher"]]:
                message.append("update_teacher")
                message.append(user.teacher)
                message.append(user.validations[User.validation_keys["teacher"]])
                
            if not validations[User.validation_keys["classroom_ids"]] == user.validations[User.validation_keys["classroom_ids"]]:
                message.append("update_classroom_ids")
                message.append(user.encode_classroom_ids())
                message.append(user.validations[User.validation_keys["classroom_ids"]])
                raw_classrooms = ""
                for classroom_id in user.classroom_ids:
                    key = datastore_client.key("Classroom", int(classroom_id))
                    classroom_entity = datastore_client.get(key)
                    classroom = Classroom()
                    if classroom.decode_entity(classroom_entity):
                        continue
                    raw_classrooms += classroom_id + "%" + classroom_entity["data"] + "%"
                raw_classrooms = raw_classrooms[:-1]
                message.append(raw_classrooms)
                
            if not validations[User.validation_keys["attandee_sheet_info_dict"]] == user.validations[User.validation_keys["attandee_sheet_info_dict"]]:
                message.append("update_attandee_sheet_info_dict")
                key = datastore_client.key("Attandee Sheet Info Dict", int(user.attandee_sheet_info_dict_id))
                attandee_sheet_info_dict_entity = datastore_client.get(key)
                raw_attandee_sheet_info_dict = attandee_sheet_info_dict_entity["attandee_sheet_info_elements"]
                message.append(raw_attandee_sheet_info_dict)
                message.append(user.validations[User.validation_keys["attandee_sheet_info_dict"]])
                
            if not validations[User.validation_keys["class_names"]] == user.validations[User.validation_keys["class_names"]]:
                message.append("update_class_names")
                message.append(user.class_names)
                message.append(user.validations[User.validation_keys["class_names"]])
                
            return prepare_message(*message)
        else:
            return prepare_message("message", messages["bad_login"])

        
    if action == "login_admin":
        try:
            username = parameters[0]
            password = parameters[1]
            validations = parameters[2].split("-")
        except:
            return prepare_message("message", messages["basic_error"].format("U 01"))
        key = datastore_client.key("User", username)
        user_entity = datastore_client.get(key)
        user = User()
        if user.decode_entity(user_entity):
            return prepare_message("message", messages["bad_login"])
        
        if not user.is_admin:
            return prepare_message("message", messages["wrong_panel"])
        
        if password == user.password:
            message = ["success"]
            if not validations[User.validation_keys_admin["teacher"]] == user.validations[User.validation_keys_admin["teacher"]]:
                message.append("update_teacher")
                message.append(user.teacher)
                message.append(user.validations[User.validation_keys_admin["teacher"]])
                
            if not validations[User.validation_keys_admin["classrooms"]] == user.validations[User.validation_keys_admin["classrooms"]]:
                message.append("update_classrooms")
                message.append(user.validations[User.validation_keys_admin["classrooms"]])
                query = datastore_client.query(kind = "Classroom")
                classroom_entities = list(query.fetch())
                raw_classrooms = ""
                for classroom_entity in classroom_entities:
                    
                    raw_classrooms += str(classroom_entity.id) + "%" + classroom_entity["data"] + "%"
                raw_classrooms = raw_classrooms[:-1]
                message.append(raw_classrooms)

            if not validations[User.validation_keys_admin["messages"]] == user.validations[User.validation_keys_admin["messages"]]:
                message.append("update_messages")
                message.append(user.validations[User.validation_keys_admin["messages"]])
                query = datastore_client.query(kind = "Message")
                message_entities = list(query.fetch())
                raw_messages = ""
                for message_entity in message_entities:
                    raw_messages += message_entity["data"] + "&"
                raw_messages = raw_messages[:-1]
                message.append(raw_messages)

            if not validations[User.validation_keys_admin["user_infos"]] == user.validations[User.validation_keys_admin["user_infos"]]:
                message.append("update_user_infos")
                message.append(user.validations[User.validation_keys_admin["user_infos"]])
                query = datastore_client.query(kind = "User")
                user_entities = list(query.fetch())
                raw_user_infos = ""
                for user_entity in user_entities:
                    queried_user = User()
                    queried_user.decode_entity(user_entity)
                    raw_user_infos += queried_user.get_user_info() + "%"
                raw_user_infos = raw_user_infos[:-1]
                message.append(raw_user_infos)
                
            return prepare_message(*message)
        else:
            return prepare_message("message", messages["bad_login"])

        
    elif action == "send_attandee_sheet":
        try:
            username = parameters[0]
            password = parameters[1]
            date = parameters[2]
            classroom_id = parameters[3]
            data = parameters[4]
        except:
            return prepare_message("message", messages["basic_error"].format("U 03"))
        key = datastore_client.key("User", username)
        user_entity = datastore_client.get(key)
        user = User()
        if user.decode_entity(user_entity):
            return prepare_message("message", messages["bad_login"])
        
        if password == user.password:
            key = datastore_client.key('Attandee Sheet')
            attandee_sheet = datastore.Entity(key)
            attandee_sheet.update({"username": username, "date": date, "classroom_id": classroom_id, "data": data})
            datastore_client.put(attandee_sheet)

            with datastore_client.transaction():
                key = datastore_client.key("Attandee Sheet Info Dict", int(user.attandee_sheet_info_dict_id))
                attandee_sheet_info_dict_entity = datastore_client.get(key)
                user.decode_attandee_sheet_info_dict_entity(attandee_sheet_info_dict_entity)
            
                try:
                    user.attandee_sheet_info_elements[attandee_sheet["date"]].append([str(attandee_sheet.id), "1"])
                except KeyError:
                    user.attandee_sheet_info_elements[attandee_sheet["date"]] = [[str(attandee_sheet.id), "1"]]

                entity = user.encode_attandee_sheet_info_dict_entity()
                datastore_client.put(entity)
            
            attandee_sheet_info_dict_validation = str(int(user.validations[User.validation_keys["attandee_sheet_info_dict"]]) + 1)
            user.validations[User.validation_keys["attandee_sheet_info_dict"]] = attandee_sheet_info_dict_validation

            entity = user.encode_entity()
            datastore_client.put(entity)
            return prepare_message("success", attandee_sheet.id, attandee_sheet_info_dict_validation)
        else:
            return prepare_message("message", messages["bad_login"])


    elif action == "replace_attandee_sheet":
        try:
            username = parameters[0]
            password = parameters[1]
            date = parameters[2]
            classroom_id = parameters[3]
            data = parameters[4]
            attandee_sheet_id = parameters[5]
        except:
            return prepare_message("message", messages["basic_error"].format("U 03"))
        key = datastore_client.key("User", username)
        user_entity = datastore_client.get(key)
        user = User()
        if user.decode_entity(user_entity):
            return prepare_message("message", messages["bad_login"])
        
        if password == user.password:
            key = datastore_client.key('Attandee Sheet', int(attandee_sheet_id))
            attandee_sheet = datastore.Entity(key)
            attandee_sheet.update({"username": username, "date": date, "classroom_id": classroom_id, "data": data})
            datastore_client.put(attandee_sheet)

            with datastore_client.transaction():
                key = datastore_client.key("Attandee Sheet Info Dict", int(user.attandee_sheet_info_dict_id))
                attandee_sheet_info_dict_entity = datastore_client.get(key)
                user.decode_attandee_sheet_info_dict_entity(attandee_sheet_info_dict_entity)
            
                for attandee_sheet_info_element in user.attandee_sheet_info_elements[attandee_sheet["date"]]:
                    if attandee_sheet_info_element[0] == attandee_sheet_id:
                        sync = str(int(attandee_sheet_info_element[1]) + 1)
                        attandee_sheet_info_element = [attandee_sheet_info_element[0], sync]
                        break

                entity = user.encode_attandee_sheet_info_dict_entity()
                datastore_client.put(entity)
            
            attandee_sheet_info_dict_validation = str(int(user.validations[User.validation_keys["attandee_sheet_info_dict"]]) + 1)
            user.validations[User.validation_keys["attandee_sheet_info_dict"]] = attandee_sheet_info_dict_validation

            entity = user.encode_entity()
            datastore_client.put(entity)
            return prepare_message("success", sync, attandee_sheet_info_dict_validation)
        else:
            return prepare_message("message", messages["bad_login"])

    elif action == "delete_attandee_sheet":
        try:
            username = parameters[0]
            password = parameters[1]
            attandee_sheet_id = parameters[2]
        except:
            return prepare_message("message", messages["basic_error"].format("U 03"))
        key = datastore_client.key("User", username)
        user_entity = datastore_client.get(key)
        user = User()
        if user.decode_entity(user_entity):
            return prepare_message("message", messages["bad_login"])
        
        if password == user.password:
            attandee_sheet_key = datastore_client.key('Attandee Sheet', int(attandee_sheet_id))
            attandee_sheet_entity = datastore_client.get(attandee_sheet_key)

            key = datastore_client.key("User", attandee_sheet_entity["username"])
            user_entity = datastore_client.get(key)
            attandee_sheet_user = User()
            if not attandee_sheet_user.decode_entity(user_entity):
                with datastore_client.transaction():
                    key = datastore_client.key("Attandee Sheet Info Dict", int(attandee_sheet_user.attandee_sheet_info_dict_id))
                    attandee_sheet_info_dict_entity = datastore_client.get(key)
                    attandee_sheet_user.decode_attandee_sheet_info_dict_entity(attandee_sheet_info_dict_entity)
                
                    for ind in range(len(attandee_sheet_user.attandee_sheet_info_elements[attandee_sheet_entity["date"]])):
                        attandee_sheet_info_element = attandee_sheet_user.attandee_sheet_info_elements[attandee_sheet_entity["date"]][ind]
                        if attandee_sheet_info_element[0] == attandee_sheet_id:
                            attandee_sheet_user.attandee_sheet_info_elements[attandee_sheet_entity["date"]].pop(ind)
                            break

                    entity = attandee_sheet_user.encode_attandee_sheet_info_dict_entity()
                    datastore_client.put(entity)
            
                attandee_sheet_info_dict_validation = str(int(attandee_sheet_user.validations[User.validation_keys["attandee_sheet_info_dict"]]) + 1)
                attandee_sheet_user.validations[User.validation_keys["attandee_sheet_info_dict"]] = attandee_sheet_info_dict_validation
                
                entity = attandee_sheet_user.encode_entity()
                datastore_client.put(entity)
                
            datastore_client.delete(attandee_sheet_key)
            return prepare_message("success", attandee_sheet_info_dict_validation)
        else:
            return prepare_message("message", messages["bad_login"])

        
    elif action == "get_attandee_sheets":
        try:
            username = parameters[0]
            password = parameters[1]
            raw_attandee_sheet_ids = parameters[2]
        except:
            return prepare_message("message", messages["basic_error"].format("U 04"))
        
        key = datastore_client.key("User", username)
        user_entity = datastore_client.get(key)
        user = User()
        if user.decode_entity(user_entity):
            return prepare_message("message", messages["bad_login"])
        
        if password == user.password:
            message = ["success"]
            try:
                keys =[datastore_client.key("Attandee Sheet", int(attandee_sheet_id)) for attandee_sheet_id in raw_attandee_sheet_ids.split("-")]
            except:
                prepare_message("message", messages["basic_error"].format("U 05"))
            attandee_sheet_entities = datastore_client.get_multi(keys)
            for attandee_sheet_entity in attandee_sheet_entities:
                message.append("attandee_sheet")
                message.append(str(attandee_sheet_entity.id))
                message.append(attandee_sheet_entity["username"])
                message.append(attandee_sheet_entity["date"])
                message.append(attandee_sheet_entity["classroom_id"])
                message.append(attandee_sheet_entity["data"])
            return prepare_message(*message)
        else:
            return prepare_message("message", messages["bad_login"])


    elif action == "query_attandee_sheets":
        try:
            username = parameters[0]
            password = parameters[1]
            date = parameters[2]
            classroom_id = parameters[3]
            teacher_username = parameters[4]
        except:
            return prepare_message("message", messages["basic_error"].format("U 04"))
        
        key = datastore_client.key("User", username)
        user_entity = datastore_client.get(key)
        user = User()
        if user.decode_entity(user_entity):
            return prepare_message("message", messages["bad_login"])
        
        if password == user.password:
            query = datastore_client.query(kind = "Attandee Sheet")
            if teacher_username:
                query.add_filter("username", "=", teacher_username)
            if date:
                query.add_filter("date", "=", date)
            if classroom_id:
                query.add_filter("classroom_id", "=", classroom_id)
            attandee_sheet_entities = list(query.fetch())
            message = []
            for attandee_sheet_entity in attandee_sheet_entities:
                message.append("attandee_sheet")
                message.append(str(attandee_sheet_entity.id))
                message.append(attandee_sheet_entity["username"])
                message.append(attandee_sheet_entity["date"])
                message.append(attandee_sheet_entity["classroom_id"])
                message.append(attandee_sheet_entity["data"])
            return prepare_message(*message)
        else:
            return prepare_message("message", messages["bad_login"])

    elif action == "change_classroom_name":
        try:
            username = parameters[0]
            password = parameters[1]
            classroom_id = parameters[2]
            year = parameters[3]
            name = parameters[4]
        except:
            return prepare_message("message", messages["basic_error"].format("U 04"))
        
        key = datastore_client.key("User", username)
        user_entity = datastore_client.get(key)
        user = User()
        if user.decode_entity(user_entity):
            return prepare_message("message", messages["bad_login"])

        if not user.is_admin:
            return prepare_message("message", messages["wrong_panel"])
        
        if password == user.password:
            message = ["success"]
            key = datastore_client.key("Classroom", int(classroom_id))
            classroom_entity = datastore_client.get(key)
            classroom = Classroom()
            if classroom.decode_entity(classroom_entity):
                return prepare_message("message", messages["bad_classroom"])
            classroom.year = year
            classroom.name = name
            entity = classroom.encode_entity()
            datastore_client.put(entity)
            return prepare_message(*message)
        else:
            return prepare_message("message", messages["bad_login"])

    elif action == "change_classroom_students":
        try:
            username = parameters[0]
            password = parameters[1]
            classroom_id = parameters[2]
            students = parameters[3]
        except:
            return prepare_message("message", messages["basic_error"].format("U 04"))
        
        key = datastore_client.key("User", username)
        user_entity = datastore_client.get(key)
        user = User()
        if user.decode_entity(user_entity):
            return prepare_message("message", messages["bad_login"])

        if not user.is_admin:
            return prepare_message("message", messages["wrong_panel"])
        
        if password == user.password:
            message = ["success"]
            key = datastore_client.key("Classroom", int(classroom_id))
            classroom_entity = datastore_client.get(key)
            classroom = Classroom()
            if classroom.decode_entity(classroom_entity):
                return prepare_message("message", messages["bad_classroom"])
            classroom.students = students
            entity = classroom.encode_entity()
            datastore_client.put(entity)
            return prepare_message(*message)
        else:
            return prepare_message("message", messages["bad_login"])

    elif action == "change_password":
        try:
            username = parameters[0]
            password = parameters[1]
            new_password = parameters[2]
        except:
            return prepare_message("message", messages["basic_error"].format("U 04"))
        
        key = datastore_client.key("User", username)
        user_entity = datastore_client.get(key)
        user = User()
        if user.decode_entity(user_entity):
            return prepare_message("message", messages["bad_login"])
        
        if password == user.password:
            message = ["success"]
            user.password = new_password
            entity = user.encode_entity()
            datastore_client.put(entity)
            return prepare_message(*message)
        else:
            return prepare_message("message", messages["bad_login"])

    elif action == "send_message":
        try:
            username = parameters[0]
            password = parameters[1]
            data = parameters[2]
        except:
            return prepare_message("message", messages["basic_error"].format("U 04"))
        
        key = datastore_client.key("User", username)
        user_entity = datastore_client.get(key)
        user = User()
        if user.decode_entity(user_entity):
            return prepare_message("message", messages["bad_login"])
        
        if password == user.password:
            message = ["success"]
            key = datastore_client.key('Message')
            message_entity = datastore.Entity(key)
            message_entity.update({"data": data})
            datastore_client.put(message_entity)
            return prepare_message(*message)
        else:
            return prepare_message("message", messages["bad_login"])

    elif action == "reset_password":
        try:
            username = parameters[0]
            password = parameters[1]
            changed_username = parameters[2]
        except:
            return prepare_message("message", messages["basic_error"].format("U 04"))
        
        key = datastore_client.key("User", username)
        user_entity = datastore_client.get(key)
        user = User()
        if user.decode_entity(user_entity):
            return prepare_message("message", messages["bad_login"])

        if not user.is_admin:
            return prepare_message("message", messages["wrong_panel"])
        
        if password == user.password:
            message = ["success"]
            key = datastore_client.key("User", changed_username)
            user_entity = datastore_client.get(key)
            changed_user = User()
            if changed_user.decode_entity(user_entity):
                return prepare_message("message", messages["bad_user"])
            changed_user.password = get_random_string(6)
            message.append(changed_user.password)
            entity = changed_user.encode_entity()
            datastore_client.put(entity)
            return prepare_message(*message)
        else:
            return prepare_message("message", messages["bad_login"])

    elif action == "change_teacher":
        try:
            username = parameters[0]
            password = parameters[1]
            changed_username = parameters[2]
            teacher = parameters[3]
        except:
            return prepare_message("message", messages["basic_error"].format("U 04"))
        
        key = datastore_client.key("User", username)
        user_entity = datastore_client.get(key)
        user = User()
        if user.decode_entity(user_entity):
            return prepare_message("message", messages["bad_login"])
        
        if password == user.password:
            message = ["success"]
            key = datastore_client.key("User", changed_username)
            user_entity = datastore_client.get(key)
            changed_user = User()
            if changed_user.decode_entity(user_entity):
                return prepare_message("message", messages["bad_user"])
            changed_user.teacher = teacher
            entity = changed_user.encode_entity()
            datastore_client.put(entity)
            return prepare_message(*message)
        else:
            return prepare_message("message", messages["bad_login"])

    elif action == "set_classrooms":
        try:
            username = parameters[0]
            password = parameters[1]
            changed_username = parameters[2]
            classroom_ids = parameters[3].split("-")
        except:
            return prepare_message("message", messages["basic_error"].format("U 04"))
        
        key = datastore_client.key("User", username)
        user_entity = datastore_client.get(key)
        user = User()
        if user.decode_entity(user_entity):
            return prepare_message("message", messages["bad_login"])
        
        if password == user.password:
            message = ["success"]
            key = datastore_client.key("User", changed_username)
            user_entity = datastore_client.get(key)
            changed_user = User()
            if changed_user.decode_entity(user_entity):
                return prepare_message("message", messages["bad_user"])
            changed_user.classroom_ids = classroom_ids
            entity = changed_user.encode_entity()
            datastore_client.put(entity)
            return prepare_message(*message)
        else:
            return prepare_message("message", messages["bad_login"])

    return prepare_message("message", messages["basic_error"].format("U 02"))

@app.route('/')
def help():
    return "Hi"

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=False)
# [END gae_python38_app]
