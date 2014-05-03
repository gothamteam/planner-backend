#this article gives examples of the user authentication and user information retrival

a user information is saved in using hash datatype "user:111" eg:
key name: "user:wangsuse",
key value contains subkeys like:
"timejoined" : 11231231231.3
"username":"wangsuse"
"firstname":"shusen"
"lastnmae":"wang"
"date of birth":"04061987"
"email":"wangsuse@hotmail.com"
"age":"25"
"sex":"M"
"nickName":"ss",
"id":"111"


username and id are saved in hash "user:" eg:
"wangsuse2011" ,"111"

the id increment is "user:id", single string and is incremented by 1 for every new user

lock is saved in "lock:user:"+lower_userName


username and password is stored in hash "user:password", eg:
key: "wangsuse" value:"mypassword"
key:"yhfy2008" value:"yhfypassword"

friends information are store in a set "user:wangsuse:friends"
value contains a set of friends' unique usernames 
to get the friend for a particular person is just getting the whole set of "user:username:friends"



to get the user authentication, use ajax call post to url with "username=wanguse&passward=mypassword" 
the request will return json with has_access true or false:
{
	username:"wangsuse",
	has_access: "true",
	fristName: "Shusen",
	lastName: "Wang",
	nickName:"ss"
	id:"111"
}
you can then use the has_access to redirect user page to the main app page or login again with error messages.

the friends information can be obtained by sending ajaxcall with "username=wangsuse", 
then a list of friends with their user infor will is sent back as a json file.
	
	