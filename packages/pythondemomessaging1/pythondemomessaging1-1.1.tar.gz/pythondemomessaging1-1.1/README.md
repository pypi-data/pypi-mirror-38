# Getting started

TODO: Add a description

## How to Build


You must have Python ```2 >=2.7.9``` or Python ```3 >=3.4``` installed on your system to install and run this SDK. This SDK package depends on other Python packages like nose, jsonpickle etc. 
These dependencies are defined in the ```requirements.txt``` file that comes with the SDK.
To resolve these dependencies, you can use the PIP Dependency manager. Install it by following steps at [https://pip.pypa.io/en/stable/installing/](https://pip.pypa.io/en/stable/installing/).

Python and PIP executables should be defined in your PATH. Open command prompt and type ```pip --version```.
This should display the version of the PIP Dependency Manager installed if your installation was successful and the paths are properly defined.

* Using command line, navigate to the directory containing the generated files (including ```requirements.txt```) for the SDK.
* Run the command ```pip install -r requirements.txt```. This should install all the required dependencies.

![Building SDK - Step 1](https://apidocs.io/illustration/python?step=installDependencies&workspaceFolder=Messages-Python)


## How to Use

The following section explains how to use the Messages SDK package in a new project.

### 1. Open Project in an IDE

Open up a Python IDE like PyCharm. The basic workflow presented here is also applicable if you prefer using a different editor or IDE.

![Open project in PyCharm - Step 1](https://apidocs.io/illustration/python?step=pyCharm)

Click on ```Open``` in PyCharm to browse to your generated SDK directory and then click ```OK```.

![Open project in PyCharm - Step 2](https://apidocs.io/illustration/python?step=openProject0&workspaceFolder=Messages-Python)     

The project files will be displayed in the side bar as follows:

![Open project in PyCharm - Step 3](https://apidocs.io/illustration/python?step=openProject1&workspaceFolder=Messages-Python&projectName=pythondemomessaging1)     

### 2. Add a new Test Project

Create a new directory by right clicking on the solution name as shown below:

![Add a new project in PyCharm - Step 1](https://apidocs.io/illustration/python?step=createDirectory&workspaceFolder=Messages-Python&projectName=pythondemomessaging1)

Name the directory as "test"

![Add a new project in PyCharm - Step 2](https://apidocs.io/illustration/python?step=nameDirectory)
   
Add a python file to this project with the name "testsdk"

![Add a new project in PyCharm - Step 3](https://apidocs.io/illustration/python?step=createFile&workspaceFolder=Messages-Python&projectName=pythondemomessaging1)

Name it "testsdk"

![Add a new project in PyCharm - Step 4](https://apidocs.io/illustration/python?step=nameFile)

In your python file you will be required to import the generated python library using the following code lines

```Python
from pythondemomessaging1.pythondemomessaging_1_client import Pythondemomessaging1Client
```

![Add a new project in PyCharm - Step 4](https://apidocs.io/illustration/python?step=projectFiles&workspaceFolder=Messages-Python&libraryName=pythondemomessaging1.pythondemomessaging_1_client&projectName=pythondemomessaging1&className=Pythondemomessaging1Client)

After this you can write code to instantiate an API client object, get a controller object and  make API calls. Sample code is given in the subsequent sections.

### 3. Run the Test Project

To run the file within your test project, right click on your Python file inside your Test project and click on ```Run```

![Run Test Project - Step 1](https://apidocs.io/illustration/python?step=runProject&workspaceFolder=Messages-Python&libraryName=pythondemomessaging1.pythondemomessaging_1_client&projectName=pythondemomessaging1&className=Pythondemomessaging1Client)


## How to Test

You can test the generated SDK and the server with automatically generated test
cases. unittest is used as the testing framework and nose is used as the test
runner. You can run the tests as follows:

  1. From terminal/cmd navigate to the root directory of the SDK.
  2. Invoke ```pip install -r test-requirements.txt```
  3. Invoke ```nosetests```

## Initialization

### Authentication
In order to setup authentication and initialization of the API client, you need the following information.

| Parameter | Description |
|-----------|-------------|
| api_key | TODO: add a description |
| api_secret | TODO: add a description |



API client can be initialized as following.

```python
# Configuration parameters and credentials
api_key = 'api_key'
api_secret = 'api_secret'

client = Pythondemomessaging1Client(api_key, api_secret)
```



# Class Reference

## <a name="list_of_controllers"></a>List of Controllers

* [MessagesController](#messages_controller)
* [RepliesController](#replies_controller)
* [DeliveryReportsController](#delivery_reports_controller)

## <a name="messages_controller"></a>![Class: ](https://apidocs.io/img/class.png ".MessagesController") MessagesController

### Get controller instance

An instance of the ``` MessagesController ``` class can be accessed from the API Client.

```python
 messages_controller = client.messages
```

### <a name="create_send_messages"></a>![Method: ](https://apidocs.io/img/method.png ".MessagesController.create_send_messages") create_send_messages

> Submit one or more (up to 100 per request) SMS or text to voice messages for delivery.

```python
def create_send_messages(self,
                             body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body = SendMessagesRequest()

result = messages_controller.create_send_messages(body)

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 400 | Something went wrong. Please try again later. |




### <a name="get_message_status"></a>![Method: ](https://apidocs.io/img/method.png ".MessagesController.get_message_status") get_message_status

> Retrieve the current status of a message using the message ID returned in the send messages end point.
> A successful request to the get message status endpoint will return a response body as follows:
> ```json
> {
>     "format": "SMS",
>     "content": "My first message!",
>     "metadata": {
>         "key1": "value1",
>         "key2": "value2"
>     },
>     "message_id": "877c19ef-fa2e-4cec-827a-e1df9b5509f7",
>     "callback_url": "https://my.callback.url.com",
>     "delivery_report": true,
>     "destination_number": "+61401760575",
>     "scheduled": "2016-11-03T11:49:02.807Z",
>     "source_number": "+61491570157",
>     "source_number_type": "INTERNATIONAL"
>     "message_expiry_timestamp": "2016-11-03T11:49:02.807Z",
>     "status": "enroute"
> }
> ```
> The status property of the response indicates the current status of the message. See the Delivery
> Reports section of this documentation for more information on message statues.
> *Note: If an invalid or non existent message ID parameter is specified in the request, then
> a HTTP 404 Not Found response will be returned*

```python
def get_message_status(self,
                           message_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| messageId |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
message_id = 'messageId'

result = messages_controller.get_message_status(message_id)

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 404 | Message not found |




### <a name="update_cancel_scheduled_message"></a>![Method: ](https://apidocs.io/img/method.png ".MessagesController.update_cancel_scheduled_message") update_cancel_scheduled_message

> Cancel a scheduled message that has not yet been delivered.
> A scheduled message can be cancelled by updating the status of a message from ```scheduled```
> to ```cancelled```. This is done by submitting a PUT request to the messages endpoint using
> the message ID as a parameter (the same endpoint used above to retrieve the status of a message).
> The body of the request simply needs to contain a ```status``` property with the value set
> to ```cancelled```.
> ```json
> {
>     "status": "cancelled"
> }
> ```
> *Note: Only messages with a status of scheduled can be cancelled. If an invalid or non existent
> message ID parameter is specified in the request, then a HTTP 404 Not Found response will be
> returned*

```python
def update_cancel_scheduled_message(self,
                                        message_id,
                                        content_type,
                                        body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| messageId |  ``` Required ```  | TODO: Add a parameter description |
| contentType |  ``` Required ```  | TODO: Add a parameter description |
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
message_id = 'messageId'
content_type = 'Content-Type'
body = CancelScheduledMessageRequest()

result = messages_controller.update_cancel_scheduled_message(message_id, content_type, body)

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 400 | TODO: Add an error description |
| 404 | TODO: Add an error description |




[Back to List of Controllers](#list_of_controllers)

## <a name="replies_controller"></a>![Class: ](https://apidocs.io/img/class.png ".RepliesController") RepliesController

### Get controller instance

An instance of the ``` RepliesController ``` class can be accessed from the API Client.

```python
 replies_controller = client.replies
```

### <a name="get_check_replies"></a>![Method: ](https://apidocs.io/img/method.png ".RepliesController.get_check_replies") get_check_replies

> Check for any replies that have been received.
> Replies are messages that have been sent from a handset in response to a message sent by an
> application or messages that have been sent from a handset to a inbound number associated with
> an account, known as a dedicated inbound number (contact <support@messagemedia.com> for more
> information on dedicated inbound numbers).
> Each request to the check replies endpoint will return any replies received that have not yet
> been confirmed using the confirm replies endpoint. A response from the check replies endpoint
> will have the following structure:
> ```json
> {
>     "replies": [
>         {
>             "metadata": {
>                 "key1": "value1",
>                 "key2": "value2"
>             },
>             "message_id": "877c19ef-fa2e-4cec-827a-e1df9b5509f7",
>             "reply_id": "a175e797-2b54-468b-9850-41a3eab32f74",
>             "date_received": "2016-12-07T08:43:00.850Z",
>             "callback_url": "https://my.callback.url.com",
>             "destination_number": "+61491570156",
>             "source_number": "+61491570157",
>             "vendor_account_id": {
>                 "vendor_id": "MessageMedia",
>                 "account_id": "MyAccount"
>             },
>             "content": "My first reply!"
>         },
>         {
>             "metadata": {
>                 "key1": "value1",
>                 "key2": "value2"
>             },
>             "message_id": "8f2f5927-2e16-4f1c-bd43-47dbe2a77ae4",
>             "reply_id": "3d8d53d8-01d3-45dd-8cfa-4dfc81600f7f",
>             "date_received": "2016-12-07T08:43:00.850Z",
>             "callback_url": "https://my.callback.url.com",
>             "destination_number": "+61491570157",
>             "source_number": "+61491570158",
>             "vendor_account_id": {
>                 "vendor_id": "MessageMedia",
>                 "account_id": "MyAccount"
>             },
>             "content": "My second reply!"
>         }
>     ]
> }
> ```
> Each reply will contain details about the reply message, as well as details of the message the reply was sent
> in response to, including any metadata specified. Every reply will have a reply ID to be used with the
> confirm replies endpoint.
> *Note: The source number and destination number properties in a reply are the inverse of those
> specified in the message the reply is in response to. The source number of the reply message is the
> same as the destination number of the original message, and the destination number of the reply
> message is the same as the source number of the original message. If a source number
> wasn't specified in the original message, then the destination number property will not be present
> in the reply message.*
> Subsequent requests to the check replies endpoint will return the same reply messages and a maximum
> of 100 replies will be returned in each request. Applications should use the confirm replies endpoint
> in the following pattern so that replies that have been processed are no longer returned in
> subsequent check replies requests.
> 1. Call check replies endpoint
> 2. Process each reply message
> 3. Confirm all processed reply messages using the confirm replies endpoint
> *Note: It is recommended to use the Webhooks feature to receive reply messages rather than polling
> the check replies endpoint.*

```python
def get_check_replies(self)
```

#### Example Usage

```python

result = replies_controller.get_check_replies()

```


### <a name="create_confirm_replies_as_received"></a>![Method: ](https://apidocs.io/img/method.png ".RepliesController.create_confirm_replies_as_received") create_confirm_replies_as_received

> Mark a reply message as confirmed so it is no longer returned in check replies requests.
> The confirm replies endpoint is intended to be used in conjunction with the check replies endpoint
> to allow for robust processing of reply messages. Once one or more reply messages have been processed
> they can then be confirmed using the confirm replies endpoint so they are no longer returned in
> subsequent check replies requests.
> The confirm replies endpoint takes a list of reply IDs as follows:
> ```json
> {
>     "reply_ids": [
>         "011dcead-6988-4ad6-a1c7-6b6c68ea628d",
>         "3487b3fa-6586-4979-a233-2d1b095c7718",
>         "ba28e94b-c83d-4759-98e7-ff9c7edb87a1"
>     ]
> }
> ```
> Up to 100 replies can be confirmed in a single confirm replies request.

```python
def create_confirm_replies_as_received(self,
                                           content_type,
                                           body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| contentType |  ``` Required ```  | TODO: Add a parameter description |
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
content_type = 'Content-Type'
body = ConfirmRepliesAsReceivedRequest()

result = replies_controller.create_confirm_replies_as_received(content_type, body)

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 400 | Request was invalid |




[Back to List of Controllers](#list_of_controllers)

## <a name="delivery_reports_controller"></a>![Class: ](https://apidocs.io/img/class.png ".DeliveryReportsController") DeliveryReportsController

### Get controller instance

An instance of the ``` DeliveryReportsController ``` class can be accessed from the API Client.

```python
 delivery_reports_controller = client.delivery_reports
```

### <a name="get_check_delivery_reports"></a>![Method: ](https://apidocs.io/img/method.png ".DeliveryReportsController.get_check_delivery_reports") get_check_delivery_reports

> Check for any delivery reports that have been received.
> Delivery reports are a notification of the change in status of a message as it is being processed.
> Each request to the check delivery reports endpoint will return any delivery reports received that
> have not yet been confirmed using the confirm delivery reports endpoint. A response from the check
> delivery reports endpoint will have the following structure:
> ```json
> {
>     "delivery_reports": [
>         {
>             "callback_url": "https://my.callback.url.com",
>             "delivery_report_id": "01e1fa0a-6e27-4945-9cdb-18644b4de043",
>             "source_number": "+61491570157",
>             "date_received": "2017-05-20T06:30:37.642Z",
>             "status": "enroute",
>             "delay": 0,
>             "submitted_date": "2017-05-20T06:30:37.639Z",
>             "original_text": "My first message!",
>             "message_id": "d781dcab-d9d8-4fb2-9e03-872f07ae94ba",
>             "vendor_account_id": {
>                 "vendor_id": "MessageMedia",
>                 "account_id": "MyAccount"
>             },
>             "metadata": {
>                 "key1": "value1",
>                 "key2": "value2"
>             }
>         },
>         {
>             "callback_url": "https://my.callback.url.com",
>             "delivery_report_id": "0edf9022-7ccc-43e6-acab-480e93e98c1b",
>             "source_number": "+61491570158",
>             "date_received": "2017-05-21T01:46:42.579Z",
>             "status": "enroute",
>             "delay": 0,
>             "submitted_date": "2017-05-21T01:46:42.574Z",
>             "original_text": "My second message!",
>             "message_id": "fbb3b3f5-b702-4d8b-ab44-65b2ee39a281",
>             "vendor_account_id": {
>                 "vendor_id": "MessageMedia",
>                 "account_id": "MyAccount"
>             },
>             "metadata": {
>                 "key1": "value1",
>                 "key2": "value2"
>             }
>         }
>     ]
> }
> ```
> Each delivery report will contain details about the message, including any metadata specified
> and the new status of the message (as each delivery report indicates a change in status of a
> message) and the timestamp at which the status changed. Every delivery report will have a
> unique delivery report ID for use with the confirm delivery reports endpoint.
> *Note: The source number and destination number properties in a delivery report are the inverse of
> those specified in the message that the delivery report relates to. The source number of the
> delivery report is the destination number of the original message.*
> Subsequent requests to the check delivery reports endpoint will return the same delivery reports
> and a maximum of 100 delivery reports will be returned in each request. Applications should use the
> confirm delivery reports endpoint in the following pattern so that delivery reports that have been
> processed are no longer returned in subsequent check delivery reports requests.
> 1. Call check delivery reports endpoint
> 2. Process each delivery report
> 3. Confirm all processed delivery reports using the confirm delivery reports endpoint
> *Note: It is recommended to use the Webhooks feature to receive reply messages rather than
> polling the check delivery reports endpoint.*

```python
def get_check_delivery_reports(self)
```

#### Example Usage

```python

result = delivery_reports_controller.get_check_delivery_reports()

```


### <a name="create_confirm_delivery_reports_as_received"></a>![Method: ](https://apidocs.io/img/method.png ".DeliveryReportsController.create_confirm_delivery_reports_as_received") create_confirm_delivery_reports_as_received

> Mark a delivery report as confirmed so it is no longer return in check delivery reports requests.
> The confirm delivery reports endpoint is intended to be used in conjunction with the check delivery
> reports endpoint to allow for robust processing of delivery reports. Once one or more delivery
> reports have been processed, they can then be confirmed using the confirm delivery reports endpoint so they
> are no longer returned in subsequent check delivery reports requests.
> The confirm delivery reports endpoint takes a list of delivery report IDs as follows:
> ```json
> {
>     "delivery_report_ids": [
>         "011dcead-6988-4ad6-a1c7-6b6c68ea628d",
>         "3487b3fa-6586-4979-a233-2d1b095c7718",
>         "ba28e94b-c83d-4759-98e7-ff9c7edb87a1"
>     ]
> }
> ```
> Up to 100 delivery reports can be confirmed in a single confirm delivery reports request.

```python
def create_confirm_delivery_reports_as_received(self,
                                                    content_type,
                                                    body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| contentType |  ``` Required ```  | TODO: Add a parameter description |
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
content_type = 'Content-Type'
body = ConfirmDeliveryReportsAsReceivedRequest()

result = delivery_reports_controller.create_confirm_delivery_reports_as_received(content_type, body)

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 400 | TODO: Add an error description |




[Back to List of Controllers](#list_of_controllers)



