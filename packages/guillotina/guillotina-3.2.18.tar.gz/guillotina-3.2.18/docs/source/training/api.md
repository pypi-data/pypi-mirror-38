# Using the Guillotina API

Before we start using the Guillotina API, let's get us some test data to play with.

Using the `testdata` command, we'll populate our database with some data from
wikipedia.


```
g testdata --per-node=5 --depth=2 --container=container
```


## Interacting with the API

You can use whatever you'd like but this training will mention use of Postman.

Open up Postman and do a `GET` on `http://localhost:8080/db/container`
with the username `root` and password `root` for basic auth.

We can not necessarily go over every single API but will touch on a few and
give a general understanding of how to explore and use the API.


## Creating content

To create content, do a `POST` request on a container or folder object.

```eval_rst
.. http:post:: /db/container

     Create Item

     **Example request**

     .. sourcecode:: http

        POST /db/container HTTP/1.1
        Accept: application/json
        Content-Type: application/json
        Authorization: Basic cm9vdDpyb290

        {
          "@type": "Item",
          "id": "foobar"
        }

     **Example response**

     .. sourcecode:: http

        HTTP/1.1 201 OK
        Content-Type: application/json

        {
          "@id": "http://localhost:8080/db/container/foobar",
          "@type": "Item",
          "parent": {
              "@id": "http://localhost:8080/db/container",
              "@type": "Container"
          },
          "creation_date": "2017-10-13T23:34:18.879391-05:00",
          "modification_date": "2017-10-13T23:34:18.879391-05:00",
          "UID": "f4ab591f22824404b55b66569f6a7502",
          "type_name": "Item",
          "title": null,
          "__behaviors__": [],
          "__name__": "foobar",
          "guillotina.behaviors.dublincore.IDublinCore": {
              "title": null,
              "description": null,
              "creation_date": "2017-10-13T23:34:18.879391-05:00",
              "modification_date": "2017-10-13T23:34:18.879391-05:00",
              "effective_date": null,
              "expiration_date": null,
              "creators": [
                  "root"
              ],
              "tags": null,
              "publisher": null,
              "contributors": [
                  "root"
              ]
          }
        }

     :reqheader Authorization: Required token to authenticate
     :statuscode 201: no error
     :statuscode 401: Invalid Auth code
     :statuscode 500: Error processing request
```


## Adding behaviors

To add a dynamic behavior, we use the `@behavior` endpoint.

```eval_rst
.. http:patch:: /db/container/foobar/@behaviors

     Add behavior

     **Example request**

     .. sourcecode:: http

        PATCH /db/container/foobar/@behaviors HTTP/1.1
        Accept: application/json
        Content-Type: application/json
        Authorization: Basic cm9vdDpyb290

        {
          "behavior": "guillotina.behaviors.attachment.IAttachment"
        }

     **Example response**

     .. sourcecode:: http

        HTTP/1.1 201 OK
        Content-Type: application/json

     :reqheader Authorization: Required token to authenticate
     :statuscode 201: no error
     :statuscode 401: Invalid Auth code
     :statuscode 500: Error processing request
```


## Uploading files

Simple file uploads can be done with the `@upload` endpoint.

```eval_rst
.. http:patch:: /db/container/foobar/@upload/file

     Upload file

     **Example request**

     .. sourcecode:: http

        PATCH /db/container/foobar/@upload/file HTTP/1.1
        Authorization: Basic cm9vdDpyb290

        <binary data>

     **Example response**

     .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

     :reqheader Authorization: Required token to authenticate
     :statuscode 200: no error
     :statuscode 401: Invalid Auth code
     :statuscode 500: Error processing request
```

Then, to download the file, use the `@download` endpoint.

```eval_rst
.. http:get:: /db/container/foobar/@download/file

     Download file

     **Example request**

     .. sourcecode:: http

        GET /db/container/foobar/@downlaod/file HTTP/1.1
        Authorization: Basic cm9vdDpyb290

     **Example response**

     .. sourcecode:: http

        HTTP/1.1 200 OK
        <binary data>

     :reqheader Authorization: Required token to authenticate
     :statuscode 200: no error
     :statuscode 401: Invalid Auth code
     :statuscode 500: Error processing request
```

## Uploading files with TUS

Guillotina also supports the TUS protocol using the `@tusupload` endpoint. The
TUS protocol allows you to upload large files in chunks and allows you to have
resumable uploads.


First, initialize the TUS upload with a POST

```eval_rst
.. http:post:: /db/container/foobar/@tusupload/file

     Upload file

     **Example request**

     .. sourcecode:: http

        POST /db/container/foobar/@tusupload/file HTTP/1.1
        Authorization: Basic cm9vdDpyb290
        UPLOAD-LENGTH: 2097152
        TUS-RESUMABLE: 1

     **Example response**

     .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

     :reqheader Authorization: Required token to authenticate
     :statuscode 200: no error
     :statuscode 401: Invalid Auth code
     :statuscode 500: Error processing request
```

Next, upload the chunks(here we're doing chunks of 1MB):

```eval_rst
.. http:patch:: /db/container/foobar/@tusupload/file

     Upload file

     **Example request**

     .. sourcecode:: http

        PATCH /db/container/foobar/@tusupload/file HTTP/1.1
        Authorization: Basic cm9vdDpyb290
        Upload-Offset: 0
        TUS-RESUMABLE: 1
        CONTENT-LENGTH: 1048576

        < binary data >

     **Example response**

     .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

     :reqheader Authorization: Required token to authenticate
     :statuscode 200: no error
     :statuscode 401: Invalid Auth code
     :statuscode 500: Error processing request
```

And final chunk of 1MB:

```eval_rst
.. http:patch:: /db/container/foobar/@tusupload/file

     Upload file

     **Example request**

     .. sourcecode:: http

        PATCH /db/container/foobar/@tusupload/file HTTP/1.1
        Authorization: Basic cm9vdDpyb290
        Upload-Offset: 1048576
        TUS-RESUMABLE: 1
        CONTENT-LENGTH: 1048576

        < binary data >

     **Example response**

     .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

     :reqheader Authorization: Required token to authenticate
     :statuscode 200: no error
     :statuscode 401: Invalid Auth code
     :statuscode 500: Error processing request
```

### Unknown upload size

Guillotina's TUS implementation has support for the `Upload-Defer-Length` header.
This means you can upload files with an unknown final upload size.

In order to implement this correctly, you will need to provide the
`Upload-Defer-Length: 1` header and value on the initial POST to start the TUS
upload. You are then not required to provide the `UPLOAD-LENGTH` header.

Then, before or on your last chunk, provide a `UPLOAD-LENGTH` value to let
TUS know the upload can not finish.


### Simultaneous TUS uploads

Guillotina's TUS implementation also attempts to prevent simultaneous uploaders.

If two users attempt to start an upload on the same object + field at the same
time, a 412 error will be thrown. Guillotina tracks upload activity to detect this.
If there is no activity detected for 15 seconds with an unfinished TUS upload,
no error is thrown.

To override this, send the `TUS-OVERRIDE-UPLOAD: 1` header.


## Modifying permissions

The `@sharing` endpoint is available to inspect and modify permissions on an object.

```eval_rst
.. http:get:: /db/container/foobar/@sharing

     Get sharing information

     **Example request**

     .. sourcecode:: http

        GET /db/container/foobar/@sharing HTTP/1.1
        Authorization: Basic cm9vdDpyb290

     **Example response**

     .. sourcecode:: http

        HTTP/1.1 201 OK
        Content-Type: application/json

        {
          "local": {
              "roleperm": {},
              "prinperm": {},
              "prinrole": {
                  "root": {
                      "guillotina.Owner": "Allow"
                  }
              }
          },
          "inherit": [
              {
                  "@id": "http://localhost:8080/db/container",
                  "roleperm": {},
                  "prinperm": {},
                  "prinrole": {
                      "root": {
                          "guillotina.ContainerAdmin": "Allow",
                          "guillotina.Owner": "Allow"
                      }
                  }
              }
          ]
        }

     :reqheader Authorization: Required token to authenticate
     :statuscode 200: no error
     :statuscode 401: Invalid Auth code
     :statuscode 500: Error processing request
```

To modify, we use the same endpoint but with a `POST`.


```eval_rst
.. http:post:: /db/container/foobar/@sharing

     Add local permissions

     **Example request**

     .. sourcecode:: http

        POST /db/container/foobar/@sharing HTTP/1.1
        Content-Type: application/json
        Authorization: Basic cm9vdDpyb290

        {
          "prinperm": [
            {
              "principal": "foobar",
              "permission": "guillotina.ModifyContent",
              "setting": "Allow"
            }
          ]
        }

     **Example response**

     .. sourcecode:: http

        HTTP/1.1 201 OK
        Content-Type: application/json

        {}

     :reqheader Authorization: Required token to authenticate
     :statuscode 200: no error
     :statuscode 401: Invalid Auth code
     :statuscode 500: Error processing request
```

There are three types of permission settings you can modify:

- prinperm: principal + permission
- prinrole: principal + role
- roleperm: role + permission

Each change can use the following settings:

- Allow : you set it on the resource and the children will inherit
- Deny : you set in on the resource and the children will inherit
- AllowSingle : you set in on the resource and the children will not inherit
- Unset : you remove the setting


## Exploring the API with Swagger

In the previous step, we installed `guillotina_swagger`. With Swagger, we can
inspect any context and explore the API.

Visit `http://localhost:8080/@docs`

![alt text](../../_static/img/swagger.png "Swagger")

click the `Authorize` button

![alt text](../../_static/img/auth-swagger.png "Swagger Auth")


The `Base API Endpoint` setting is what the current context is that you're exploring
on. If you create content at `/db/container/foobar` and want to explore that
content's API, you should change the URL. Different content types will have
different services available.



**References**

  - [REST API](../../rest/index)
  - [Behaviors](../../developer/behavior)
  - [Security](../../developer/security)
