// CPP code to implement relational 
// operators on String objects 
#include<iostream> 
using namespace std; 

void relational_operation(string s1, string s2) 
{ 
	string s3 = s1 + s2; 
	
	if(s1 != s2) 
		cout << s1 << " is not equal to " << s2 << endl; 

	if(s1 > s2) 
		cout << s1 << " is greater than " << s2 << endl; 

	else if(s1 < s2) 
		cout << s1 << " is smaller than " << s2 << endl; 

	if(s3 == s1 + s2) 
		cout << s3 << " is equal to " << s1 + s2 << endl; 
		
} 

// Main function 
int main() 
{ 
	string s1("Geeks"); 
	string s2("forGeeks"); 
	relational_operation(s1, s2); 
	
return 0; 
} 
