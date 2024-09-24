import aiohttp
#import asyncio
#import json

url = "https://owobot.com/api/status"



def get_max_shards(json_data):
    max_shard = 0
    for item in json_data:
        if 'shards' in item:
            shard_data = item['shards']
            max_shard_in_item = max(shard['shard'] for shard in shard_data)
            if max_shard_in_item > max_shard:
                max_shard = max_shard_in_item
    return max_shard + 1

def get_shard_id(server_id, total_shards):
    """
    getShardId: function(t) {
        var e = parseInt(this.search);
        return parseInt(e.toString(2).slice(0, -22), 2) % t;
    }
    -where t is total shards of owo bot

    code from :- owobot.com/status, a random js script there.
    """
    e = int(server_id)
    """
    bin() returns binary of an int, 
    first two charactrer is removed since it starts with prefix '0b'
    """
    binary_str = bin(e)[2:]
    #print(f"Binary string: {binary_str}")
    if len(binary_str) > 22:
        sliced_binary_str = binary_str[:-22]
    else:
        sliced_binary_str = '0' #this will never be executed.
    #print(f"Sliced binary string: {sliced_binary_str}")
    sliced_int = int(sliced_binary_str, 2) # the ,2) makes it back into integer
    #print(f"Sliced integer: {sliced_int}")
    shard_id = sliced_int % total_shards # the final modulus (i hope thats what its called) calc.
    return shard_id

#server_id = '420104212895104355044'


# Calculate and print the shard ID

async def delaycheck(session, server_id):
    try:
        async with session.get(url) as response:
            response.raise_for_status() #raises an HTTPError for bad responses (4xx, 5xx)
            json_data = response.json()
    except aiohttp.ClientError as e:
        print(f"An error occurred: {e}")

    #json_data = []
    shard_id = get_shard_id(server_id, get_max_shards(json_data))
    #print(f"Shard ID: {shard_id}")

    #print("\n\n ----------------------------------")


    for item in json_data:
        if 'shards' in item:
            shard_data = item['shards']
            for i in shard_data:
                if i["shard"] == shard_id:
                    return i
#delaycheck(None, server_id)



