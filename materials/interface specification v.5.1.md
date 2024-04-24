# Interface Specification

[TOC]



## frontend-database

##### Interface 1	frontend::Login ==> database::Login 

~~~json
{
	"InterfaceId": {
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {"type": "string"},
    "UserName": {
        "type": "string",
    	"minLength": 1
    },
    "PassWord": {
        "type": "string",
    	"minLength": 1,
        "maxLength": 6
    }
}

return with

{
    "InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "miLLength": 1,
    },
    "MatchToken": {"type": "boolean"}
}
~~~

+ Tip1: InterfaceId means the id of interface that we use the identify the interface index and json content. We have 32 interfaces in total so the InterfaceId will range from 1 to 32.
+ Tip 2: CurrentUser is None if this is a anonymous visiting, otherwise it is the UserName.

+ Description of the interface: When the user logs in, this interface is called. On the front end, the user needs to input the Username and Password, which are then sent to the database. The database performs verification, and the result of the verification is indicated by the returned match_token. If the inputted Username and Password successfully match those in the database, the login is successful; otherwise, it fails.

##### Interface 2	frontend::Location ==> database::Location

~~~json
{
    "InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "CurrentLocation": {
        "type": "object::Location",
        "properties": "Illustrated in appendix"
    }
}
~~~

+ Description of the interface: The user, seeking recommended content, actively provides location information to the database.

##### Interface 3	frontend::Store ==> database::Store

~~~json
{
    "InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "StoreName": {
        "type": "string",
        "minLength": 1
    }
}

return with

{
    "InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "StoreList": {
    	"type": "array",
        "items": {
            "type": "object::Store",
            "properties": "Illustrated in appendix"
        },
        "minItems": 0,
        "uniqueItems": true
    }
}
~~~

+ Tip1: This provides the function of querying the store information given the store name.
+ Description of the interface: When a user wants to inquire about store information, they provide the StoreName to the database. Since the StoreName provided by the user might be incomplete or there may be stores with the same name, the database should return a list of stores that meet the criteria.

##### Interface 4	frontend::HuntedStore ==> database::HuntedStore

```json
{
    "InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "HuntedStoreIdList": {
        "type": "array",
        "items": {
            "type": "integer",
         	"minimum": 0
        },
        "minItems": 0,
        "uniqueItems": true
    }
}
```

+ Tip1: HuntedList is like a "Browsing history".

+ Tip2: In "items," the "type" labeled as "integer" refers to the StoreId.

+ Description of the interface: When a user browses new stores, they need to provide the HuntedStoreIdList to the database for updating the content stored in the database.

##### Interface 5	database::HuntedStore ==> frontend::HuntedStore

```json
{
 	"InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "HuntedStoreIdList": {
        "type": "array",
        "items": {
            "type": "integer",
         	"minimum": 0
        },
        "minItems": 0,
        "uniqueItems": true
    }
}
```

+ Tips1: This is for displaying the HuntedList.
+ Description of the interface: When a user needs to view their browsing history, the database provides information about the HuntedStoreIdList to the front end.

##### Interface 6	frontend::Item ==> database:Item

```json
{
 	"InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "ItemName": {
        "type": "string",
        "minLength": 1
    }
}

return with

{
 	"InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "ItemList": {
        "type": "array",
        "items": {
            "type": "Item",
         	"properties": "Illustrated in appendix"
        },
        "minItems": 0,
        "uniqueItems": true
    }
}
```

+ Tips1: This provides the function of querying the item information given the item name.
+ Description of the interface: When a user wants to inquire about item information, they provide the ItemName to the database. Since the ItemName provided by the user might be incomplete or there may be items with the same name, the database should return a list of items that meet the criteria.

##### Interface 7	frontend::Map ==> database::Map

```json
{
 	"InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "MyLocation": {
        "type": "object::Location",
        "properties": "Illustrated in appendix"
    },
    "RequestType": {
        "type":"integer",
        "minimum": 1,
        "maximum": 2
    },
}

return with

{
 	"InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "StoreList": {
    	"type": "array",
        "items": {
            "type": "object::Store",
            "properties": "Illustrated in appendix"
        },
        "minItems": 0,
        "uniqueItems": true
    }
}
```

+ Description of the interface: RequestType=1 means this a request searching for nearby stores provided with "MyLocation".   RequestType=2 means this is a request for a list recommended stores. The user provides the RequestType and MyLocation to the database to obtain the needed StoreList.

##### Interface 8	frontend::Feedback ==> database::Feedback

```json
{
	"InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "StoreId": {
		"type": "integer",
        "minimum": 0
    },
	"comment": {
        "type": "string",
        "minLength": 0
    },
	"rating": {
        "type":"integer",
        "minimum": 1,
        "maximum": 10
    }
}
```

+ Tip1 : Feedback is a rating that evaluate the recommendation results.
+ Tip2 : "rating" should be a positive integer from 1 to 10.
+ Description of the interface: Users evaluate the store recommendations provided by the recommendation system, specifically including comments and ratings, which are transmitted to the database.

##### Interface 9	frontend::Feedback ==> database::Feedback

```json
{
	"InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "ItemId": {
        "type":"integer",
        "minimum": 0
    },
	"comment": {
        "type": "string",
        "minLength": 0
    },
	"rating": {
        "type":"integer",
        "minimum": 1,
        "maximum": 10
    }
}
```

+ Description of the interface: Similar to Interface8. Users evaluate the recommended item results from the recommendation system, specifically including comments and ratings, which are transmitted to the database.

##### Interface 10	frontend::Customer ==> database:: Customer 

```json
{
	"InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "UserName": {
        "type": "string",
    	"minLength": 1
    },
    "PassWord": {
        "type": "string",
    	"minLength": 1,
        "maxLength": 6
    },
    "Birthday": {
        "type": "date"
    },
    "Interests": {
    	"type": "array",
       	"items": "integer",
        "minimum": 0
    },
    "CurrentLocation":{
        "type": "object::Location",
        "properties": "Illustrated in appendix"
    }
}
```

+ Tip1: This is used to update customer information stored in the database. 
+ Description of the interface: When a user wishes to update their information, they provide the database with new details such as Birthday, Interests, and CurrentLocation. It should be noted that for security reasons, before updating the information, the user needs to re-enter their Username and Password for verification.

##### Interface11	database::Customer ==> frontend:: Customer

```json
{
	"InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "UserName": {
        "type": "string",
    	"minLength": 1
    },
    "PassWord": {
        "type": "string",
    	"minLength": 1,
        "maxLength": 6
    },
    "Birthday": {
        "type": "date"
    },
    "Interests": {
    	"type": "array",
       	"items": "integer",
        "minimum": 0
    },
    "CurrentLocation":{
        "type": "object::Location",
        "properties": "Illustrated in appendix"
    }
}
```

+ Tip1: This is used to show the customer information on the screen. Password should be set to "None".
+ Description of the interface: The database provides the current user with relevant information about other users, without the need to enter a password.

##### Interface 12 frontend::Registration ==> database::Registration

~~~json
{
	"InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "UserName": {
        "type": "string",
    	"minLength": 1
    },
    "PassWord": {
        "type": "string",
    	"minLength": 1,
        "maxLength": 6
    }
}

return with
{
	"InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "successful_token": {"type": "boolean"}
}

~~~

+ Tip1: this is used for registration and to check whether the UserName is unique.
+ Description of the interface: Users register by entering their Username and Password on the front end, which are then transmitted to the database. The database checks if the same Username already exists and returns a successful_token to the front end to indicate whether the registration was successful or not. Registration fails if there is a duplicate name; otherwise, it is successful.

---



## algorithm-database

##### Interface 13	database::Store ==> algorithm::Store

~~~json
{
	"InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
	"Items": {
        "type": "array",
        "items": {
            "type": "object::Item",
            "preperties": "Illustrated in appendix"
        },
        "minItems": 1,
        "uniqueItems": true
    },
	"Location": {
        "type": "object::Location",
        "properties": "Illustrated in appendix"
    }
}
~~~

##### Interface 14	database::Customer ==> algorithm::user

~~~json
{
   	"InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "UserId": {
        "type": "integer",
        "minimum": 0
    },
    "UserData": {
        "type": "array",
        "items": {
            "type": "object::Customer",
            "preperties": "Illustrated in appendix"
        },
        "minItems": 1,
        "uniqueItems": true
    }
}
~~~

##### Interface 15	database::Item ==> algorithm::recommendation algorithm

~~~json
{
    "InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "ItemData": {
        "type": "array",
        "items": {
            "type": "object::Item",
            "preperties": "Illustrated in appendix"
        },
        "minItems": 1,
        "uniqueItems": true
    }
}
~~~

##### Interface 16	algorithm::recommendation algorithm ==> database:: 

~~~json
{
    "InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "RecommendedStores": {
        "type": "array",
        "items": {
            "type": "object::Item",
            "preperties": "Illustrated in appendix"
        },
        "minItems": 1,
        "uniqueItems": true
    }
}
~~~



---



## web-database

##### Interface 17	web::Registration ==> database::Registration

~~~json
{
    "InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "UserName": {
        "type": "string",
    	"minLength": 1
    },
    "HashedPassWord": {
        "type": "string",
    	"minLength": 1,
        "maxLength": 6
    }
}
~~~

##### Interface 18	database::Registration ==> web::Registration

~~~json
{
    "InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "UserName": {
        "type": "string",
    	"minLength": 1
    },
    "HashedPassWord": {
        "type": "string",
    	"minLength": 1,
        "maxLength": 6
    }
}
~~~

##### Interface 19	database::Login ==> web::Login

~~~json
{
    "InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "UserName": {
        "type": "string",
    	"minLength": 1
    },
    "HashedPassWord": {
        "type": "string",
    	"minLength": 1,
        "maxLength": 6
    },
}
~~~

##### Interface 20	web::Management ==> database::Administrator

~~~json
{
    "InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "UserData" : {
    	"type": "object::User",
        "properties": "Illustrated in appendix"
    },
	"StoreInfo" : {
    	"type": "object::Store",
        "properties": "Illustrated in appendix"
    }
}
~~~

##### Interface 21	database::Administrator ==> web::Management

~~~json
{
    "InterfaceId": {
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "userData": {
    	"type": "object::User",
        "properties": "Illustrated in appendix"
    },
	"storeInfo": {
    	"type": "object::Store",
        "properties": "Illustrated in appendix"
    }
}
~~~

##### Interface 22	database::Analytics ==> web::Analytics

~~~json
{
    "InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "userEngagementData": "",
    "performanceData":""
}
~~~

**<font color='red'>Warning: object not defined.</font>**

##### Interface 23	database::Store ==> web::StoreOwner

~~~json
{
    "InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "statistics": {
    	"type": "object::Statistics",
        "properties": "Illustrated in appendix"
    }
}
~~~

##### Interface 24	 web::StoreOwner ==> database::Store

~~~json
{
    "InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "storeInfo": {
    	"type": "object::StoreInfo",
        "properties": "Illustrated in appendix"
    }
}
~~~

##### Interface 25	web::StoreInfo ==> database::Store

~~~json
{
    "InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "storeName": {
        "type": "string",
        "minLength": 1
    },
	"location" : {
        "type": "object::Location",
        "properties": "Illustrated in appendix"
    },
    "Items": {
        "type": "array",
        "items": {
            "type": "object::Item",
            "preperties": "Illustrated in appendix"
        },
        "minItems": 1,
        "uniqueItems": true
    }
}
~~~

Description: The UserName and Password of the store owner should be stored in "StoreInfo" class in database.  

##### Interface 26	web::User ==> database::Store

~~~json
{
    "InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "UserName": {
        "type": "string",
    	"minLength": 1
    },
    "HashedPassWord": {
        "type": "string",
    	"minLength": 1,
        "maxLength": 6
    }
}
~~~

##### Interface 27	database::Store ==> web::User

~~~json
{
    "InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "UserName": {
        "type": "string",
    	"minLength": 1
    },
    "HashedPassWord": {
        "type": "string",
    	"minLength": 1,
        "maxLength": 6
    }
}
~~~

##### Interface 28	database::Feedback ==> web::Feedback

~~~json
{
    "InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "feedback": {
        "type": "object::Feedback",
        "preperties": "Illustrated in appendix"
    }
}
~~~

##### Interface 29	database::Item ==> web::Item

~~~json
{
    "InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "item": {
        "type": "object:Item",
        "preperties": "Illustrated in appendix"
    }
}
~~~

##### Interface 30	web::Item ==> database::Item

~~~json
{
    "InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "item": {
        "type": "object:Item",
        "preperties": "Illustrated in appendix"
    }
}
~~~

##### Interface 31	database::Store ==> web::Location

~~~json
{
    "InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "Location": {
        "type": "object:Location",
        "preperties": "Illustrated in appendix"
    }
}
~~~

##### Interface 32 database::Item ==> web::Statistics

~~~json
{
    "InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 32
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "customerVisits": {
        "type": "integer"
    },
	"feedbacks": {
        "type": "array",
        "items": {
            "type": "object::Feedback",
            "preperties": "Illustrated in appendix"
        },
        "minItems": 1,
        "uniqueItems": true
    }
}
~~~



## Appendix:

##### object::Location

~~~json
{
    "latitude": {
    	"type": "number"
    },
	"longitude":{
    	"type": "number"
    },
	"country" : {
    	"type": "string",
        "minLength": 0
    },
	"state" : {
    	"type": "string",
        "minLength": 0
    },
	"city": {
    	"type": "string",
        "minLength": 0
    },
	"street": {
    	"type": "string",
        "minLength": 0
    },
	"number": {
    	"type": "string",
        "minLength": 0
    },
	"floor": {
    	"type": "string",
        "minLength": 0
    },
	"zipcode": {
    	"type": "string",
        "minLength": 0
    }
}
~~~

##### object::Item

~~~json
{
    "ItemId": {
    	"type": "integer",
        "minLength": 0
    },
    "ItemName": {
    	"type": "string",
        "minLength": 1
    },
	"ItemPrice": {
    	"type": "number",
        "minimum": 0
	},
	"ItemDescription": {
    	"type": "string",
        "minLength": 0
    },
	"ItemImage": {
    	"type": "base64",
        "minLength": 0
    },  
	"ItemStoreId": {
    	"type": "integer",
        "minLength": 0
    },
    "ItemStoreName": {
    	"type": "string",
        "minLength": 1
    },
    "customerVisits": {
        "type": "integer"
    }
}
~~~

+ Description: Same items in different stores have different ItemId, which means ItemId is unique.

##### object::Store

~~~json
{
	"storeId": {
    	"type": "integer",
        "minLength": 0
    },
    "storeName": {
    	"type": "string",
        "minLength": 1
    },
	"location": {
        "type": "object:Location",
        "preperties": "Illustrated in appendix"
    },
	"items": {
        "type": "array",
        "items": {
            "type": "object::Item",
            "preperties": "Illustrated in appendix"
        },
        "minItems": 1,
        "uniqueItems": true
    },
    "StoreDescription": {
    	"type": "string",
        "minLength": 0
    }
}
~~~

##### object::Feedback

~~~json
{
	"Item": {
        "type": "object::Item",
        "preperties": "Illustrated in appendix"
    },
	"comment": {
    	"type": "string",
        "minLength": 0
    },
	"rating": {
        "type":"integer",
        "minimum": 1,
        "maximum": 10
    },
	"UserName": {
    	"type": "string",
        "minLength": 1
    }
}
~~~

##### object::User

~~~json
{
	"userId": {
        "type": "integer",
        "minimum": 0,
    },
	"UserEmail": {
        "type": "email"
    },
	"UserName": {
    	"type": "string",
        "minLength": 1
    },
	"HashedPassword": {
        "type": "string",
    	"minLength": 1,
        "maxLength": 6
    }
}
~~~

##### object::Statistics

	{
		"customerVisits": {
	        "type": "integer"
	    }
		"feedbacks": {
	        "type": "array",
	        "items": {
	            "type": "object::Feedback",
	            "preperties": "Illustrated in appendix"
	        },
	        "minItems": 0,
	        "uniqueItems": true
	    }
	}

---

#### update from v.4 to v.5.1:

1. Use JSON SCHEMA to make it more formal.
   1. Follow [English Version](https://json-schema.org/understanding-json-schema) / [Chinese Version](https://json-schema.apifox.cn/).
   2. Make some slight changes for "object" type for readability.
   3. Add more restrictions on the data formats like the minimum value of integer or the minimum length of string. However, these restrictions may **not be precise before each PM from each group checking them**.
2. Remove the comma after the last item in the JSON.
3. Set unique interface ID.
4. Unified the naming convention to use PascalCase consistently. (except for the formats in JSON SCHEMA)
5. Set maximum length of password for security consideration. 
