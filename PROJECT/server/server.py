import asyncio
import alg
import alg2
import alg3
from websockets.server import serve
import ast
import time

#обрабатывает сообщения от клиента
async def echo(websocket):
    async for message in websocket:
        m = message.split()
        if m[0] == 'start':
                lst = ast.literal_eval(m[1])
                lst[2] = float(lst[2]) #PC
                lst[4] = float(lst[4]) #PM
                lst[5] = int(lst[5]) 
                lst[6] = int(lst[6]) 
                if lst[7] == '1':
                    t0 = time.time()
                    await alg.GA(websocket, sel=lst[0], mate=lst[1], PC=lst[2], muta=lst[3], PM=lst[4], sizeP=lst[5], sizeI=lst[6])
                    print(f'Время работы программы: {time.time()-t0}')
                elif lst[7] == '2':
                    t0 = time.time()
                    await alg2.GA(websocket, sel=lst[0], mate=lst[1], PC=lst[2], muta=lst[3], PM=lst[4], sizeP=lst[5], sizeI=lst[6])
                    print(f'Время работы программы: {time.time()-t0}')
                else:
                    t0 = time.time()
                    await alg3.GA(websocket, sel=lst[0], mate=lst[1], PC=lst[2], muta=lst[3], PM=lst[4], sizeP=lst[5], sizeI=lst[6])
                    print(f'Время работы программы: {time.time()-t0}')

#начинает работать в бесконечном цикле
async def main(): 
    async with serve(echo, "localhost", 5600):
        await asyncio.Future() 

asyncio.run(main())