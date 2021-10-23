import pickle
import base64
import json
from flask import *
from ruamel import yaml


vulnapp = Flask(__name__)


class User:
    def __init__(self, username, is_admin):
        self.username = username
        self.is_admin = is_admin


@vulnapp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        post_data = request.get_data()
        if post_data:

            # parse user input

            username = ""
            serialization_type = ""

            try:
                parse_post_data = post_data.decode().split("&")
                username = parse_post_data[0].split("=")[1]
                serialization_type = parse_post_data[1].split("=")[1]
            except IndexError:
                return render_template(
                    "index.html",
                    message="Please Enter Your Name and Choose the Serialization Type",
                )

            # create user object
            user = User()
            user.username = username
            user.is_admin = False

            if serialization_type == "binary":

                try:
                    pickle_serialize_user = pickle.dumps(user)

                    userid = {
                        "user_data": base64.b64encode(pickle_serialize_user),
                        "type": "binary",
                    }

                    res = make_response(redirect("/"))
                    res.set_cookie(
                        "userid",
                        base64.b64encode(json.dumps(userid).encode()),
                        60 * 60 * 24,
                    )
                    return res
                except Exception as e:
                    print(e)
                    return (
                        render_template("index.html", message="Internal Servar Error"),
                        500,
                    )

            elif serialization_type == "yaml":
                try:
                    userid = {
                        "user_data": base64.b64encode(yaml.dump(user, Dumper=yaml.Dumper).encode()),
                        "type": "yaml",
                    }

                    res = make_response(redirect("/"))
                    res.set_cookie(
                        "userid",
                        base64.b64encode(json.dumps(userid).encode()),
                        60 * 60 * 24,
                    )
                    return res
                except Exception as e:
                    print(e)
                    return (
                        render_template("index.html", message="Internal Servar Error"),
                        500,
                    )
            else:
                return render_template(
                    "index.html", message="Invalid Serialization Type"
                )

        else:
            return render_template(
                "index.html",
                message="Please Enter Your Name and Choose the Serialization Type",
            )

    elif request.method == "GET":
        if not request.cookies:
            return render_template("index.html")

        elif request.cookies:
            parse_userid_cookie = json.loads(
                base64.b64decode(request.cookies["userid"])
            )

            if parse_userid_cookie["type"] == "binary":

                deserialize_binary_user_cookie = pickle.loads(
                    base64.b64decode(parse_userid_cookie["user_data"])
                )

                if deserialize_binary_user_cookie.is_admin:
                    return render_template(
                        "index.html",
                        message=f"Welcome, {deserialize_binary_user_cookie.username}",
                        admin='admin'
                    )
                else:
                    return render_template(
                        "index.html",
                        message=f"Welcome, {deserialize_binary_user_cookie.username}",
                    )
            elif parse_userid_cookie["type"] == "yaml":
                deserialize_yaml_user_cookie = yaml.load(
                    base64.b64decode(parse_userid_cookie["user_data"]), Loader=yaml.Loader
                )

                if deserialize_yaml_user_cookie.is_admin:
                    return render_template(
                        "index.html",
                        message=f"Welcome, {deserialize_yaml_user_cookie.username}",
                        admin='admin'
                    )
                else:
                    return render_template(
                        "index.html",
                        message=f"Welcome, {deserialize_yaml_user_cookie.username}",
                    )
            else:
                return render_template(
                    "index.html", message=f"Serialization Type is not supported"
                )


@vulnapp.route("/logout")
def logout():
    res = make_response(redirect("/"))
    res.set_cookie("userid", "", 0)
    return res


if __name__ == "__main__":
    vulnapp.run()
