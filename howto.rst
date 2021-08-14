How To - Project Documentation
==================================================

To build and serve backend in development mode::

    docker-compose -f local.yml up

To build and serve backend in production mode::

    docker-compose -f production.yml up --build


To run API tests::

    docker-compose -f test.yml up



To shorten a url (on develop - port 8000)::

    curl -d '{"url":"https://finn.auto/"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:8000/encode/


To Decode a url::

    Just click on the shortened URL :)