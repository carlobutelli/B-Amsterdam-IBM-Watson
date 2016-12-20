import twitter
import json

api = twitter.Api(consumer_key='R49BASTgKR2rNk9tO9wzmk98a',
                  consumer_secret='wTUxkzXOXClj02zJ2hEkgzKyQUUGUpyjCW6Vl6Put2WxRRk772',
                  access_token_key='74159038-hPAziL8KdJp4TIZAfKdoC5O1RsH7bPkP1EUhP1o4l',
                  access_token_secret='y4puW2TMgCdJSuZam8zn2Q0ukKAmzjLZcc2pgzfgBN7se')

def get_twitter_data(usr):
    #print("VerifyCred: %s" % api.VerifyCredentials())
    max_id = None
    data = []
    for i in range(0, 100):
        statuses = api.GetUserTimeline(user_id=usr, include_rts=False, count=200, max_id=max_id)
        #print("len of data received: {}".format(len(statuses)))
        if (len(statuses) == 1) and (max_id is not None):
            break
        for status in statuses:
            if status.id == max_id:
                continue
            data.append(status.text)
            max_id = status.id
    #print("downloaded data length: {}".format(len(data)))
    print(json.dumps(data, indent=2, cls=DecimalEncoder))
    return [data, len(data)]


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

if __name__ == "__main__":
    get_twitter_data(74159038)
