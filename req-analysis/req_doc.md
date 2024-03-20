# DSD Requirements Analysis

 

**Group:** Algorithm Group 

**Theme:** Algorithm Group Requirement Analysis

**Time:** 03/15/2024

 

### Requirements for Web Page group

 

**Requirement 1:** Shop Information Provision

**Description:** The detailed and updated information of the shops should be provided.(If all the information is stored in the data base, then only the name and shop id is required) 

 

**Requirement 2:** Current User Information Provision

**Description:** When a user requests item recommendations upon entering a shop, the Algorithm Group must access user and shop information to deliver effective suggestions. If user data is stored in the database, only the user's name and ID are required.

 

**Requirement 3:** Provide feedback (satisfaction of our recommendation) 

**Description:** Following a shop's query to the Algorithm Group for recommendations, the system should provide a satisfaction score(for example, on the scale from 1 to 10) for the suggested items. This feedback loop enables the Algorithm Group to refine the recommendation algorithm to better align with the preferences of the shops.

 

 

### Requirements for DB group

 

**Requirement 1:**  Access user information with a user ID, basic user information, or user shopping history as input.

 

**Description:** The algorithm module needs personalized recommendations based on user preferences. User information should include basic information (such as age, gender, occupation, education, etc.), historical shopping data (such as shopping store, time, products, quantity, etc.), and user preferences.

```
Demo 1: Please provide me with all users who are students and have shopped at Walmart. 

Demo 2: Please provide user 001's user information.
```



**Requirement 2:** Access shop information that meets certain criteria with a shop ID or shop type as input. There might be search range limitations (latitude and longitude + radius).

 

**Description:** The algorithm module needs to recommend specific shops or products to users based on shop information. Shop information should include the shop's name, type, sales history (such as quantities of certain products sold), and detailed information about all products (such as product name, brief description, category, etc.). To make effective recommendations based on the user's geographical location, the algorithm module will provide the database with the user's location information (possibly latitude and longitude) and the search radius (x kilometers), and the database should return shop information that meets these criteria.


```
Demo 1: Please provide me with information about all antique shops. </span>

Demo 2: Please provide shop 001's shop information.

Demo 3: Please provide all shop information within a 10km radius of (30°N, 120°E).
```

 

**Requirement 3:** Store/Access shop/user analysis reports.

 

**Description:** To reduce unnecessary computational burdens, the algorithm module will save the analysis and learning-derived shop/user analysis reports in the database.

 

 

 

### Requirements for User group

 

**Requirement 1:** about source data we collect for recommendation system.

**Description:** Able to set their preference setting during their registration and leave their record during using our application so that we can provide better recommendation service based on the things i have just said.

 

**Requirement 2:** about how we adjust our recommendation strategy 

**Description:** User should be able to leave a comment or grade on the thing that has been recommended to them. and we can based on those thing to adjust weather a item is worthy to be recommended or whether our current recommendation system works on the specific user well, should we adjust some weights of parameters to change our recommendation strategy.

 

**Requirement 3:** (optional): friend system

**Description:** (optional) probably can add friend system to the project. just a common friend system which can send message and recommend people have similar interest to the user.