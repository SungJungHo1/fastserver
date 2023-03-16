import uvicorn


if __name__ == '__main__':

    uvicorn.run("main:app",

                host="0.0.0.0",

                reload=True,

                # port=80,

                port=443,
 
                ssl_keyfile="./private.key",

                ssl_certfile="./certificate.pem"

                )
