from flask import Flask, jsonify, request
import redis

app = Flask(__name__)
r = redis.Redis(host="redis-12764.skr.demo.redislabs.com", port=12764)

@app.route('/getMinFares', methods=['GET'])
def get_sorted_set_data():
    try:
        source = request.args.get('s')    
        dest = request.args.get('d') 
        if source and dest:
            key = source+'-'+dest
        start = int(request.args.get('start', 0))
        end = int(request.args.get('end', -1))
        with_scores = request.args.get('with_scores', "True")

        if with_scores and with_scores.lower() == 'true':
            with_scores = True
        else:
            with_scores = False

        sorted_set_data = r.zrange(key, start, end, withscores=with_scores)

        response_data = []
        for item in sorted_set_data:
            date = item[0].decode('utf-8') if isinstance(item[0], bytes) else item[0]

            if with_scores:
                response_data.append({'date': date, 'minFare': item[1]})
            else:
                response_data.append({'date': date})

        return jsonify({'data': response_data})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
