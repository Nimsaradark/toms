from telegram import Update 
from telegram.ext import CallbackContext
from .functions import *
import asyncio

QUERY_DICT = {
    "Q3N8D" : G5V1K,
    "J4P6L" : A9X2F,
    "STIX" : FG3ZX,
    "M7T5Z" : help_page,
    "MVFX2" : MSX34,
    "GSX21" : GSX34,
    "SDX63" : THDX23,
    "BC2ML" : B2MLX1,
    "EDBX2" : EDCX12,
    "ECPX1" : EDCPX52,
    "BDBX1" : EDCX11,
    "ETPX1" : EDCPX53,
    "DELX12" : EDCPX54,
    "DLXF41" : EDCPX55,
    "TCX51" : GTVX162,
    "VTX12" : GTVX163,
    "RDX152" : FDX152,
    "RQMX16" : FDX153,
    "DNX15" : FDX154,
    "DNX16" : FDX156,
    "EQPX1" : EDCPX56,
    "EFPX1" : EDCPX57,
    "SDTX15" : SDTX12,
}

async def button_handler(update: Update , context: CallbackContext):
    query = update.callback_query
    button = query.data
    if ':' in str(button):
        func = button.split(":")[0]
        function = QUERY_DICT.get(func)
        if func == 'NO':
            await query.answer()
        if func == 'Close':
            await query.delete_message()
        if func ==  "ERX45":
            await query.answer("unknown error occurred",show_alert=True)
        elif function:
            asyncio.create_task(function(update,context))
        else:
            await query.answer("This Feature is not availabel yet !",show_alert=True)

        
