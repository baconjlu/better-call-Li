# Interface Specification

[TOC]



## frontend-database

##### Interface 1	frontend::Login ==> database::Login 

~~~json
{
	"InterfaceId": {
        "type":"integer",
        "minimum": 1,
        "maximum": 33
    },
    "CurrentUser": {"type": "string"},
    "UserName": {
        "type": "string",
    	"minLength": 1
    },
    "PassWord": {
        "type": "string",
    	"minLength": 1
    }
}

return with

{
    "InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 33
    },
    "CurrentUser": {
        "type": "string",
        "miLLength": 1
    },
    "MatchToken": {"type": "boolean"},
    "Interest": {
    	"type": "array",
        "items": "string" 
    }
}
~~~

+ Tip1: InterfaceId means the id of interface that we use the identify the interface index and json content. We have 33 interfaces in total so the InterfaceId will range from 1 to 33.
+ Tip 2: CurrentUser is None if this is a anonymous visiting, otherwise it is the UserName.

+ Tip3: "interests" in return JSON is set to null if the user has not been set.(login for the first time)

+ Description of the interface: When the user logs in, this interface is called. On the front end, the user needs to input the Username and Password, which are then sent to the database. The database performs verification, and the result of the verification is indicated by the returned match_token.

##### Interface 2	frontend::Location ==> database::Location

~~~json
{
    "InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 33
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

+ Description of the interface: When the user needs data related to location information, such as viewing a map, they need to provide the CurrentLocation to the database.

##### Interface 3	frontend::Store ==> database::Store

~~~json
{
    "InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 33
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
        "maximum": 33
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
        "maximum": 33
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "HuntedStoreIdList": {
        "type": "array",
        "items": {
            "type": "HistoryVisit",
         	"properties": {
                "StoreId": {
                    "type": "integer",
                    "minimum": 0
                },
                "VisitTime": {
                    "type": "data-time"
                }
            }
        },
        "minItems": 0,
        "uniqueItems": true
    }
}
```

+ Tips1: HuntedList is like a "Browsing history".

+ Description of the interface: When a user browses new stores, they need to provide the HuntedStoreIdList to the database for updating the content stored in the database.

##### Interface 5	database::HuntedStore ==> frontend::HuntedStore

```json
{
 	"InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 33
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
        "maximum": 33
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
        "maximum": 33
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
        "maximum": 33
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
        "maximum": 33
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

##### Interface 8	frontend::Feedback2Store ==> database::Feedback2Store

```json
{
	"InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 33
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
	"Feedback":{
        "type": "object::Feedback2Store",
        "properties": "Illustrated in appendix"
    }
}
```

+ Tip1 : Feedback is a rating that evaluate the recommendation results.
+ Tip2 : "rating" should be a positive integer from 1 to 10.
+ Description of the interface: Users evaluate the store recommendations provided by the recommendation system, specifically including comments and ratings, which are transmitted to the database.

##### Interface 9	frontend::Feedback2Item ==> database::Feedback2Item

```json
{
	"InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 33
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
	"Feedback":{
        "type": "object::Feedback2Item",
        "properties": "Illustrated in appendix"
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
        "maximum": 33
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
    	"minLength": 1
    },
    "Birthday": {
        "type": "date"
    },
    "Interests": {
    	"type": "array",
       	"items": "string",
    }
}
```

+ Tip1: This is used to update customer information stored in the database. 
+ Tip2: Interests are users' preference used recommendation.
+ Description of the interface: When a user wishes to update their information, they provide the database with new details such as Birthday, Interests, and CurrentLocation. It should be noted that for security reasons, before updating the information, the user needs to re-enter their Username and Password for verification.

##### Interface11	database::Customer ==> frontend:: Customer

```json
{
	"InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 33
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
    	"minLength": 1
    },
    "Birthday": {
        "type": "date"
    },
    "Interests": {
    	"type": "array",
       	"items": "string",
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
        "maximum": 33
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
    	"minLength": 1
    }
}

return with
{
	"InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 33
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "successful_token": {"type": "boolean"}
}

~~~

+ Tip1: this is used for registration and to check whether the UserName is unique.
+ Description of the interface: Users register by entering their Username and Password on the front end, which are then transmitted to the database. The database checks if the same Username already exists and returns a successful_token to the front end to indicate whether the registration was successful or not.

---



## algorithm-database

##### Interface 13	database::Store ==> algorithm::Store

~~~json
{
	"InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 33
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
	"Stores": {
        "type": "array",
        "items": {
            "type": "object::Store",
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

 + Tip1: this one is used for generating recommendation user for specific user
 + Description of the interface: database delivers stores based on the location of specific user. for instance, when we gonna recommended stores for user A, database should deliver all the stores nearby user A. the threshold might be 1km or 2km or other specific distance. And recommendation system use the data provided by this interface to generate recommendation result.

##### Interface 14	database::Customer ==> algorithm::user

~~~json
{
   	"InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 33
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
		"type": "object::Customer",
        "preperties": "Illustrated in appendix"
    }
}
~~~

+ Tip1: this one is the specific user who calls recommendation service

+ Tip2: customer should conclude data such as his preference and history review.

+ Description of the interface: recommendation system needs the preference of the user to generate recommendation.

##### Interface 15	database::Item ==> algorithm::recommendation algorithm

~~~json
{
    "InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 33
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

+  Tip1: actually this interface is for extension functions in the future.

##### Interface 16	algorithm::recommendation  ==> database::  algorithm

~~~json
{
    "InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 33
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
    "RecommendedStores": {
        "type": "array",
        "items": {
            "type": "object::Store",
            "preperties": "Illustrated in appendix"
        },
        "minItems": 1,
        "uniqueItems": true
    }
}
~~~

+ Tip1: this one is to deliver recommendation back to database

+ Description of the interface: recommendation in this interface is considered to be an array of stores. the size of this array is concrete. when there is not enough interested store around. the recommendation might recommend something not in user's preference as exploration.

##### Interface 17  database::  algorithm ==> algorithm::recommendation 

~~~json
{
    "InterfaceId":{
        "type":"integer",
        "minimum": 1,
        "maximum": 33
    },
    "CurrentUser": {
        "type": "string",
        "minLength": 1
    },
	"Feedback":{
        "type": "object::Feedback2Store",
        "properties": "Illustrated in appendix"
    }
}
~~~

+ Tip1: this one is about rating the recommendation
+ description of the interface: database deliver the feedback which is about rating the recommendation. and algorithm might adjust its recommendation strategy based on this feedback.

---



## web-database

##### Interface 18	web::Registration ==> database::Registration

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
        "minLength": 1,
        "maxLength": 1
    },
    "MatchToken": {"type": "boolean"}
}
~~~

* Description of the interface: This occurs when a new store owner attempts to register its account, which returns an indicator asserting whether the registration is successful.
* Tip1: At the database end, if an existing store owner account holds the same username, the registration should be considered unsuccessful.

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
    "PassWord": {
        "type": "string",
    	"minLength": 1,
        "maxLength": 6
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
        "minLength": 1,
        "maxLength": 1
    },
    "MatchToken": {"type": "boolean"}
}
~~~

* Description of the interface: This takes place when a store owner or the administrator attempts to login to their accounts, which returns an indicator asserting whether the login process is successful.
* Tip1: At the database end, if the username and the password match a registered account, the login should be considered successful.
* Tip2: Currently the username of the administrator account is "admin", so the role of the user logged-in can be determined by the username.

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

* Description of the interface: This procedure describes when the administrator make changes to user or store data, which information will be transmit to the database.
* Tip1: For easy implementation of data flow from the front-end to back-end, the transmission of user data, store info and item info(as a subclass of store info), can be implemented separately.
* Tip2: This procedure is the same as the next Interface; the only difference is the direction of the dataflow.
* Tip3: For any interface like this contains multiple classes, database can separate the class and implement with multiple steps of requests.

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
    "avgRating": {
        "type":"float",
        "minimum": 1,
        "maximum": 10
    },
    "selectedComments":{
        "type": "array",
    	"items": {
            "type": "string"
        },
        "minItems": 1
	},
    "overallAdvice": {
    	"type": "string",
        "minLength": 1
	}
}
~~~

* Description of the interface: This describes the analytical data that is obtained by the administrator: "avgRating" means to the average rating of a specific store; "selectedComments" is a list consists of all the comment that have a lower rating of 2; "overallAdvice"  refers to a string that generated by algorithms, to be specific, the advice or advices provided by AI for systematic refinement.
* Tip1: The implementation of "avgRating" can be consistent with how store info are obtained in the previous interface. The ultimate goal is to display a table listing stores alongside their ratings.

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
    "customerVisits": {
		"type": "int",
        "minimum" 0
    },
    "feedback": {
    	"type": "object::Feedback",
        "properties": "Illustrated in appendix"
    }
}
~~~

Description of the interface: This occurs when a store owner attempts to checking the statistics of the store. The content of the "statistics" class is provided in appendix. customerVisits can be simplified to the number of purchases happening in a store, while "feedback" refers to the feedbacks toward item happening after each single purchase.

##### Interface 24	database::Store ==> web::StoreInfo

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
    "Location": {
        "type": "object:Location",
        "preperties": "Illustrated in appendix"
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
    "storeName": {
        "type": "string",
        "minLength": 1
    },
    "Location": {
        "type": "object:Location",
        "preperties": "Illustrated in appendix"
    }
}
~~~

* Description of the interface: This procedure occurs when a store owner wants to access his store info (other than items) and update it if needed.

* Tip1: The UserName and Password (store owner as a user to the system) of the store owner should be stored in "StoreInfo" class in database.  

##### Interface 25	database::Item ==> web::Item

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
    "item": {
        "type": "object:Item",
        "preperties": "Illustrated in appendix"
    }
}
~~~

Description of the interface: This procedure occurs when a store owner wants to access his items' information and update it if needed.



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

+ Tip1: Same items in different stores have different ItemId, which means ItemId is unique.

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

##### object::Feedback2Store

~~~json
{
	"Item": {
        "type": "object::Store",
        "preperties": "Illustrated in appendix"
    },
	"comment": {
    	"type": "string",
        "minLength": 0
    },
	"rating": {
        "type":"int",
        "minimum": 1,
        "maximum": 10
    },
	"UserName": {
    	"type": "string",
        "minLength": 1
    }
}
~~~

+ Description: This is used to give feedback to the recommendation results (a store) and helps optimize recommendation algorithm.



##### object::Feedback2Item

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
        "type":"int",
        "minimum": 1,
        "maximum": 10
    },
	"UserName": {
    	"type": "string",
        "minLength": 1
    }
}
~~~

+ Description: This is used to give feedback to the purchased item and helps stores to offer better service.

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
    	"minLength": 1
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
	            "type": "object::Feedback2Item",
	            "preperties": "Illustrated in appendix"
	        },
	        "minItems": 0,
	        "uniqueItems": true
	    }
	}

##### object::EngagementData

~~~json
{
    "AvgRating": {
        "type": "number",
        "minimum": 0
    },
    "SelectedComment": {
        "type": "array",
        "items":{
            "type": "string"
        },
        "minItems": 1,
        "uniqueItems": true
    }
    
    
}
~~~

+ Tip1: AvgRating is the average rating of a paticular store.
+ Tip2: SelectedComment is the low scored comment by user selected as reference for refining the system



---





#### update from v.5 to v.6:

1. Add the 'VisitTime' to HuntedList.
2. Add Algorithm interfaces to deal with feedback.
3. Specify the two kind of feedback:
   1. Feedback2Store is used to give feedback to the recommendation results (a store) and helps optimize recommendation algorithm.
   2. Feedback2Item is used to give feedback to the purchased item and helps stores to offer better service.\
4. We have updated the description of the algorithm group.
5. The web group modified some interfaces and added description.
6. The interests have been changed from integer array to string.
7. The interface one return an additional "interests". 
