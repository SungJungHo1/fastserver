import uvicorn


if __name__ == '__main__':

    uvicorn.run("main:app",

                host="0.0.0.0",

                port=80,

                reload=True,

                # ssl_keyfile="./private.key",

                # ssl_certfile="./certificate.pem"

                )
