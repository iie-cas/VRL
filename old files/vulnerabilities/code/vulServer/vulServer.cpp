#include<stdio.h>
#include<stdlib.h>
#include<iostream>
#include<fstream>
#include<string>
#include<vector>
#include<unistd.h>
#include<libgen.h>
#include<sys/types.h>
using namespace std;

void showInfo(vector<string> &info)
{
	cout<<"******************************************************"<<endl;
	cout<<"\t\t\t0.quit"<<endl;
	for(int i=0; i<info.size(); i+=2)
	{
		cout<<"\t\t\t"<<to_string(i/2+1)<<"."<<info[i]<<": "<<info[i+1]<<endl;
	}
	cout<<"******************************************************"<<endl;
}
int main(int argc, char *argv[])
{
	chdir(dirname(argv[0]));         //将当前目录更改为程序所在目录
	vector<string> info;
	string line;
	unsigned int select = -1;
	ifstream in("./vuls_information");
	if(!in.is_open())  
	{
		cout<<"Error opening file \"vuls_information\""<<endl;
		exit(1);
	}
	while(!in.eof())
	{
		getline(in, line);
		//cout<<line<<"abc"<<endl;
		if(!line.empty())
		{
			info.push_back(line);
		}
	}
	in.close();
	//cout<<info.size()<<endl;
	while(true)
	{
		select = -1;
		showInfo(info);
		while(select>info.size()/2)
		{
			cout<<"请选择对应编号： ";
			cin>>select;
		}
		if(select==0)
		{
			break;
		}
		string vulName = "gnome-terminal -e ./vuls/vul"+to_string(select);    //打开对应漏洞程序
		system(vulName.c_str());	
		
	}
	return 0;
}
