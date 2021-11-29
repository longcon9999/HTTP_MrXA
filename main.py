from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)


def time_vector(p, c, m):
    result = {}
    connection = {}
    try:
        for i in range(len(p)):
            result[i + 1] = [[int(tmp.strip()) for tmp in p[i].split(",")]]
        print(result)
        for i in c:
            tmp = i.split("-")
            connection[",".join([x.strip() for x in tmp[1].split(",")])] = ",".join([x.strip() for x in tmp[0].split(",")])
        print(connection)
        for i in range(1, m + 1):
            for j in range(1, len(p) + 1):
                tmp = result.get(j)
                if tmp is None:
                    tmp = [[0, 0, 0]]
                pre_tmp = tmp[i - 1]
                after_tmp = []
                for _i in range(len(pre_tmp)):
                    if _i == j - 1:
                        after_tmp.append(pre_tmp[_i] + 1)
                    else:
                        after_tmp.append(pre_tmp[_i])
                if connection.get(f"{j},{i}") is not None:
                    compare_item = str(connection.get(f"{j},{i}"))
                    compare_vector = result.get(int(compare_item.split(",")[0]))[int(compare_item.split(",")[1])]
                    for _i in range(len(after_tmp)):
                        if after_tmp[_i] < compare_vector[_i]:
                            after_tmp[_i] = compare_vector[_i]
                tmp.append(after_tmp)
                result[j] = tmp
        for k, v in result.items():
            print(k)
            print(v)
        return result, True
    except Exception as e:
        return e, False


def phys_time_sys(client_send, server_received, server_send, client_received):
    client_send_time = datetime.strptime(client_send, "%Y-%m-%d %H:%M:%S.%f")
    server_received_time = datetime.strptime(server_received, "%Y-%m-%d %H:%M:%S.%f")
    server_send_time = datetime.strptime(server_send, "%Y-%m-%d %H:%M:%S.%f")
    client_received_time = datetime.strptime(client_received, "%Y-%m-%d %H:%M:%S.%f")
    result = ((server_received_time - client_send_time) + (server_send_time - client_received_time))/2
    return str(client_received_time + result)[:-3]


def berkeley_gt(server, client_1, client_2):
    server_time = datetime.strptime(server, "%Y-%m-%d %H:%M:%S.%f")
    client_1_time = datetime.strptime(client_1, "%Y-%m-%d %H:%M:%S.%f")
    client_2_time = datetime.strptime(client_2, "%Y-%m-%d %H:%M:%S.%f")
    print(server_time)
    print(client_1_time)
    print(client_2_time)
    offset = ((client_1_time - server_time) + (client_2_time - server_time))/3
    client_1_offset = offset - (client_1_time - server_time)
    client_2_offset = offset - (client_2_time - server_time)
    print()
    print()
    print(round(client_2_offset.total_seconds()*1000, 0))
    server_update = str(server_time + offset)
    client_1_update = str(client_1_time + client_1_offset)
    client_2_update = str(client_2_time + client_2_offset)
    print(server_update)
    print(client_2_update)
    print(client_1_update)
    result = {"Điều phối": round(offset.total_seconds()*1000, 0),
              "Khách 1": round(client_1_offset.total_seconds()*1000, 0),
              "Khách 2": round(client_2_offset.total_seconds()*1000, 0)}
    
    return


@app.route('/', methods=["GET"])
def index():
    return render_template("homepage.html")


@app.route('/vector_time', methods=["POST", "GET"])
def vector_time():
    if request.method == "POST":
        try:
            num_process = int(request.form.get("num_process"))
            num_message = int(request.form.get("num_message"))
            num_event = int(request.form.get("num_events"))
            p = []
            m = []
            for i in range(num_process):
                p.append(request.form.get(f"process{i}"))
            for i in range(num_message):
                m.append(request.form.get(f"mess{i}"))
            result, ok = time_vector(p, m, num_event)
            if ok:
                return render_template("result_page.html", result=result)
            else:
                return render_template("vector_time.html", Error=result)
        except Exception as e:
            print(e)
            return render_template("vector_time.html", Error=e)
    return render_template("vector_time.html")


@app.route("/sys_physic_time", methods=["POST", "GET"])
def sys_physic_time():
    if request.method == "POST":
        try:
            time_send_client = request.form.get("time_send_client").strip()
            time_received_client = request.form.get("time_received_client").strip()
            time_send_server = request.form.get("time_send_server").strip()
            time_received_server = request.form.get("time_received_server").strip()
            result = phys_time_sys(time_send_client, time_received_server, time_send_server, time_received_client)
            return render_template("sys_physic_time.html", result=result)
        except Exception as e:
            print(e)
            return render_template("sys_physic_time.html", Error=e)
    return render_template("sys_physic_time.html")


@app.route("/berkeley", methods=["POST", "GET"])
def berkeley():
    if request.method == "POST":
        try:
            server_time = request.form.get("time_server").strip()
            client_1_time = request.form.get("client_1").strip()
            client_2_time = request.form.get("client_2").strip()
            result = berkeley_gt(server_time, client_1_time, client_2_time)
            return render_template("berkeley.html", result=result)
        except Exception as e:
            print(e)
            return render_template("berkeley.html", Error=e)
    return render_template("berkeley.html")


if __name__ == "__main__":
    app.run(debug=True)